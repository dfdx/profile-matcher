import os
from flask import Flask, json, redirect, render_template, request, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)
client = None
vk_app_id = 5043927
redirect_uri = ""

@app.route("/")
def index():
    print(request.cookies)
    if "vk_token" in request.cookies:
        vk_token = request.cookies["vk_token"]
        return render_template("index.html")
    else:
        return redirect(url_for("vk_auth"))

@app.route("/search")
def search():
  if "q" in request.args:
      if "vk_token" in request.cookies:
          token_param = "&access_token=" + request.cookies["vk_token"]
          query_string = request.args["q"]
          vk_query = "https://api.vk.com/method/users.search?q=" + query_string + token_param
          print(vk_query)
          results = requests.get(vk_query).json()["response"]
          model = {'count': results[0], 'persons': results[1:]}
          return render_template("search.html", model=model)
      else:
          redirect(url_for("vk_auth"))
  else:
      redirect(url_for("/"))

@app.route("/vk_auth")
def vk_auth():
    return render_template("vk_auth.html", app_id=vk_app_id, redirect_uri=redirect_uri)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    mongo_uri = os.environ.get("MONGOLAB_URI", "mongodb://localhost:27017/profile-matcher")
    client = MongoClient(mongo_uri)
    vk_app_id = int(os.environ.get("VK_APP_ID", 5043927))
    redirect_uri = os.environ.get("VK_REDIRECT_URI", "http://localhost:" + str(port))
    app.run(port=port, debug=True)