import sys

try:
    sys.modules['CryptoLib'] = __import__('Cryptodome')
    import Cryptodome as _crypto_lib
except ImportError:
    try:
        sys.modules['CryptoLib'] = __import__('Crypto')
    except ImportError:
        raise ImportError('PyCryptodomeX (recommended) or PyCrypto must be installed')

CryptoLib = __import__('CryptoLib')
