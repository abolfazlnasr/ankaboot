import uvicorn
from fastapi import FastAPI
from utils.crawler import crawl
from starlette.responses import FileResponse
from utils.similar_pages import find_similar_pages
from starlette.middleware.cors import CORSMiddleware
from utils.word_cloud import create_wordcloud_from_text
from connections.database_connection import get_connection
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


@app.post("/api")
def index(method: str, url: str):
    global crawled_text, crawled_url
    crawled_url = url
    crawled_text = crawl(url)
    kws = []

    if method == "tfidf":
        kws = keywords_using_tfidf(crawled_text)
        save_to_db(url, crawled_text, [], [], kws)

    elif method == "yake":
        kws = keywords_using_yake(crawled_text)
        save_to_db(url, crawled_text, kws)

    elif method == "keybert":
        kws = keywords_using_keybert(crawled_text)()
        save_to_db(url, crawled_text, [], kws)

    return {
        "keywords": kws,
        "similar_pages": find_similar_pages(kws)
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
