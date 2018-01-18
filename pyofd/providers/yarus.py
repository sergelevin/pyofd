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
import datetime


def _strip(value):
    return str(value).strip()


def _to_decimal(value):
    return Decimal(str(value))


def _to_datetime(value):
    """ Example: 2018-01-18T22:42:35.413

    :return: datetime with milliseconds stripped
    """
    return datetime.datetime.fromtimestamp(int(value))


def _to_decimal100(value):
    return Decimal(str(value)) / 100


class ofdYarus(Base):
    providerName = 'Yarus'
    urlTemplate = 'https://ofd-ya.ru/getFiscalDoc?kktRegId={rn_kkt:0>16}&fiscalSign={fpd:0>10}&json=true'
    requiredFields = ('rn_kkt', 'fpd')

    _jsonTicketFieldsMapping = {
        'user': ('seller_name', _strip),
        'operator': ('cashier', _strip),
        'totalSum': ('total', _to_decimal100),
        'fiscalDriveNumber': ('fn', _strip),
        'fiscalDocumentNumber': ('fd', _strip),
        'fiscalSign': ('fpd', _strip),
        'shiftNumber': ('shift_no', int),
        'requestNumber': ('receipt_no', int),
        'kktRegId': ('rn_kkt', _strip),
        'dateTime': ('purchase_date', _to_datetime),
        'retailAddress': ('seller_address', _strip),
        'userInn': ('inn', _strip),
    }

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

        if result:
            ticket = raw_data['requestmessage']
            recognized_fields = {v[0]: v[1](ticket[k]) for k, v in self._jsonTicketFieldsMapping.items() if k in ticket}
            return pyofd.providers.Result(items=result, **recognized_fields)

    @staticmethod
    def _parse_entry(entry):
        try:
            subtotal = _to_decimal(entry['sum']) / 100
            quantity = _to_decimal(entry['quantity'])
            price = _to_decimal(entry['price']) / 100
            name = _strip(entry['name'])

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
