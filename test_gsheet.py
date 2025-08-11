import os
import pandas as pd
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv('GSPREAD_SERVICE_ACCOUNT_JSON')
print("SERVICE_ACCOUNT_FILE =", SERVICE_ACCOUNT_FILE)  # <-- Add this line to check path

SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME')
WORKSHEET_NAME = os.getenv('GOOGLE_SHEET_WORKSHEET')

def read_google_sheet():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open(SHEET_NAME)
    worksheet = sheet.worksheet(WORKSHEET_NAME)
    data = worksheet.get_all_records()

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = read_google_sheet()
    print(df.head())

