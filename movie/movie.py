from unittest import result
from urllib import response
from flask import Flask, render_template, request, jsonify, make_response
import json
import requests

#.env imports
from dotenv import load_dotenv
from pathlib import Path
import os

#Getting env variables
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
IMDB_API_KEY = os.getenv('IMDB_KEY')

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'
#IMDb variables
IMDB_LINK = f"https://imdb-api.com/en/API/"


#Loading small db
with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res

    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    if not(request.args) or request.args["title"]=="": return make_response(jsonify({'error':'invalid arguments'}),400)

    req = request.args
    title = req["title"]
    link = IMDB_LINK + f"SearchMovie/{IMDB_API_KEY}/"+title

    resp = json.loads(requests.get(link).text)
    results = resp["results"]
    
    movie_list = list(map(lambda movie:fetchMovieByIdIMDb(movie["id"]),results))

    return make_response(jsonify({"movies":movie_list}),200)

def fetchMovieByIdIMDb(_id:str):
    link = IMDB_LINK + f"Title/{IMDB_API_KEY}/"+_id
    movie = json.loads(requests.get(link).text)
    res = {
        "director":movie["directors"],
        "rating":movie["imDbRating"],
        "title":movie["title"],
        "id":movie["id"]
        }
    
    return res

@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

@app.route("/movies/abovefive", methods=['GET'])
def get_movies_rated_above_five():
    movie_list = []
    for movie in movies:
        if float(movie["rating"]) >= 5 :
            movie_list.append(movie)
    return make_response(jsonify(movie_list),400)

@app.route("/moviesbydirector", methods=['GET'])
def get_movie_bydirector():
    json = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                json.append(movie)

    if not json:
        res = make_response(jsonify({"error": "movie director not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res

if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
