# -*- coding: utf-8 -*-

"""
pyofd.providers.nalog
OFD provider for checking receipts via nalog.ru API
(c) Serge A. Levin, 2018
"""

from .base import Base
import pyofd
import json
import urllib.request as _request
import base64
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


class NalogRu(Base):
    apiLogin = None
    apiPassword = None

    urlTemplate = 'http://proverkacheka.nalog.ru:8888/' \
                  'v1/inns/*/kkts/*/fss/{fn:0>16}/tickets/{fd}?fiscalSign={fpd:0>10}&sendToEmail=no'
    requiredFields = ('fn', 'fd', 'fpd')

    _jsonFieldsMapping = {
        'user': ('seller_name', _strip),
        'operator': ('cashier', _strip),
        'totalSum': ('total', _to_decimal100),
        'fiscalDriveNumber': ('fn', _strip),
        'fiscalDocumentNumber': ('fd', int),
        'fiscalSign': ('fpd', _strip),
        'shiftNumber': ('shift_no', int),
        'requestNumber': ('receipt_no', int),
        'kktRegId': ('rn_kkt', _strip),
        'dateTime': ('purchase_date', _to_datetime),
        'retailPlaceAddress': ('seller_address', _strip),
        'userInn': ('inn', _strip),
    }

    def is_candidate(self, **kwargs):
        return self.apiLogin and self.apiPassword and super(NalogRu, self).is_candidate(**kwargs)

    def get_request_url(self, **context):
        url = super(NalogRu, self).get_request_url(**context)
        auth_pair = '{}:{}'.format(self.apiLogin, self.apiPassword)
        auth_token = base64.standard_b64encode(auth_pair.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': 'Basic {}'.format(auth_token),
            'Device-Id': 'None',
            'Device-OS': 'None'
        }

        return _request.Request(url, headers=headers, method='GET')

    def parse_response(self, data):
        raw_data = json.loads(data.read().decode('utf-8'))

        try:
            items = raw_data['document']['receipt']['items']
        except KeyError:
            return None

        result = []
        for item in items:
            entry = self._parse_entry(item)
            if entry:
                result.append(entry)

        if result:
            document = raw_data['document']['receipt']
            recognized_fields = {v[0]: v[1](document[k]) for k, v in self._jsonFieldsMapping.items() if k in document}
            return pyofd.providers.Result(items=result, **recognized_fields)

    def _parse_entry(self, entry):
        try:
            subtotal = _to_decimal(entry['sum']) / 100
            quantity = _to_decimal(entry['quantity'])
            price = _to_decimal(entry['price']) / 100
            name = _strip(entry['name'])

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
