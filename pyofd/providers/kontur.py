# -*- coding: utf-8 -*-

"""
pyofd.providers.kontur
Kontur OFD provider.
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
    """ Example: 2018-05-06T19:44:00Z

    :return: datetime with milliseconds stripped
    """
    return datetime.datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%SZ')


def _to_decimal100(value):
    return Decimal(str(value)) / 100


class ofdKontur(Base):
    providerName = 'Kontur'
    urlTemplate = 'https://ofd-api.kontur.ru/v1/cash-receipt/kontur/?fiscalSignature={fpd:0>10}&fnSerialNumber={fn:0>10}&fiscalDocumentNumber={fd}'
    requiredFields = ('fn', 'fd', 'fpd')

    _jsonTicketFieldsMapping = {
        'organizationName': ('seller_name', _strip),
        'cashier': ('cashier', _strip),
        'fnSerialNumber': ('fn', _strip),
        'fiscalDocumentNumber': ('fd', int),
        'fiscalSignature': ('fpd', int),
        'shiftNumber': ('shift_no', int),
        'cashboxRegNumber': ('rn_kkt', _strip),
        'dateTime': ('purchase_date', _to_datetime),
        'inn': ('inn', _strip),
    }

    _jsonRootFieldsMapping = {
        'number' : ('receipt_no', int),
        'total' : ('total', _to_decimal),
    }

    def parse_response(self, data):
        raw_data = json.loads(data.read().decode('utf-8'))

        try:
            items = raw_data['products']
        except KeyError:
            return None

        result = []
        for item in items:
            entry = self._parse_entry(item)
            if entry:
                result.append(entry)

        if result:
            ticket = raw_data['requisites']
            recognized_fields = {v[0]: v[1](ticket[k]) for k, v in self._jsonTicketFieldsMapping.items() if k in ticket}
            recognized_fields.update( {v[0]: v[1](raw_data[k]) for k, v in self._jsonRootFieldsMapping.items() if k in raw_data} )
            return pyofd.providers.Result(items=result, **recognized_fields)

    @staticmethod
    def _parse_entry(entry):
        try:
            subtotal = _to_decimal(entry['total'])
            quantity = _to_decimal(entry['count'])
            price = _to_decimal(entry['price'])
            name = _strip(entry['name'])

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
