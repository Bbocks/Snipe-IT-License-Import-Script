# Snipe-IT License Import Script

This repository contains Python scripts to automate the assignment and management of license seats in Snipe-IT using its API. The scripts are designed to help administrators efficiently assign software licenses to users based on data from CSV or Excel files.

## Features
- Assign available license seats to users in bulk from a CSV or Excel file
- Query available and assigned license seats for a specific license
- Handles Snipe-IT API rate limits
- Supports both `.csv` and `.xlsx`/`.xls` user data files

## Files
- `license_import.py`: Main script to assign available license seats to users listed in a file
- `get_seat_id.py`: Utility script to list available and assigned license seats for a given license
- `users-pro.csv`, `users-standard.csv`: Example user data files (CSV format)

## Requirements
- Python 3.7+
- [pandas](https://pandas.pydata.org/)
- [requests](https://docs.python-requests.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [openpyxl](https://openpyxl.readthedocs.io/) (for Excel file support)

Install dependencies:
```bash
pip install pandas requests python-dotenv openpyxl
```

## Setup
1. **Clone the repository**
2. **Create a `.env` file** in the project directory with the following variables:
   ```env
   SNIPEIT_API_URL=https://your-snipeit-instance/api/v1
   API_TOKEN=your_api_token_here
   ```
3. **Prepare your user data file** (CSV or Excel) with at least a `name` and  `email` column.

## Usage

### Assign License Seats
Edit `LICENSE_ID` and `USER_FILE` in `license_import.py` to match your target license and user file. Then run:
```bash
python license_import.py
```

### List License Seats
Edit `LICENSE_ID` in `get_seat_id.py` and run:
```bash
python get_seat_id.py
```

## Notes
- The script respects Snipe-IT API rate limits by pausing after every 50 assignments.
- Only users found in Snipe-IT will be assigned a seat; missing users are reported.
- The script assigns seats in the order they are listed in the user file and available in Snipe-IT.

## License
This project is provided as-is for internal use. See [Snipe-IT](https://snipeitapp.com/) for more information about the API and licensing.
