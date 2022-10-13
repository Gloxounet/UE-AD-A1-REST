import os
import json
from dotenv import load_dotenv
import requests
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

MOVIE_PORT = os.getenv('MOVIE_PORT')

MOVIE_URL = f"http://127.0.0.1:{MOVIE_PORT}"


def get_movie_by_id(id):
    try:
        res = requests.get(f'{MOVIE_URL}/movies/{id}')
    except:
        return "{'error': 'error fetching movie microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response


def get_list_movies():
    try:
        res = requests.get(f'{MOVIE_URL}/json')
    except:
        return "{'error': 'error fetching movie microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def get_movies_by_title(title):
    try:
        res = requests.get(f'{MOVIE_URL}/moviesbytitle?title={title}')
    except:
        return "{'error': 'error fetching movie microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def get_movies_by_director(director):
    try:
        res = requests.get(f'{MOVIE_URL}/moviesbydirector?director={director}')
    except:
        return "{'error': 'error fetching movie microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def main():
    print("-------------- GetMovieByID --------------")
    print(get_movie_by_id("a8034f44-aee4-44cf-b32c-74cf452aaaae"))

    print("-------------- GetListMovies --------------")
    print(get_list_movies())

    print("-------------- GetMoviesByTitle --------------")
    print(get_movies_by_title("Creed"))

    print("-------------- GetMoviesByDirector --------------")
    print(get_movies_by_director("Ridley Scott"))
