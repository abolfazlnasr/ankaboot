import os
import uvicorn
from typing import List
from fastapi import FastAPI
from utils.crawler import crawl
from utils.summarizer import summarize_text
from starlette.responses import FileResponse
from utils.similar_pages import find_similar_pages
from starlette.middleware.cors import CORSMiddleware
from utils.word_cloud import create_wordcloud_from_text
from connections.database_connection import get_connection
from utils.similarity_graph import similarity_matrix, network_graph
from utils.keyword_extractor import keywords_using_keybert, keywords_using_yake, keywords_using_tfidf

crawled_text = ""
crawled_url = ""

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)


def save_to_db(url, text, yake=[], keybert=[], tfidf=[]):
    with get_connection() as (cursor, conn):
        stmt = """
        select * from crawled_pages
        where url like %s
        """
        cursor.execute(stmt, (url,))
        result = cursor.fetchone()
        if result:
            stmt = """
            update crawled_pages
            set tfidf_kw = %s
            where url like %s
            """
            cursor.execute(stmt, (list(tfidf), url))
            conn.commit()
        else:
            stmt = """
            insert into crawled_pages (url, text, yake_kw, keybert_kw, tfidf_kw)
            values (%s, %s, %s, %s, %s)
            """
            cursor.execute(stmt, (url, text, yake, keybert, tfidf))
            conn.commit()

    return True


@app.get("/word_cloud")
def get_word_cloud():
    create_wordcloud_from_text(crawled_text)
    return FileResponse("img/result.png")


@app.get("/similarity_graph")
def get_word_cloud():
    return FileResponse("img/graph.png")


@app.post("/api/similarity_graph")
def get_similarity_graph(urls: List[str]):
    pages = {url: crawl(url) for url in urls}
    network_graph(similarity_matrix(pages))
    pages.clear()

    return True


@app.post("/api/tfidf")
def index_tfidf(url: str):
    global crawled_text, crawled_url
    crawled_url = url
    crawled_text = crawl(url)

    kws = keywords_using_tfidf(crawled_text)
    # save_to_db(url, crawled_text, [], [], kws)

    return {
        "keywords": kws,
        # "similar_pages": find_similar_pages(kws),
        "summary": summarize_text(crawled_text)
    }


@app.post("/api/keybert")
def index_keyebrt(url: str):
    global crawled_text, crawled_url
    crawled_url = url
    crawled_text = crawl(url)

    kws = keywords_using_keybert(crawled_text)
    # save_to_db(url, crawled_text, [], kws)

    return {
        "keywords": kws,
        # "similar_pages": find_similar_pages(kws),
        "summary": summarize_text(crawled_text)
    }


@app.post("/api/yake")
def index(url: str):
    global crawled_text, crawled_url
    crawled_url = url
    crawled_text = crawl(url)

    kws = keywords_using_yake(crawled_text)
    # save_to_db(url, crawled_text, kws)

    return {
        "keywords": kws,
        # "similar_pages": find_similar_pages(kws),
        "summary": summarize_text(crawled_text)
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
