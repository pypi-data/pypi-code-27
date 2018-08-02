from typing import List


def convert_base(n: int, b: int) -> List[int]:
    """Returns n converted from base 10 to base b."""
    output = []
    while n >= 1:
        n, r = divmod(n, b)
        output.append(r)
    output.reverse()
    return output
