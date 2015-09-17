import os
from flask import Flask, abort, json, render_template
# from pymongo import MongoClient
import requests

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
mongo_uri = os.environ.get("MONGOLAB_URI", "mongodb://localhost:27017/profile-matcher")
# client = MongoClient(mongo_uri)
vk_app_id = int(os.environ.get("VK_APP_ID", 5043927))
redirect_uri = os.environ.get("VK_REDIRECT_URI", "http://localhost:" + str(port))

@app.route("/")
def index():
    return render_template("index.html", vk_app_id=vk_app_id)

@app.route("/api/search/vk", methods=['POST'])
def search():
    abort(501)

if __name__ == '__main__':
    app.run(port=port, debug=True)
