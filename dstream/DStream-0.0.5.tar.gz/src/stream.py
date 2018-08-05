# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import reduce


def _infinity():
    while True:
        yield None


_INF = _infinity()


class Stream:
    def __init__(self, iterable):
        if not hasattr(iterable, '__iter__'):
            raise TypeError('The argument must be iterable.')
        self.stream = iterable

    def __iter__(self):
        return self.stream.__iter__()

    @classmethod
    def empty(cls):
        return cls([])

    @classmethod
    def of(cls, *elements):
        return cls(elements)

    # 迭代
    @classmethod
    def iterate(cls, initial, func):
        def g():
            val = initial
            while True:
                yield val
                val = func(val)
        return cls(g())

    # 生成
    @classmethod
    def generate(cls, func):
        return cls(func() for _ in _INF)

    # 连接
    @classmethod
    def concat(cls, stream1, stream2):
        def g():
            for data in stream1:
                yield data
            for data in stream2:
                yield data
        return cls(g())

    # 过滤
    def filter(self, func):
        self.stream = (data for data in self.stream if func(data))
        return self

    # 映射
    def map(self, func):
        self.stream = (func(data) for data in self.stream)
        return self

    def flatMap(self, func):
        self.stream = (data for data0 in self.stream for data in func(data0))
        return self

    # 保证元素的唯一性
    def distinct(self):
        stream = self.stream
        passed = []

        def g():
            for data in stream:
                if data not in passed:
                    passed.append(data)
                    yield data
        self.stream = g()
        return self

    # 将流中的元素排序
    def sorted(self, key=None, reverse=False):
        self.stream = sorted(self.stream, key=key, reverse=reverse)
        return self

    def peek(self, func):
        self.stream = (data for data in self.stream if func(data) or True)
        return self

    # 限制最多n个元素
    def limit(self, n):
        stream = self.stream

        def g(n):
            for data in stream:
                if not n:
                    break
                n -= 1
                yield data
        self.stream = g(n)
        return self

    # 跳过n个元素
    def skip(self, n):
        self.stream = (data for idx, data in enumerate(
            self.stream) if idx >= n)
        return self

    # 在每个元素上执行一个操作
    def foreach(self, func):
        for data in self.stream:
            func(data)

    # 收集流中的元素，得到一个列表
    # TODO
    def toList(self):
        return [data for data in self.stream]

    # 规约
    def reduce(self, func, initial=None):
        return reduce(func, self.stream) if initial is None else reduce(func, self.stream, initial)

    # TODO
    def collect(self):
        raise NotImplementedError

    # 最小值
    def min(self):
        return min(self.stream)

    # 最大值
    def max(self):
        return max(self.stream)

    # 获取元素的个数
    def count(self):
        return self.reduce(lambda x, y: x + 1, 0)

    def anyMatch(self, func):
        for data in self.stream:
            if func(data):
                return True
        return False

    def allMatch(self, func):
        for data in self.stream:
            if not func(data):
                return False
        return True

    def noneMatch(self, func):
        for data in self.stream:
            if func(data):
                return False
        return True

    def first(self):
        for data in self.stream:
            return data

    # 打印最多n个元素到控制台
    def show(self, n=100):
        for data in self.stream:
            print(data)
