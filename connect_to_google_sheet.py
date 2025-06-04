
import gspread
from google.oauth2.service_account import Credentials

import os
#from dotenv import load_dotenv,dotenv_values

scopes = [ "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("/etc/secrets/cred.json", scopes=scopes)#for deployment
#creds = Credentials.from_service_account_file("cred.json", scopes=scopes)#local development
client = gspread.authorize(creds)

#sheet_id=os.getenv("GOOGLE_SHEET_ID")
sheet_id = "1v21AGPdkgt_TAC9y9XfVI5Hztr2JXPn6KF9QXo53l50"

spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
spreadsheet = client.open_by_url(spreadsheet_url)

sheet1 = client.open_by_url(spreadsheet_url).sheet1
sheet2 = spreadsheet.worksheet('Sheet1')





def return_data():
    sheet1 = client.open_by_url(spreadsheet_url).sheet1
    data=sheet1.get_all_records()
    return data