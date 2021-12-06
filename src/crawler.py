import requests
import re as regex
from bs4 import BeautifulSoup


def crawl(url: str) -> list:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    page_text = soup.getText()
    page_text = regex.sub(r"\[[\u06F0-\u06F90-9]*]", "", page_text)  # Remove citations
    page_text = regex.sub(r"[\u0021-\u007f•«»↑▼.،٪–]", " ", page_text)  # Remove special characters
    page_text = regex.sub(r"[\u200c\u200f\ufeff]", " ", page_text)  # Replace half-space with space
    page_words = page_text.split()
    return page_words
