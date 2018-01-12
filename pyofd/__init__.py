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
    def __init__(self, signature, total):
        """
        :param signature: Receipt signature (FPD in terms of Tax service of Russia)
        :param total: Receipt total
        """
        self.signature = signature
        self.total = total
        self.items = []

    def load_receipt(self):
        """
        Validates data over known OFD providers and loads receipt details

        :return: True if could validate and load receipt data, False otherwise
        """
        if hasattr(self, "provider"):
            return True

        args = {
            'signature' : self.signature,
            'total'     : self.total,
        }
        for provider in pyofd.providers.get_providers():
            if not provider.is_candidate(**args):
                continue

            result = provider.validate(**args)
            if result:
                self.provider = provider
                self.items = result.copy()
                return True

        return False
