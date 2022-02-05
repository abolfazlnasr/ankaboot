import hazm
from psycopg2.extras import Json
from connections.database_connection import get_connection


def update_df_model():
    data = get_df_and_docs_count()
    save_to_db(data['df'], data['docs_count'])


def get_df_and_docs_count():
    df = {}
    with get_connection() as (cursor, conn):
        stmt = """
                select text
                from crawled_pages
                """
        cursor.execute(stmt)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        docs_count = len(results)
        for result in results:
            word_set = []
            doc_text = result['text']
            doc_text = doc_text.replace(u'\xa0', u' ')  # clean non-breaking spaces
            doc_words = [word.lower() for word in hazm.word_tokenize(doc_text) if len(word) > 1]

            for word in doc_words:
                if word not in word_set:
                    word_set.append(word)

            for unique_word in word_set:
                if unique_word in df:
                    df[unique_word] += 1
                else:
                    df[unique_word] = 1

        return {
            "df": df,
            "docs_count": docs_count
        }


def save_to_db(df: dict, docs_count):
    with get_connection() as (cursor, conn):
        stmt = """
            INSERT INTO df_models(df, docs_count)
            VALUES(%s, %s)
            """
        cursor.execute(stmt, (Json(df), docs_count))
        conn.commit()


if __name__ == '__main__':
    update_df_model()
