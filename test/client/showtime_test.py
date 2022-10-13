import os
import json
from dotenv import load_dotenv
import requests
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

SHOWTIME_PORT = os.getenv('SHOWTIME_PORT')

SHOWTIME_URL = f"http://127.0.0.1:{SHOWTIME_PORT}"


# SHOWTIME
def get_showtimes():
    try:
        res = requests.get(f'{SHOWTIME_URL}/showtime')
    except:
        return "{'error': 'error fetching bookings microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def get_showtimes_by_date(date):
    try:
        res = requests.get(f'{SHOWTIME_URL}/showtime/{date}')
    except:
        return "{'error': 'error fetching bookings microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def main():
    print("-------------- GetShowtimes --------------")
    print(get_showtimes())

    print("-------------- GetShowtimesByDate --------------")
    print(get_showtimes_by_date("20151130"))
