import yake
from keybert import KeyBERT


def keywords_using_keybert(text):
    kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    keywords = kw_extractor.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=[])
    return keywords


def keywords_using_yake(text):
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    return keywords
