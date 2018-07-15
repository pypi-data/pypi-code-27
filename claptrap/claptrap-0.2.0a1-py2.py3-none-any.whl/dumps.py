try:
    from contextlib import suppress
except ImportError:
    from .backports import suppress
import importlib

from .serializer import deserialize_digraph, serialize_digraph


COMPRESSORS = {lib: None for lib in ["gzip", "bz2", "lzma"]}
for lib in COMPRESSORS:
    with suppress(ImportError):
        COMPRESSORS[lib] = importlib.import_module(lib)


COMPRESSED_EXTS = {"gz": "gzip", "bz2": "bz2", "xz": "lzma", "lzma": "lzma"}


def opener(fn, *args, **kwargs):
    final_ext = fn.rsplit(".")[-1]
    if final_ext in COMPRESSED_EXTS:
        compressor = COMPRESSED_EXTS[final_ext]
        compressor_lib = COMPRESSORS.get(compressor, None)
        if compressor_lib is None:
            raise RuntimeError('could not import library "{}"'.format(compressor))
        return compressor_lib.open(fn, *args, **kwargs)
    return open(fn, *args, **kwargs)


def dump_word_digraph(G, filename):
    dump = serialize_digraph(G)
    with opener(filename, "wb") as f:
        f.write(dump)


def load_word_digraph(filename):
    with opener(filename, "rb") as f:
        dump = f.read()
    G = deserialize_digraph(dump)
    return G
