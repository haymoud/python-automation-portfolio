from scraper import scrape_books
from uploader import upload_to_gsheet

# Your Google Sheet ID here
SHEET_ID = "19lpSWCeKGW5ymdg0Zvh9renvk4JoMLxtPW7H4Lx5sD4"

def run_pipeline():
    print("Scraping website...")
    df = scrape_books(limit=40)

    if df.empty:
        print("Scraping failed. Check logs.")
        return
    
    print("Uploading to Google Sheets...")
    upload_to_gsheet(df, SHEET_ID)

    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
