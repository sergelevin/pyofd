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
import datetime


def _strip(value):
    return str(value).strip()


def _to_decimal(value):
    return Decimal(str(value))


def _to_decimal100(value):
    return Decimal(str(value)) / 100


def _to_datetime(value):
    """ Example: 2018-01-18T22:42:35

    :return: datetime
    """
    return datetime.datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%S')


class ofdOfdRu(Base):
    providerName = 'OfdRu'
    urlTemplate = 'https://ofd.ru/api/rawdoc/RecipeInfo?' \
        'Fn={fn:0>16}&Kkt={rn_kkt:0>16}&Inn={inn}&Num={fd}&Sign={fpd:0>10}'
    requiredFields = ('fn', 'inn', 'rn_kkt', 'fpd', 'fd')

    _jsonFieldsMapping = {
        'Operator': ('cashier', _strip),
        'Amount_Total': ('total', _to_decimal100),
        'UserInn': ('inn', _strip),
        'FN_FactoryNumber': ('fn', _strip),
        'Document_Number': ('fd', int),
        'DecimalFiscalSign': ('fpd', _strip),
        'ShiftNumber': ('shift_no', int),
        'Number': ('receipt_no', int),
        'KKT_RegNumber': ('rn_kkt', _strip),
        'DateTime': ('purchase_date', _to_datetime),
    }

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

        if result:
            document = raw_data['Document']
            recognized_fields = {v[0]: v[1](document[k]) for k, v in self._jsonFieldsMapping.items() if k in document}
            return pyofd.providers.Result(items=result, **recognized_fields)

    @staticmethod
    def _parse_entry(entry):
        try:
            subtotal = _to_decimal(entry['Total']) / 100
            quantity = _to_decimal(entry['Quantity'])
            price = _to_decimal(entry['Price']) / 100
            name = _strip(entry['Name'])

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
