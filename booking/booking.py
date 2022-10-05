import json
import os
from pathlib import Path

# .env imports
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response

# Getting env variables
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
IMDB_API_KEY = os.getenv('IMDB_KEY')

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# List all the bookings

@app.route("/bookings", methods=['GET'])
def get_json():
    return make_response(jsonify(bookings), 200)


# Get the bookings for the user corresponding to <userid>

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking), 200)
            return res
    return make_response(jsonify({"error": "booking ID not found"}), 400)


# Add a booking for the user corresponding to <userid>
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_by_user(userid):
    req = request.get_json()

    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return make_response(jsonify({"error": "booking ID already exists"}), 409)

    res = {
        "userid": userid,
        "dates": [
            {
                "date": req["date"],
                "movies": req["movieid"]
            }
        ]
    }

    bookings.append(res)

    res = make_response(jsonify({"message": "booking added"}), 200)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
