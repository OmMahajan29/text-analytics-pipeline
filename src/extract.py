# extract.py
# Handles downloading a web page and extracting only the article title and body text,
# then saving that into Text/<URL_ID>.txt.

import os
import time
import random
import requests
from bs4 import BeautifulSoup

# Where to save article .txt files
TEXT_DIR = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Text"

# Realistic browser-like headers to reduce chances of being blocked (406/403)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive"
}

def fetch_and_clean_article(url):
    """
    Fetch the page at `url`, parse out the article's title and main body,
    and return the clean text. Returns None on fetch errors.
    """
    try:
        # Use a session to preserve cookies; can help with some sites
        session = requests.Session()
        r = session.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        # Set a reasonable encoding guess to prevent empty/garbled text
        r.encoding = r.apparent_encoding
    except Exception as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None

    # Parse HTML
    soup = BeautifulSoup(r.text, "lxml")

    # Remove non-content elements we never want to include
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.extract()

    # Typical WordPress article title and content container
    title_tag = soup.find("h1")
    content_div = soup.find("div", class_="td-post-content")

    # Prefer the known article container; otherwise fall back to all <p> paragraphs
    if content_div:
        paras = content_div.find_all("p")
    else:
        paras = soup.find_all("p")

    # Extract visible paragraph text, skipping empties
    text_blocks = [p.get_text(" ", strip=True) for p in paras if p.get_text(strip=True)]
    title = title_tag.get_text(" ", strip=True) if title_tag else ""

    # Combine title and paragraphs; strip extra whitespace
    full_text = (title + "\n" + "\n".join(text_blocks)).strip()

    # Gentle delay to avoid rate-limiting
    time.sleep(random.uniform(0.8, 1.5))
    return full_text

def save_article_text(url_id, text):
    """
    Save the article `text` to Text/<URL_ID>.txt.
    Creates the Text directory if needed. Writes empty string if text is None.
    """
    os.makedirs(TEXT_DIR, exist_ok=True)
    filepath = os.path.join(TEXT_DIR, f"{url_id}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text if text else "")
