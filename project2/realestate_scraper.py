import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import logging

logging.basicConfig(
    filename="realestate_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = "https://www.scrapethissite.com/pages/forms/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def clean_text(text):
    if not text:
        return None
    return re.sub(r"\s+", " ", text).strip()


def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        logging.error(f"Fetch error: {e}")
        return None


def scrape_properties():
    html = fetch_page(URL)
    if not html:
        logging.error("HTML not fetched")
        return pd.DataFrame()

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select(".team")
    if not cards:
        logging.error("No cards found — selector may be wrong")
        return pd.DataFrame()

    data = []

    for c in cards:
        try:
            title = clean_text(c.select_one(".name").text)
            location = clean_text(c.select_one(".year").text)
            price = clean_text(c.select_one(".wins").text)
            details = clean_text(c.select_one(".losses").text)

            data.append({
                "Title": title,
                "Price": price,
                "Location": location,
                "Details": details
            })

        except Exception as e:
            logging.error(f"Item parsing error: {e}")
            continue

    return pd.DataFrame(data)
