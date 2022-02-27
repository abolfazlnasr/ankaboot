import networkx as nx
from matplotlib import pyplot as plt
from utils.similar_pages import jaccard_similarity
from utils.keyword_extractor import keywords_using_tfidf


def similarity_matrix(pages: dict) -> dict:
    matrix = {}
    kws_list = [keywords_using_tfidf(text[1]) for text in pages.items()]
    urls = list(pages)

    for i, (url, text) in enumerate(pages.items()):
        sims = []
        for j, kws in enumerate(kws_list):
            if i != j:
                jaccard_score = jaccard_similarity(kws_list[i], kws_list[j])
                if 0.05 < jaccard_score < 1:
                    sims.append(urls[j])
        matrix[url] = sims

    return matrix


def network_graph(matrix: dict):
    edges = []
    for origin, aim in matrix.items():
        edges.append((origin, aim[0]))

    graph = nx.Graph()
    graph.add_edges_from(edges)
    nx.draw(graph, cmap=plt.get_cmap('jet'), with_labels=True)
    plt.savefig("img/graph.png", format="PNG")
