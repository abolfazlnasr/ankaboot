import requests
import re as regex
from bs4 import BeautifulSoup


def crawl(url: str) -> str:
    """
    Get page text
    Remove numbers
    Remove citations
    Remove special characters
    Replace half-space with space
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    page_text = soup.getText()
    page_text = text_cleaner(page_text)

    return page_text


def text_cleaner(text: str) -> str:
    text = regex.sub(r"[۰-۹0-9]", "", text)
    text = regex.sub(r"\[[\u06F0-\u06F90-9]*]", "", text)
    text = regex.sub(r"[\u0021-\u0040\u005b-\u0060\u007b-\u007f•«»↑▼.،٪–]", "", text)
    text = regex.sub(r"[\u200c\u200f\ufeff]", " ", text)

    return text
