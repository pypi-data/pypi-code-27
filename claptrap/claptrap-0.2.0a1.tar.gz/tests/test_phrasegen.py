from claptrap import phrasegenerator as pg


def test_fromcorpus():
    text = "hello there what is up"
    G = pg.from_corpus(text)

    assert len(G.edges()) == 4
    assert len(G.nodes()) == 5


def test_phrasegen():
    text = "hello folks hello world"
    phrasegen = pg.GraphPhraseGenerator.from_corpus(text)

    phrasegen.phrase()
