# -*- coding: utf8 -*-
import operator as op
from functools import partial
from dstream import Stream


def test_toList():
    r = Stream([1, 2, 3, 4]).toList()
    assert r == [1, 2, 3, 4]


def test___iter__():
    stream = Stream([1, 2, 3, 4])
    assert hasattr(stream, '__iter__')
    assert [1, 2, 3, 4] == [data for data in stream]


def test_empty():
    r = Stream.empty().toList()
    assert r == []


def test_of_1():
    r = Stream.of().toList()
    assert r == []


def test_of_2():
    r = Stream.of(1, 2, 3).toList()
    assert r == [1, 2, 3]


def test_iterate():
    r = Stream.iterate(0, lambda x: x + 1).limit(3).toList()
    assert r == [0, 1, 2]


def test_generate():
    r = Stream.generate(lambda: 10).limit(3).toList()
    assert r == [10, 10, 10]


def test_concat():
    s1 = Stream([1, 2])
    s2 = Stream([3, 4])
    r = Stream.concat(s1, s2).toList()
    assert r == [1, 2, 3, 4]


def test_filter():
    stream = Stream([1, 2, 3, 4])
    r = stream.filter(lambda x: x % 2 == 0).toList()
    assert r == [2, 4]


def test_map():
    stream = Stream([1, 2, 3, 4])
    r = stream.map(lambda x: x * x).toList()
    assert r == [1, 4, 9, 16]


def test_flatMap():
    stream = Stream([1, 2, 3, 4])
    r = stream.flatMap(lambda x: range(x)).toList()
    assert r == [0, 0, 1, 0, 1, 2, 0, 1, 2, 3]


def test_distinct():
    stream = Stream([1, 1, 2, 3, 2, 4])
    r = stream.distinct().toList()
    assert r == [1, 2, 3, 4]


def test_sorted_1():
    stream = Stream([3, 1, 2, 8, 5, 6])
    r = stream.sorted().toList()
    assert r == [1, 2, 3, 5, 6, 8]


def test_sorted_2():
    stream = Stream([3, 1, 2, 8, 5, 6])
    r = stream.sorted(reverse=True).toList()
    assert r == [8, 6, 5, 3, 2, 1]


def test_sorted_3():
    stream = Stream(['aa', 'bbb', 'c', 'dddd'])
    r = stream.sorted(key=len).toList()
    assert r == ['c', 'aa', 'bbb', 'dddd']


def test_peek():
    tmp = []
    stream = Stream([1, 2, 3])
    r = stream.peek(lambda x: tmp.append(x*x)).toList()
    assert r == [1, 2, 3] and tmp == [1, 4, 9]


def test_limit_1():
    r = Stream([1, 2, 3, 4]).limit(2).toList()
    assert r == [1, 2]


def test_limit_2():
    r = Stream([1, 2, 3, 4]).limit(10).toList()
    assert r == [1, 2, 3, 4]


def test_skip_1():
    r = Stream([1, 2, 3, 4]).skip(2).toList()
    assert r == [3, 4]


def test_skip_2():
    r = Stream([1, 2, 3, 4]).skip(10).toList()
    assert r == []


def test_foreach():
    tmp = []
    stream = Stream([1, 2, 3])
    r = stream.foreach(lambda x: tmp.append(x*x))
    assert tmp == [1, 4, 9]


def test_reduce_1():
    stream = Stream([1, 2, 3])
    r = stream.reduce(lambda x, y: x + y)
    assert r == 6


def test_reduce_2():
    stream = Stream([1, 2, 3])
    r = stream.reduce(lambda x, y: x + y, 10)
    assert r == 16


def test_min():
    stream = Stream([1, 2, 3])
    assert stream.min() == 1


def test_max():
    stream = Stream([1, 2, 3])
    assert stream.max() == 3


def test_count():
    stream = Stream([1, 2, 3, 4])
    assert stream.count() == 4


def test_anyMatch_1():
    stream = Stream([1, 2, 3, 4])
    assert stream.anyMatch(lambda x: x > 3) is True


def test_anyMatch_2():
    stream = Stream([1, 2, 3, 4])
    assert stream.anyMatch(lambda x: x < 0) is False


def test_allMatch_1():
    stream = Stream([1, 2, 3, 4])
    assert stream.allMatch(lambda x: x > 0) is True


def test_allMatch_2():
    stream = Stream([1, 2, 3, 4])
    assert stream.allMatch(lambda x: x < 4) is False


def test_noneMatch_1():
    stream = Stream([1, 2, 3, 4])
    assert stream.noneMatch(lambda x: x > 10) is True


def test_noneMatch_1():
    stream = Stream([1, 2, 3, 4])
    assert stream.noneMatch(lambda x: x < 2) is False


def test_first():
    stream = Stream([1, 2, 3, 4])
    assert stream.first() == 1
