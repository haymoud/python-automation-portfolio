import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BASE_URL = "https://books.toscrape.com/"


def fetch_page(url):
    """Downloads page HTML with error handling."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url} : {e}")
        return None


def clean_price(raw_price):
    """
    Clean price values like '£51.77'
    → convert to float using regex.
    """
    try:
        clean = re.sub(r"[^\d.]", "", raw_price)  # remove currency
        return float(clean)
    except Exception:
        return None


def scrape_books(limit=30):
    """Scrapes the first few books with cleaning."""
    results = []

    try:
        html = fetch_page(BASE_URL)
        if not html:
            logging.error("No HTML fetched.")
            return pd.DataFrame()

        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".product_pod")

        for item in items[:limit]:
            try:
                title = item.h3.a["title"]
                raw_price = item.select_one(".price_color").text.strip()

                price = clean_price(raw_price)

                availability = item.select_one(".availability").text.strip()

                # Regex cleaning of availability
                availability = re.sub(r"\s+", " ", availability)

                results.append({
                    "Title": title,
                    "Price": price,
                    "Availability": availability
                })

            except Exception as e:
                logging.error(f"Error parsing item: {e}")
                continue

        return pd.DataFrame(results)

    except Exception as e:
        logging.error(f"General scraping error: {e}")
        return pd.DataFrame()
