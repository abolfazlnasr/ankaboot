from connections.database_connection import get_connection


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def find_similar_pages(keywords: list):
    jaccard_scores = []
    with get_connection() as (cursor, conn):
        stmt = """
        select url, yake_kw || keybert_kw || tfidf_kw as keywords
        from crawled_pages
        """
        cursor.execute(stmt)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for result in results:
            jaccard_score = jaccard_similarity(keywords, result['keywords'])
            if 0.05 < jaccard_score < 1:
                jaccard_scores.append([result['url'], jaccard_score])
        return sorted(jaccard_scores, key=lambda score: score[1], reverse=True)[:3]
