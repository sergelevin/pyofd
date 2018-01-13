# -*- coding: utf-8 -*-

"""
pyofd
(c) Serge A. Levin, 2018
"""


import pyofd.providers
from functools import total_ordering


@total_ordering
class ReceiptEntry:
    def __init__(self, title, price, qty, subtotal):
        self.title = title
        self.price = price
        self.quantity = qty
        self.subtotal = subtotal

    @staticmethod
    def _is_comparable(other):
        return (
            hasattr(other, 'title') and
            hasattr(other, 'price') and
            hasattr(other, 'quantity') and
            hasattr(other, 'subtotal')
        )

    def __eq__(self, other):
        if not self._is_comparable(other):
            return NotImplemented
        return (self.title, self.price, self.quantity, self.subtotal) == \
               (other.title, other.price, other.quantity, other.subtotal)

    def __le__(self, other):
        if not self._is_comparable(other):
            return NotImplemented
        return (self.title, self.price, self.quantity, self.subtotal) < \
               (other.title, other.price, other.quantity, other.subtotal)


class OFDReceipt:
    def __init__(
            self,
            signature=None,
            total=None,
            cash_machine_no=None,
            receipt_no=None,
            taxpayer_id=None,
            purchase_date=None,
    ):
        """
        :param signature: Receipt signature (FPD in terms of Tax service of Russia)
        :param total: Receipt total
        :param cash_machine_no: Cash machine serian number (RN KKT)
        :param receipt_no: Receipt fiscal number (FN)
        :param taxpayer_id: Seller's taxpayer identifier (INN)
        :param purchase_date: Purchase date and time
        """
        fields = [k for k in locals().keys() if k != 'self']

        for key in fields:
            setattr(self, key, locals()[key])

        self.items = []
        self.provider = None
        self._fields = fields

    def load_receipt(self):
        """
        Validates data over known OFD providers and loads receipt details

        :return: True if could validate and load receipt data, False otherwise
        """
        if self.provider:
            return True

        args = {k: getattr(self, k, None) for k in self._fields}
        for provider in pyofd.providers.get_providers():
            if not provider.is_candidate(**args):
                continue

            result = provider.validate(**args)
            if result:
                self.provider = provider
                self.items = result.copy()
                return True

        return False
