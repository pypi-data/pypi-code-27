from typing import *
from math import *
from itertools import *

T = TypeVar('T')
num = Union[int, float]


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


def cartesian_product(*collections: Collection[T]) -> Iterator[Tuple[T]]:
    return product(*collections)


def coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


def coprimes(n: int) -> Iterator[int]:
    if is_prime(n):
        return range(1, n)
    if log(n, 2).is_integer():
        return range(1, n, 2)
    return (i for i in range(1, n) if gcd(n, i) == 1)


def factors(n: int) -> Iterator[int]:
    n = abs(n)
    return (i for i in range(1, n+1) if n % i == 0)


def is_prime(n: int) -> bool:
    return n > 1 and all((n % i) for i in range(2, 2+int(sqrt(n)-1)))


def prime_factors(n: int) -> Iterator[int]:
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            yield i
    if n > 1:
        yield i


def largest_prime_factor(n: int) -> int:
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
    return n


def is_mersenne_prime(n: int) -> int:
    return log(n+1, 2).is_integer() and is_prime(n)


def primes(n: int) -> Iterator[int]:
    pass


def is_rational(n: num) -> bool:
    pass


def primes_up_to(n: int) -> Iterator[int]:
    pass
