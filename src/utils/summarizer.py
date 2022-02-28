from heapq import nlargest
from collections import defaultdict
from nltk.probability import FreqDist
from hazm import stopwords_list, sent_tokenize, word_tokenize


def summarize_text(text: str):
    sents = sent_tokenize(text)
    size = int(len(sents) / 5)
    word_sent = word_tokenize(text)
    word_sent = [word for word in word_sent if word not in stopwords_list()]
    freq = FreqDist(word_sent)
    ranking = defaultdict(int)

    for i, sent in enumerate(sents):
        sent_words = word_tokenize(sent)
        for w in sent_words:
            if w in freq:
                ranking[i] += freq[w]
        ranking[i] /= len(sent_words)

    sents_idx = nlargest(size, ranking, key=ranking.get)

    return " ".join([sents[j] for j in sorted(sents_idx)])
