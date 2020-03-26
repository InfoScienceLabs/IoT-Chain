import uuid
from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bigchain"
mongo = PyMongo(app)

uuid_str = str(uuid.uuid4())
data = mongo.db.api_key

data.insert({'api_key':uuid_str})

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 2020)  