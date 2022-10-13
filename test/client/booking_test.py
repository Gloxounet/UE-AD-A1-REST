import os
import json
from dotenv import load_dotenv
import requests
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

BOOKING_PORT = os.getenv('BOOKING_PORT')

BOOKING_URL = f"http://127.0.0.1:{BOOKING_PORT}"

def get_booking_by_userId(userId):
    try:
        res = requests.get(f'{BOOKING_URL}/bookings/{userId}')
    except:
        return "{'error': 'error fetching bookings microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response


def get_list_bookings():
    try:
        res = requests.get(f'{BOOKING_URL}/bookings')
    except:
        return "{'error': 'error fetching bookings microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

# Booking service tester
def main():
    print("-------------- GetBookingById --------------")
    print(get_booking_by_userId("dwight_schrute"))

    print("-------------- GetListBookings --------------")
    print(get_list_bookings())