# -*- coding: utf-8 -*-

"""
pyofd.providers.ofd
OFD.Ru OFD provider.
(c) Serge A. Levin, 2018
"""

from .base import Base
import pyofd
import json
from decimal import Decimal


class ofdOfdRu(Base):
    providerName = 'OfdRu'
    urlTemplate = 'https://ofd.ru/api/rawdoc/RecipeInfo?' \
        'Fn={fn:0>16}&Kkt={rn_kkt:0>16}&Inn={inn}&Num=7481&Sign={fpd:0>10}'
    requiredFields = ('fn', 'inn', 'rn_kkt', 'fpd')

    def parse_response(self, data):
        raw_data = json.loads(data.read().decode('utf-8'))

        try:
            items = raw_data['Document']['Items']
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
            subtotal = Decimal(str(entry['Total'])) / 100
            quantity = str(entry['Quantity'])
            price = Decimal(str(entry['Price'])) / 100
            name = str(entry['Name'])

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
