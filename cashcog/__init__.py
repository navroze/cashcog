from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from cashcog.config import DEBUG, MONGODB_CASHCOG_URI

app = Flask(__name__, static_url_path="/static/")
CORS(app)
app.debug = DEBUG

client = MongoClient(MONGODB_CASHCOG_URI)
db = client.expenses_db

from cashcog.routes import routes
