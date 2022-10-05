import json
import os
from pathlib import Path

import requests
# .env imports
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response

# Getting env variables
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
IMDB_API_KEY = os.getenv('IMDB_KEY')

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'
# IMDb variables
IMDB_LINK = f"https://imdb-api.com/en/API/"

# Loading small db
with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# Return all the values in the JSON file
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


# Gets a movie datas on IMDB database from the movie ID
def fetch_movie_by_id_imdb(_id: str):
    try:
        link = IMDB_LINK + f"Title/{IMDB_API_KEY}/" + _id
        movie = json.loads(requests.get(link).text)
        res = {
            "director": movie["directors"],
            "rating": movie["imDbRating"],
            "title": movie["title"],
            "id": movie["id"]
        }
        return res
    except KeyError:
        return None


# Gets a movie datas from the database, if not found search on the IMDB database
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_by_id(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res

    imdb = fetch_movie_by_id_imdb(movieid)
    print(imdb)
    if imdb is not None: return make_response(jsonify(imdb), 200)

    return make_response(jsonify({"error": "Movie ID not found"}), 400)


# Gets the movie datas from its title
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_by_title():
    if not request.args or request.args["title"] == "": return make_response(jsonify({'error': 'invalid arguments'}),
                                                                             400)

    req = request.args
    title = req["title"]
    link = IMDB_LINK + f"SearchMovie/{IMDB_API_KEY}/" + title

    resp = json.loads(requests.get(link).text)
    results = resp["results"]

    movie_list = list(map(lambda movie: fetch_movie_by_id_imdb(movie["id"]), results))

    return make_response(jsonify({"movies": movie_list}), 200)


# Creates a movie from the data given in a POST
@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res


# Updates a movie ratings from its ID
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


# Delete a movie from its ID
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


# Get all the movies with a rating above 5
@app.route("/movies/abovefive", methods=['GET'])
def get_movies_rated_above_five():
    movie_list = []
    for movie in movies:
        if float(movie["rating"]) >= 5:
            movie_list.append(movie)
    return make_response(jsonify(movie_list), 400)


# Get the movies directed by the given director
@app.route("/moviesbydirector", methods=['GET'])
def get_movie_by_director():
    directors = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                directors.append(movie)

    if not directors:
        res = make_response(jsonify({"error": "movie director not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
