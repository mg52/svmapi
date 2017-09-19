# svmapi - Python Support Vector Machine (SVM) API

This API makes SVM classification using given trained and test data.

I used Flask for REST API, MongoDB to handle API Key and storing train data and scikit-learn for SVM algorithm. Also Heroku is used to publish the API.

API Link: https://svmapi.herokuapp.com/

Here is the API Keys that you can use: "4bfc1e9c9d25f192a2f442e748aac4", "12bafb07d521189510289229deadc5", "ceeac25e0e7044ec80e7027f827add"

Also I can create new unique API Keys for you. If you want you can ask me via using issues. I wish you can create your own unique API key but I am using free tier of MongoDB so the storage is limited.

## Train Data Example:

You should give train data like this:

x:[[1, 1], [2, 1],[-1, -1.3], [-2, -1]]

y:[1, 1, 2, 2]

and you should give your API Key as 'key'

and make HTTP Post Request like below:

https://svmapi.herokuapp.com/train?x=[[1, 1], [2, 1],[-1, -1.3], [-2, -1]]&y=[1, 1, 2, 2]&key=4bfc1e9c9d25f192a2f442e748aac4

Success Output: "Data Trained."

## Predict Data Example:

You should give test data like this:

x=[[1.1, 1.2]]

and you should give your API Key as 'key'

and make HTTP Post Request like below:

https://svmapi.herokuapp.com/predict?key=4bfc1e9c9d25f192a2f442e748aac4&x=[[1.1, 1.2]]

When it is successful it will return predicted data "1"

## Validate API Key:

Make a GET Request like below:

https://svmapi.herokuapp.com/validateApiKey/4bfc1e9c9d25f192a2f442e748aac4
