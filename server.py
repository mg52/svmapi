from pymongo import MongoClient
from flask import request, abort, Flask, jsonify
import os
from binascii import hexlify
from functools import wraps

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
        if(theKey == doc["apiKey"]):
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
        return 'Post Test OK'
    else:
        return 'Get Test OK'

@app.route('/train', methods=['POST'])
@require_appkey
def put_user():
    return request.args["username"]

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT", 5000)))
