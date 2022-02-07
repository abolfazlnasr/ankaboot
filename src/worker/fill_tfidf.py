from utils.keyword_extractor import keywords_using_tfidf
from connections.database_connection import get_connection


def fill_tfidf():
    with get_connection() as (cursor, conn):
        stmt = """
                select *
                from crawled_pages
                """
        cursor.execute(stmt)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for result in results:
            page_id = result['id']
            text = result['text']
            kws = keywords_using_tfidf(text)

            stmt = """
                    update crawled_pages
                    set tfidf_kw = %s
                    where id = %s
                    """
            cursor.execute(stmt, (list(kws), page_id))
            conn.commit()

            print(f"{page_id} is done.")


if __name__ == '__main__':
    fill_tfidf()
