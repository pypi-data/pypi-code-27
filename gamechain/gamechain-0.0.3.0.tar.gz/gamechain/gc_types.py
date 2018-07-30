
from typing import Union
from bitcash import PrivateKey, PrivateKeyTestnet


class TxId:
    pass


class GcAddr:
    pass


class GcPrivateKey:

    def __init__(self, pk: Union[PrivateKey, PrivateKeyTestnet] = None):
        if pk is None:
            self._pk = PrivateKeyTestnet()
        else:
            self._pk = pk

    def get_unspents(self):
        return self._pk.get_unspents()

    @property
    def public_key(self):
        return self._pk.public_key

    @property
    def address(self):
        return self._pk.address

    def sign(self, data):
        return self._pk.sign(data)

    @property
    def bitcash_key(self):
        return self._pk
