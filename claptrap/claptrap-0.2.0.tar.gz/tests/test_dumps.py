import tempfile

import networkx as nx

from claptrap import dumps
from claptrap import phrasegenerator


def test_roundtrip():
    pg = phrasegenerator.GraphPhraseGenerator.from_corpus("hello world hello folks")
    with tempfile.TemporaryDirectory() as tmpdir:
        fn = "somegraph"
        path = tmpdir + "/" + fn
        dumps.dump_word_digraph(pg.digraph, path)
        graph_read = dumps.load_word_digraph(path)
        assert pg.digraph.edges() == graph_read.edges()
