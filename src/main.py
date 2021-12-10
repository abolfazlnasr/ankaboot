from crawler import crawl
from fastapi import FastAPI
from starlette.responses import FileResponse
from word_cloud import create_wordcloud_from_text
from keyword_extractor import keywords_using_keybert, keywords_using_yake

extracted_words = []
default_url = "https://fa.wikipedia.org/wiki/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87%E2%80%8C%D9%86" \
              "%D9%88%DB%8C%D8%B3%DB%8C_%D8%B1%D8%A7%DB%8C%D8%A7%D9%86%D9%87%E2%80%8C%D8%A7%DB%8C "

app = FastAPI()


@app.get("/")
def index():
    return extracted_words


@app.post("/crawl")
def crawl_page(url=default_url):
    global extracted_words
    extracted_words = crawl(url)
    return True


@app.get("/word_cloud")
def show_word_cloud():
    text = " ".join(extracted_words)
    create_wordcloud_from_text(text)
    return FileResponse("img/result.png")


@app.get("/keybert")
def show_keywords_using_keybert():
    text = " ".join(extracted_words)
    return keywords_using_keybert(text)


@app.get("/yake")
def show_keywords_using_yake():
    text = " ".join(extracted_words)
    return keywords_using_yake(text)
