
from flask import Flask, render_template, request, redirect, session, jsonify
import requests
from flask_session import Session
from datetime import datetime
import pytz
from sql import * #Used for database connection and management
from SarvAuth import * #Used for user authentication functions
from auth import auth_blueprint
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

autoRun = True #Change to True if you want to run the server automatically by running the app.py file
port = 5000 #Change to any port of your choice if you want to run the server automatically
authentication = True #Change to False if you want to disable user authentication

if authentication:
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

#This route is the base route for the website which renders the index.html file
@app.route("/", methods=["GET", "POST"])
def index():
    if not authentication:
        return render_template("index.html")
    else:
        if not session.get("name"):
            return render_template("index.html", authentication=True)
        else:
            return render_template("/auth/loggedin.html")

@app.route('/autocomplete/cities')
def autocomplete_cities():
    query = request.args.get('q')
    if not query:
        return jsonify([])

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    params = {
        "namePrefix": query,
        "limit": 5
    }

    response = requests.get(url, headers=headers, params=params)
    cities = response.json().get("data", [])

    results = [f"{city['city']}, {city['country']}" for city in cities]
    return jsonify(results)

if autoRun:
    if __name__ == '__main__':
        app.run(debug=True, port=port)
