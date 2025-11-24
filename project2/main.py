from realestate_scraper import scrape_properties
from uploader import upload_to_gsheet

SHEET_ID = "19lpSWCeKGW5ymdg0Zvh9renvk4JoMLxtPW7H4Lx5sD4"


def run_pipeline():
    print("Scraping property-style listings...")
    df = scrape_properties()

    if df.empty:
        print("No data scraped — check logs.")
        return

    print("Uploading to Google Sheets...")
    upload_to_gsheet(df, SHEET_ID)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
