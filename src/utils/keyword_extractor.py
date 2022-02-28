import yake
import math
import hazm
from utils.models import DF
from keybert import KeyBERT


def keywords_using_keybert(text: str):
    keywords = []
    # kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    kw_extractor = KeyBERT()
    for kw in kw_extractor.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=[]):
        keywords.append(kw[0])
    return keywords


def keywords_using_yake(text: str):
    keywords = []
    kw_extractor = yake.KeywordExtractor(n=1)
    for kw in kw_extractor.extract_keywords(text):
        keywords.append(kw[0])
    return keywords


def get_idf(word: str):
    df = 1

    df_data = DF.get_df()
    df_model = df_data['df_model']
    docs_count = df_data['docs_count']

    if word in df_model.items():
        df += df_model[word]

    return math.log(docs_count / df)


def keywords_using_tfidf(text: str):
    words_dict = {}
    words = [word.lower() for word in hazm.word_tokenize(text) if len(word) > 1]
    words = [word for word in words if word not in hazm.stopwords_list()]

    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1

    tf = {key: value / len(words_dict) for key, value in words_dict.items()}
    tfidf = {}

    for word in tf:
        tfidf[word] = tf[word] * get_idf(word)

    return list({k: v for k, v in sorted(tfidf.items(), key=lambda item: item[1], reverse=True)})[:6]
