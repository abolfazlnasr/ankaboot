import crawler
from fastapi import FastAPI

extracted_words = []
default_url = "https://fa.wikipedia.org/wiki/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87%E2%80%8C%D9%86" \
              "%D9%88%DB%8C%D8%B3%DB%8C_%D8%B1%D8%A7%DB%8C%D8%A7%D9%86%D9%87%E2%80%8C%D8%A7%DB%8C "

app = FastAPI()


@app.get("/")
def index():
    return extracted_words


@app.post("/crawl")
def index(url=default_url):
    global extracted_words
    extracted_words = crawler.crawl(url)
    return True
