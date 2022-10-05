import json
import os
from pathlib import Path

# .env imports
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response

# Getting env variables
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
IMDB_API_KEY = os.getenv('IMDB_KEY')

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtime", methods=['GET'])
def get_schedule():
    return make_response(jsonify(schedule), 200)


@app.route("/showtime/<date>")
def get_movie_by_date(date):
    date = str(date)
    movies = []
    for s in schedule:
        if int(s["date"]) == int(date):
            movies.append(s["movies"])
    if movies != "":
        return make_response(jsonify(json), 200)

    return make_response(jsonify({'error': 'not found'}))


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
