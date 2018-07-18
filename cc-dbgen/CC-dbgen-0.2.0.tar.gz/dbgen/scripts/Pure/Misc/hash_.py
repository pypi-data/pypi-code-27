from typing  import Any
from hashlib import sha512

def hash_(x:Any)->str:
    """
    Creates a 128 Byte hash value
    """
    return sha512(str(x).encode()).hexdigest()
