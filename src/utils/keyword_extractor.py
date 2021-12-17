import yake
import math
from keybert import KeyBERT
from connections.database_connection import get_connection


def keywords_using_keybert(text: str):
    keywords = []
    kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    for kw in kw_extractor.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=[]):
        keywords.append(kw[0])
    return keywords


def keywords_using_yake(text: str):
    keywords = []
    kw_extractor = yake.KeywordExtractor()
    for kw in kw_extractor.extract_keywords(text):
        keywords.append(kw[0])
    return keywords


def get_idf(word: str):
    df = 1
    with get_connection() as (cursor, conn):
        stmt = """
        select url, text
        from crawled_pages
        """
        cursor.execute(stmt)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for result in results:
            words = result['text'].split()
            if word in words:
                df += 1
        return math.log(len(results) / df)


def keywords_using_tfidf(text: str):
    words_dict = {}
    words = text.split()
    for word in words:
        word = word.lower()
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1
    tf = {k: v / len(words_dict) for k, v in words_dict.items()}
    for word in tf:
        tf[word] = tf[word] * get_idf(word)
    return list({k: v for k, v in sorted(tf.items(), key=lambda item: item[1], reverse=True)})[:6]
