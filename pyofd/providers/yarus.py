# -*- coding: utf-8 -*-

"""
pyofd.providers.yarus
Yarus OFD provider.
(c) Serge A. Levin, 2018
"""

from .base import Base
import pyofd
import json
from decimal import Decimal


class ofdYarus(Base):
    providerName = 'Yarus'
    urlTemplate = 'https://ofd-ya.ru/getFiscalDoc?kktRegId={rn_kkt:0>16}&fiscalSign={fpd:0>10}&json=true'
    requiredFields = ('rn_kkt', 'fpd')

    def parse_response(self, data):
        raw_data = json.loads(data.read().decode('utf-8'))

        try:
            items = raw_data['requestmessage']['items']
        except KeyError:
            return None

        result = []
        for item in items:
            entry = self._parse_entry(item)
            if entry:
                result.append(entry)

        return result or None

    @staticmethod
    def _parse_entry(entry):
        try:
            subtotal = Decimal(str(entry['sum'])) / 100
            quantity = str(entry['quantity'])
            price = Decimal(str(entry['price'])) / 100
            name = str(entry['name'])

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
