import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import logging

logging.basicConfig(
    filename="uploader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def upload_to_gsheet(df, sheet_id):
    """Uploads df to Google Sheet."""
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(sheet_id).sheet1
        sheet.clear()

        set_with_dataframe(sheet, df)
        logging.info("Upload successful.")
    except Exception as e:
        logging.error(f"Upload error: {e}")
        raise
