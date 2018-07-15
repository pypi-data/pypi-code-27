import itertools

from claptrap.serializer import (
    pack_intarr_2d,
    pack_str,
    pack_strarr,
    pack_varuint,
    unpack_intarr_2d,
    unpack_str,
    unpack_strarr,
    unpack_varuint,
)


def test_unpack_varuint():
    assert unpack_varuint(b"\x00") == 0
    assert unpack_varuint(b"\x00\x00") == 0
    assert unpack_varuint(b"\x81\x00") == unpack_varuint(b"\x81\x00\x00") == 128

    bi = iter(b"\x00\x00")
    assert unpack_varuint(bi) == 0
    assert unpack_varuint(bi) == 0


def test_packunpack_varuint():
    big = 1234567890212345678902345432
    nums = itertools.chain(
        range(10000),
        range(0x3FF0, 0x400F),
        range(0x1FFFF0, 0x20000F),
        range(big, big + 1234),
    )
    for n in nums:
        packed = pack_varuint(n)
        assert n == unpack_varuint(packed)
        assert not (packed[-1] & 0x80)
        assert all(px & 0x80 for px in packed[:-1])


def test_packunpack_str():
    for word in itertools.__doc__.split():
        unpack_str(pack_str(word)) == word


def test_pack_strarr():
    assert pack_strarr([]) == b"\x00"
    assert (
        # "\U0001F984" = "\N{UNICORN FACE}" (3.3 doesn't like the name)
        pack_strarr(["hey", "there", "\U0001F984"])
        == b"\x03\x03hey\x05there\x04\xf0\x9f\xa6\x84"
    )


def test_unpack_strarr():
    assert unpack_strarr(b"\x00") == []
    assert unpack_strarr(b"\x01\x01x") == ["x"]
    assert unpack_strarr(b"\x01\x01x" + bytes(100)) == ["x"]


def test_packunpack_strarr():
    def pup(x):
        return unpack_strarr(pack_strarr(x))

    a1 = ["x"] * 10000
    assert pup(a1) == a1

    # x = ord("\N{SLIGHTLY SMILING FACE}")
    x = ord("\U0001F642")
    emojis = [chr(n) for n in range(x, x + 130)]
    assert pup(emojis) == emojis


def test_pack_intarr():
    assert pack_intarr_2d([]) == b"\x00\x00"
    assert pack_intarr_2d([[]]) == b"\x01\x00"
    assert pack_intarr_2d([[], []]) == b"\x02\x00"
    assert pack_intarr_2d([[1]]) == bytes([1] * 3)
    assert pack_intarr_2d([[2, 2], [2, 2]]) == bytes([2] * 6)
    assert pack_intarr_2d([[3] * 3] * 3) == bytes([3] * 11)


def test_pack_intarr_bad():
    try:
        pack_intarr_2d([1, 2])
    except (TypeError, ValueError):
        pass
    else:
        assert False, "allowed bad array"

    try:
        pack_intarr_2d([[1], [2, 2]])
    except (TypeError, ValueError):
        pass
    else:
        assert False, "allowed bad array"


def test_unpack_intarr():
    assert unpack_intarr_2d(b"\x00\x00") == []
    assert unpack_intarr_2d(b"\x01\x00") == [[]]
    assert unpack_intarr_2d(b"\x02\x00") == [[], []]

    assert unpack_intarr_2d(b"\x01\x01\x0F") == [[15]]
    assert unpack_intarr_2d(bytes([2, 2, 1, 2, 3, 4])) == [[1, 2], [3, 4]]
    assert unpack_intarr_2d(bytes([1, 2, 3, 4, 5, 6])) == [[3, 4]]

    byteiter = iter(bytes([1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]))
    assert unpack_intarr_2d(byteiter) == [[3, 1]]
    assert unpack_intarr_2d(byteiter) == [[1, 2, 3], [1, 2, 3]]
    assert unpack_intarr_2d(byteiter) == [[3, 1]]
