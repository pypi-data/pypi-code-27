import collections
import gzip
import pkg_resources
import random

import networkx as nx

from . import backports
from . import dumps
from .munging import gen_words
from .serializer import deserialize_digraph


IGNORE = {
    "ii",
    "iii",
    "iv",
    "v",
    "vi",
    "vii",
    "viii",
    "ix",
    "x",
    "xi",
    "xii",
    "chapter",
    "gutenberg",
}

PACKAGE = __name__.split(".", 1)[0]
CORPUS_PATH = ["data"]


# def from_corpus(cls, corpus, threshold=1000):
#     counter = collections.Counter(corpus)
#     words = [
#         word
#         for word, count
#         in counter.most_common(threshold)
#         if word.lower() not in IGNORE
#     ]
#     sparse = mat_to_sparse(matgen(words, corpus))
#     return cls(words, sparse)


def from_corpus(text):
    words = list(gen_words(text=text))
    # word_count = collections.Counter(words)

    iwords = iter(words)
    prev = next(iwords)
    G = nx.DiGraph()
    for word in iwords:
        if G.has_edge(prev, word):
            G[prev][word]["weight"] += 1
        else:
            G.add_edge(prev, word, weight=1)
        prev = word
    return G


def pick_random_node(G):
    index = random.randrange(len(G))
    for n, node in enumerate(G.nodes()):
        if n == index:
            return node


def weighted_next(G, source):
    if not len(G[source]):
        return pick_random_node(G)
    # print(source, G[source].values())
    nodes, weights = zip(*((e.get("id", k), e["weight"]) for k, e in G[source].items()))
    return backports.choices(nodes, weights)[0]


class GraphPhraseGenerator:
    @classmethod
    def from_corpus(cls, text):
        return cls(from_corpus(text))
        # words = list(gen_words(text=text))
        # # word_count = collections.Counter(words)

        # iwords = iter(words)
        # prev = next(iwords)
        # G = nx.DiGraph()
        # for word in iwords:
        #     if G.has_edge(prev, word):
        #         G[prev][word]['weight'] += 1
        #     else:
        #         G.add_edge(prev, word, weight=1)
        #     prev = word
        # return cls(G)

    @classmethod
    def from_resource(cls, name):
        corpus_path = "/".join(CORPUS_PATH + ["{}.claptrap.gz".format(name)])
        graph_dump = pkg_resources.resource_stream(PACKAGE, corpus_path)

        data = gzip.decompress(graph_dump.read())
        G = deserialize_digraph(data)
        return cls(G)

    @classmethod
    def from_file(cls, fn):
        cls(dumps.load_word_digraph(fn))

    def __init__(self, digraph):
        self.digraph = digraph
        self._walker = self._walk()

    def _walk(self):
        node = pick_random_node(self.digraph)
        while True:
            yield node
            node = weighted_next(self.digraph, node)

    def phrase(self, length=(60, 100)):
        try:
            min_len, max_len = length
        except TypeError:
            min_len = max_len = length
        if min_len > max_len:
            raise ValueError("Minimum length must be smaller than the maximum length")
        if min_len < 1:
            raise ValueError("Length must be positive")

        accum = ""
        while not accum.isalpha():
            accum = next(self._walker).title()

        term = False
        while len(accum) < min_len:
            word = next(self._walker)
            if word in set(".!?;,:"):
                accum += word
                if word in set(".!?"):
                    term = True
            else:
                if term:
                    word = word.title()
                    term = False
                accum += " " + word

        accum = accum[:max_len]
        if accum[-1] == " ":
            return accum[:-1] + random.choice(".!?s")
        return accum

    def save(self, fn):
        dumps.dump_word_digraph(self.digraph, fn)
