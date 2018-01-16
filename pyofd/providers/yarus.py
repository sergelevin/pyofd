# -*- coding: utf-8 -*-

"""
pyofd.providers.yarus
Yarus OFD provider.
(c) Serge A. Levin, 2018
"""

from .base import Base
import pyofd
import json


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
    def _fix_point(s):
        int = s[:-2] or '0'
        frac=s[-2:] or '0'
        if len(frac) == 1:
            frac='0' + frac
        return '.'.join((int, frac,))

    def _parse_entry(self, entry):
        try:
            subtotal = self._fix_point(str(entry['sum']))
            quantity = str(entry['quantity'])
            price = self._fix_point(str(entry['price']))
            name = str(entry['name'])

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
