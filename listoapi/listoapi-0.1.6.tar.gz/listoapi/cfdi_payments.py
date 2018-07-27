# -*- coding: utf-8 -*-
from .api import ListoAPI


class CfdiPayments(ListoAPI):
    def __init__(self, token):
        super(CfdiPayments, self).__init__(token)

    def cfdi_payments(self, **kwargs):
        """CFDI Payments

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 250)
        while True:
            r = self.make_request(
                method="GET", path="/cfdi_payments/payments/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size

    def cfdi_receipts(self, **kwargs):
        """CFDI Receipts

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 250)
        while True:
            r = self.make_request(
                method="GET", path="/cfdi_payments/receipts/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size
