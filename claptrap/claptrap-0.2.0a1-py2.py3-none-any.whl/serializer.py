import itertools

from networkx.readwrite import json_graph


def pump(type_):
    """
    Feed the generator into *type_* til exhaustion. Can be overridden by
    setting exhaust=False.
    """

    def _pump(f):
        def fx(*args, **kwargs):
            exhaust_gen = kwargs.pop("exhaust", True)
            gen = f(*args, **kwargs)
            if exhaust_gen:
                return type_(gen)
            return gen

        return fx

    return _pump


@pump(bytes)
def pack_intarr_2d(arr):
    rows = len(arr)
    if rows == 0:
        yield from b"\x00\x00"
        return
    yield from pack_varuint(rows)
    cols = len(arr[0])
    yield from pack_varuint(cols)
    for row in arr:
        if len(row) != cols:
            raise ValueError("jagged array")
        for element in row:
            yield from pack_varuint(element)


def pack_str(s):
    b = s.encode("utf-8")
    return bytes([len(b)]) + bytes(b)


@pump(bytes)
def pack_strarr(strs):
    yield from pack_varuint(len(strs))
    for s in strs:
        yield from pack_str(s)


def pack_varuint(n):
    if n < 0:
        raise ValueError("value must be non-negative")
    packed = [n & 0x7F]
    n >>= 7
    while n > 0:
        packed.insert(0, 0x80 | (n & 0x7F))
        n >>= 7

    return packed


@pump(list)
def unpack_intarr_2d(byteiter):
    byteiter = iter(byteiter)
    rows = unpack_varuint(byteiter)
    cols = unpack_varuint(byteiter)
    for row in range(rows):
        yield [unpack_varuint(byteiter) for _ in range(cols)]


def unpack_str(byteiter):
    byteiter = iter(byteiter)
    n = next(byteiter)
    b = bytes(itertools.islice(byteiter, n))
    return b.decode("utf-8")


@pump(list)
def unpack_strarr(byteiter):
    byteiter = iter(byteiter)
    n = unpack_varuint(byteiter)
    for _ in range(n):
        yield unpack_str(byteiter)


def unpack_varuint(byteiter):
    n = 0
    for byte in byteiter:
        n <<= 7
        n += byte & 0x7F
        if not (byte & 0x80):
            return n
    raise ValueError("byte iterator exhausted")


def serialize_digraph(G):
    adjd = json_graph.adjacency_data(G)
    return serialize_adjd(adjd)


@pump(bytes)
def serialize_adjd(adjd):
    if not adjd["directed"] or adjd["multigraph"]:
        raise ValueError("only supports directed simple graphs")

    nodes = [n["id"] for n in adjd["nodes"]]
    lookup = {nodeword: n for n, nodeword in enumerate(nodes)}

    yield from pack_strarr(nodes)

    for adj in adjd["adjacency"]:
        node_adj = [[lookup[edge["id"]], edge["weight"]] for edge in adj]
        yield from pack_intarr_2d(node_adj)


def deserialize_digraph(byteiter):
    data = deserialize_adjd(byteiter)
    return json_graph.adjacency_graph(data)


def deserialize_adjd(byteiter):
    byteiter = iter(byteiter)
    nodes = unpack_strarr(byteiter)

    adjd = []
    for node in nodes:
        adj = unpack_intarr_2d(byteiter)
        adjd.append([{"id": nodes[id_], "weight": weight} for id_, weight in adj])

    data = {
        "directed": True,
        "multigraph": False,
        "nodes": [{"id": n} for n in nodes],
        "adjacency": adjd,
    }
    return data
