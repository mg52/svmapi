from pymongo import MongoClient
from flask import request, abort, Flask, jsonify
import os
from binascii import hexlify
from functools import wraps
import numpy as np
from sklearn.svm import SVC

app = Flask(__name__)

MONGO_URL = os.environ.get('MONGODB_URI')
client = MongoClient(MONGO_URL)
#client = MongoClient('mongodb://localhost:27017/') #For Locally
db = client['heroku_mlxjr59b']

def generateApiKeyFunc():
    theKey = hexlify(os.urandom(15)).decode()
    db.keys.insert_one({'apiKey': theKey})
    return theKey


def validateApiKey(theKey):
    for doc in db.keys.find({}):
        if (theKey == doc["apiKey"]):
            return True
    return False


"""
def checkApiKey(inputApiKey):
    for doc in db.keys.find({}):
        if(inputApiKey == doc["apiKey"]):
            return True
    return False
"""


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        for doc in db.keys.find({}):
            if request.args.get('key') and request.args.get('key') == doc["apiKey"]:
                return view_function(*args, **kwargs)
        abort(401)

    return decorated_function


@app.route('/generateApiKey', methods=['GET'])
def generateApiKey():
    return generateApiKeyFunc()


@app.route('/validateApiKey/<inputKey>', methods=['GET'])
def checkTheKey(inputKey):
    return jsonify(validateApiKey(inputKey))


@app.route('/getApiKeys', methods=['GET'])
def getApiKeys():
    data = {'keys': []}
    for doc in db.keys.find({}):
        data['keys'].append(doc["apiKey"])
    return jsonify(data)


@app.route('/test', methods=['GET', 'POST'])
def fun():
    if request.method == 'POST':
        return jsonify('Post Test OK')
    else:
        return jsonify('Get Test OK')


@app.route('/train', methods=['POST'])
@require_appkey
def trainData():
    str = request.args["x"]
    input = list(map(float, str.replace('[', '').replace(']', '').split(',')))
    x = [input[i:i + int(len(input) / (str.count('[') - 1))] for i in range(0, len(input), int(len(input) / (str.count('[') - 1)))]

    str2 = request.args["y"]
    y = list(map(float, str2.replace('[', '').replace(']', '').split(',')))

    try:
        db.SVMData2.insert_one({"data": {"apiKey": request.args["key"], "x": x, "y": y}})
        return jsonify('Data Trained.')

    except:
        return jsonify('ERROR: Data CANNOT Be Trained.')


@app.route('/predict', methods=['POST'])
@require_appkey
def predictData():
    str = request.args["x"]
    input = list(map(float, str.replace('[', '').replace(']', '').split(',')))
    x = [input[i:i + int(len(input) / (str.count('[') - 1))] for i in range(0, len(input), int(len(input) / (str.count('[') - 1)))]
    
    try:
        data = db.SVMData2.find_one({'data.apiKey':request.args["key"]})
        clf = SVC()
        clf.fit(np.array(data['data']['x']), np.array(data['data']['y']))
        predicted = clf.predict(x)
        print(predicted)
        return jsonify(predicted)
    except:
        return jsonify('ERROR: Data CANNOT Be Predicted.')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    #app.run(debug=True)
