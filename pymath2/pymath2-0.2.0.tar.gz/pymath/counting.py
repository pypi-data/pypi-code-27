from math import factorial
from typing import Collection, Iterator, List, TypeVar

T = TypeVar('T')


def C(n: int, k: int) -> int:
    return factorial(n)//(factorial(n-k)*factorial(k))


def P(n: int, k: int) -> int:
    return factorial(n)//(factorial(n-k))


def powerset(collection: Collection[T]) -> Iterator[List[T]]:
    def powerset_impl(seq):
        if len(seq) == 0:
            yield []
        else:
            for item in powerset(seq[1:]):
                yield item
                yield [seq[0]] + item
    return powerset_impl(list(collection))
