import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

# CONFIGURATION
SNIPEIT_API_URL = os.getenv("SNIPEIT_API_URL")
API_TOKEN = os.getenv("API_TOKEN")
LICENSE_ID = 0  # Replace with your target license ID
USER_FILE = '.csv' # Can use a .csv, .xls, or .xlsx file

# Headers for API requests
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# === FUNCTIONS ===

def load_user_data(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(file_path)
    elif ext in ('.xls', '.xlsx'):
        return pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format")

def get_user_by_email(email):
    url = f"{SNIPEIT_API_URL}/users"
    response = requests.get(url, headers=HEADERS, params={'search': email})
    response.raise_for_status()
    users = response.json().get('rows', [])
    return users[0] if users else None

def get_available_license_seats(license_id):
    url = f"{SNIPEIT_API_URL}/licenses/{license_id}/seats"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return [seat for seat in response.json().get('rows', []) if seat.get('assigned_user') is None]

def assign_specific_seat_to_user(license_id, seat_id, user_id):
    url = f"{SNIPEIT_API_URL}/licenses/{license_id}/seats/{seat_id}"
    payload = {"assigned_user": user_id}
    response = requests.put(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# === MAIN ===

def main():
    users = load_user_data(USER_FILE)
    available_seats = get_available_license_seats(LICENSE_ID)
    count = 0

    if not available_seats:
        print("❌ No available license seats.")
        return

    if len(users) > len(available_seats):
        print("⚠️ More users than available seats. Only assigning up to available count.")

    for i, (_, row) in enumerate(users.iterrows()):
        count = count + 1
        if i >= len(available_seats):
            break
        email = row['email']
        user = get_user_by_email(email)
        if not user:
            print(f"❌ User not found: {email}")
            continue
        seat = available_seats[i]
        try:
            assign_specific_seat_to_user(LICENSE_ID, seat['id'], user['id'])
            print(f"✅ Assigned seat {seat['id']} to {email}")
        except requests.HTTPError as e:
            print(f"❌ Error assigning to {email}: {e}")
            
        # Used to get around 120 request per minute api limit
        if count >= 50:
            time.sleep(60)
            count = 0

if __name__ == "__main__":
    main()