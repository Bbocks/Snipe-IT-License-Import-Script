import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# CONFIGURATION
SNIPEIT_API_URL = os.getenv("SNIPEIT_API_URL")
API_TOKEN = os.getenv("API_TOKEN")
LICENSE_ID = 5  # Replace with your target license ID

# Headers for API requests
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_available_license_seats(license_id):
    url = f"{SNIPEIT_API_URL}/licenses/{license_id}/seats"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    seats = response.json().get('rows', [])

    # Filter out assigned seats
    available_seats = [seat for seat in seats if seat.get('assigned_user') is None]

    print(f"\nAvailable seats for License ID {license_id}:")
    for seat in available_seats:
        assigned_user = seat.get('assigned_user')
        assigned_user_name = assigned_user.get('name') if assigned_user else "Unassigned"
        print(f" - Seat ID: {seat['id']}, Seat Number: {seat['name']}, Assigned To: {assigned_user_name}")
    
    return available_seats

def get_assigned_license_seats(license_id):
    url = f"{SNIPEIT_API_URL}/licenses/{license_id}/seats"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    seats = response.json().get('rows', [])

    # Filter out assigned seats
    available_seats = [seat for seat in seats if seat.get('assigned_user') is not None]

    print(f"\nAvailable seats for License ID {license_id}:")
    for seat in available_seats:
        assigned_user = seat.get('assigned_user')
        assigned_user_name = assigned_user.get('name') if assigned_user else "Unassigned"
        print(f" - Seat ID: {seat['id']}, Seat Number: {seat['name']}, Assigned To: {assigned_user_name}")
    
    return available_seats

# Run it
if __name__ == "__main__":
    get_available_license_seats(LICENSE_ID)
    get_assigned_license_seats(LICENSE_ID)