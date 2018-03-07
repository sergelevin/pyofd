# -*- coding: utf-8 -*-

"""
aiopyofd
(c) Serge A. Levin, 2018
"""


from functools import total_ordering
from decimal import Decimal
from asyncio import get_event_loop, wait, FIRST_COMPLETED
import aiopyofd.providers


__version__ = '0.0.2.dev'


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

    async def load_receipt(self, check_providers=None, loop=None):
        """
        Validates data over known OFD providers and loads receipt details

        Providers are checked in parallel and first one giving non-empty result is treated as correct
        This method is a coroutine

        :param check_providers: Single provider instance or iterable of providers to load receipt from
        :param loop: asyncio event loop
        :return: True if could validate and load receipt data, False otherwise
        """
        if self.provider:
            return True

        if check_providers:
            if not hasattr(check_providers, '__iter__'):
                check_providers = (check_providers,)
        else:
            check_providers = aiopyofd.providers.get_providers()

        args = {k: getattr(self, k, None) for k in self._fields}

        check_providers = [provider for provider in check_providers if provider.is_candidate(**args)]
        if not check_providers:
            return False

        if loop is None:
            loop = get_event_loop()

        def wrap(o):
            async def f():
                check_result = await o.validate(loop=loop, **args)
                return o, check_result
            return loop.create_task(f())

        pending = [wrap(provider) for provider in check_providers]
        done = False

        while not done and pending:
            finished, pending = await wait(pending, loop=loop, return_when=FIRST_COMPLETED)
            for candidate in finished:
                if not candidate.cancelled() and candidate.exception() is None:
                    provider, result = candidate.result()
                    if result:
                        done = True
                        self.provider = provider
                        self.result = result
                        break

        for n in pending:
            n.cancel()
            wait(pending, loop=loop)

        return done

    @property
    def items(self):
        if self.result and self.result.items:
            return self.result.items.copy()
        else:
            return []
