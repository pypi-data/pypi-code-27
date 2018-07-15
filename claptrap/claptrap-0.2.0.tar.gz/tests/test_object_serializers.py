import itertools

import networkx as nx

from claptrap.serializer import (
    deserialize_adjd,
    deserialize_digraph,
    serialize_adjd,
    serialize_digraph,
)


def assert_fragment(it, fragment):
    assert fragment == bytes(itertools.islice(it, len(fragment)))


def test_serialize_adjd():
    nodes = [{"id": "x"}, {"id": "y"}]
    adj = [[{"id": "y", "weight": 2}], [{"id": "x", "weight": 3}], []]
    g = {"nodes": nodes, "adjacency": adj, "multigraph": False, "directed": True}
    git = iter(serialize_adjd(g))

    assert_fragment(git, b"\x02\x01x\x01y")  # nodes
    assert_fragment(git, b"\x01\x02\x01\x02")  # node x adjacency
    assert_fragment(git, b"\x01\x02\x00\x03")  # node y adjacency
    assert_fragment(git, b"\x00\x00")  # node z adjacency
    assert next(git, None) is None  # should be exhausted


def test_serialize_adjd2():
    nodes = [{"id": "x"}, {"id": "y"}, {"id": "zz"}]
    adj = [
        [{"id": "y", "weight": 2}, {"id": "zz", "weight": 0x44}],
        [{"id": "x", "weight": 3}, {"id": "zz", "weight": 0x55}],
    ]
    g = {"nodes": nodes, "adjacency": adj, "multigraph": False, "directed": True}
    git = iter(serialize_adjd(g))
    #     gb = serialize_adjd(g)
    assert_fragment(git, b"\x03\x01x\x01y\x02zz")  # nodes
    assert_fragment(git, b"\x02\x02\x01\x02\x02\x44")  # node x adjacency
    assert_fragment(git, b"\x02\x02\x00\x03\x02\x55")  # node y adjacency
    assert next(git, None) is None  # should be exhausted


def test_deserialize_adjd():
    nodes = [{"id": "x"}, {"id": "y"}]
    adj = [[{"id": "y", "weight": 2}], [{"id": "x", "weight": 3}]]
    g = {"nodes": nodes, "adjacency": adj, "multigraph": False, "directed": True}

    bit = iter(
        b"\x02\x01x\x01y"
        + b"\x01\x02\x01\x02"  # nodes
        + b"\x01\x02\x00\x03"  # node x adjacency
    )  # node y adjacency

    G = deserialize_adjd(bit)
    assert next(bit, None) is None  # should be exhausted

    assert G["nodes"] == nodes
    assert G["adjacency"] == adj, G["adjacency"]


#     assert set(G.edges()) ==


def test_deserialize_adjd2():
    nodes = [{"id": "x"}, {"id": "y"}, {"id": "z"}]
    adj = [
        [{"id": "y", "weight": 2}, {"id": "z", "weight": 0x44}],
        [{"id": "x", "weight": 3}, {"id": "z", "weight": 0x55}],
        [],
    ]
    g = {"nodes": nodes, "adjacency": adj, "multigraph": False, "directed": True}

    bit = iter(
        b"\x03\x01x\x01y\x01z"
        + b"\x02\x02\x01\x02\x02\x44"  # nodes
        + b"\x02\x02\x00\x03\x02\x55"  # node x adjacency
        + b"\x00\x00"  # node y adjacency  # node z adjacency
    )
    G = deserialize_adjd(bit)
    assert next(bit, None) is None  # should be exhausted

    assert G["nodes"] == nodes
    assert G["adjacency"] == adj


def test_round_trip():
    G = nx.DiGraph()
    G.add_edge("aardvark", "bear", weight=2)
    G.add_edge("bear", "chicken", weight=4)
    G.add_edge("bear", "aardvark", weight=421)
    G.add_edge("chicken", "aardvark", weight=12349)

    Gr = deserialize_digraph(serialize_digraph(G))

    assert G.nodes() == Gr.nodes()
    assert G.edges() == Gr.edges()
