# -*- coding: utf-8 -*-

"""
pyofd
(c) Serge A. Levin, 2018
"""


import pyofd.providers
from functools import total_ordering
from decimal import Decimal


__version__ = '0.1.4'


@total_ordering
class ReceiptEntry:
    def __init__(self, title, price, qty, subtotal):
        self.title = title
        self.price = Decimal(price)
        self.quantity = Decimal(qty)
        self.subtotal = Decimal(subtotal)

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

    def __repr__(self):
        return '"{}": {}x{} ({})'.format(self.title, self.quantity, self.price, self.subtotal)


class OFDReceipt:
    def __init__(
            self,
            fpd=None,
            total=None,
            rn_kkt=None,
            fd=None,
            fn=None,
            inn=None,
            purchase_date=None,
    ):
        """
        :param fpd: Receipt signature (FPD in terms of Tax service of Russia)
        :param total: Receipt total
        :param rn_kkt: Cash machine serial number (RN KKT)
        :param fd: Receipt number (FD)
        :param fn: Receipt fiscal number (FN)
        :param inn: Seller's taxpayer identifier (INN)
        :param purchase_date: Purchase date and time
        """
        fields = [k for k in locals().keys() if k != 'self']

        for key in fields:
            setattr(self, key, locals()[key])

        self.result = None
        self.provider = None
        self._fields = fields

    def load_receipt(self, check_providers=None):
        """
        Validates data over known OFD providers and loads receipt details

        :param check_providers: Single provider instance or iterable of providers to load receipt from
        :return: True if could validate and load receipt data, False otherwise
        """
        if self.provider:
            return True

        if check_providers:
            if not hasattr(check_providers, '__iter__'):
                check_providers = (check_providers,)
        else:
            check_providers = pyofd.providers.get_providers()

        args = {k: getattr(self, k, None) for k in self._fields}
        for provider in check_providers:
            if not provider.is_candidate(**args):
                continue

            result = provider.validate(**args)
            if result:
                self.provider = provider
                self.result = result
                return True

        return False

    @property
    def items(self):
        if self.result and self.result.items:
            return self.result.items.copy()
        else:
            return []
