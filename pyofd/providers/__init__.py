# -*- coding: utf-8 -*-

"""
pyofd.providers
(c) Serge A. Levin, 2018
"""

from .providers import *
from decimal import Decimal

_ALL_CLASSES = [
    klass for
    name, klass in globals().items()
    if name.startswith('ofd') and isinstance(klass, type)
]


def get_providers_classes():
    """

    :return: list of all known provider classes
    """
    return _ALL_CLASSES


def get_providers():
    """

    :return: list of instances of all known provider classes
    """
    return [klass() for klass in get_providers_classes()]


class Result:
    """ Class representing receipt parsing result

    """
    def __init__(self,
                 seller_name=None, seller_address=None,
                 total=Decimal(),
                 inn=None, fn=None, fd=None, fpd=None,
                 shift_no=None, receipt_no=None, cashier=None,
                 rn_kkt= None, purchase_date=None,
                 items=[]
                 ):
        """Construct result from the parsed OFD provider response

        :param seller_name: Seller organization name
        :param seller_address: Seller address
        :param total: receipt total
        :param inn: Seller taxpayer ID
        :param fn: Receipt FN number
        :param fd: Receipt FD number
        :param fpd: Receipt signature
        :param shift_no: Shop shift number
        :param receipt_no: Receipt sequental number during shift
        :param cashier: Cashier name
        :param rn_kkt: Cashier machine registry number
        :param purchase_date: Purchase date and time
        :param items: Items within receipt
        """
        parameters = {k: v for k, v in locals().items() if k != 'self'}
        for name, value in parameters.items():
            setattr(self, name, value)

        if items is not None:
            self.items = items.copy()
        self.total = Decimal(self.total)
