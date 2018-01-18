# -*- coding: utf-8 -*-

"""
pyofd.providers.first_ofd

1-OFD provider.
(c) Serge A. Levin, 2018
"""


from .base import Base
import pyofd
import pyofd.providers
import urllib.request as _request
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
    return datetime.datetime.strptime(str(value + '000'), '%Y-%m-%dT%H:%M:%S.%f')


class ofd1OFD(Base):
    providerName = '1-OFD'
    urlTemplate = None
    requiredFields = ('fpd', 'fn', 'fd')
    urlPhase1 = 'https://consumer.1-ofd.ru/api/tickets/find-ticket'
    urlPhase2 = 'https://consumer.1-ofd.ru/api/tickets/ticket/{receipt_guid}'

    _jsonTicketFieldsMapping = {
        'user': ('seller_name', _strip),
        'totalSum': ('total', _to_decimal),
        'userInn': ('inn', _strip),
        'fiscalDriveNumber': ('fn', _strip),
        'fiscalDocumentNumber': ('fd', _strip),
        'fiscalId': ('fpd', _strip),
        'shiftNumber': ('shift_no', int),
        'requestNumber': ('receipt_no', int),
        'kktRegId': ('rn_kkt', _strip),
        'transactionDate': ('purchase_date', _to_datetime),
    }

    _jsonRootFieldsMapping = {
        'retailPlaceAddress': ('seller_address', _strip),
    }

    def validate(
            self,
            fpd=None,
            total=None,
            rn_kkt=None,
            fd=None,
            fn=None,
            inn=None,
            purchase_date=None,
    ):
        request_body = json.dumps({
            'fiscalDriveId': str(fn),
            'fiscalDocumentNumber': str(fd),
            'fiscalId': str(fpd),
        }, separators=(',', ':'))
        request = self._build_request(self.urlPhase1, request_body)

        data = self._get_json_data(request)
        if 'status' in data and 'uid' in data and data['status'] == 1:
            receipt_guid = data['uid']
        else:
            return None
        data = self._get_json_data(self.urlPhase2.format(receipt_guid=receipt_guid))

        try:
            items = data['ticket']['items']
        except KeyError:
            return None

        result = []
        for item in items:
            entry = self._parse_entry(item)
            if entry:
                result.append(entry)

        if result:
            ticket = data['ticket']
            recognized_fields = {v[0]: v[1](ticket[k]) for k, v in self._jsonTicketFieldsMapping.items() if k in ticket}
            recognized_fields.update({v[0]: v[1](data[k]) for k, v in self._jsonRootFieldsMapping.items() if k in data})
            return pyofd.providers.Result(items=result, **recognized_fields)

    @staticmethod
    def _build_request(url, data):
        return _request.Request(
            url=url,
            data=data.encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
            },
            method='POST',
        )

    @staticmethod
    def _get_json_data(url):
        try:
            response = _request.urlopen(url)
        except IOError:
            return {}

        if response.getcode() != 200:
            return {}

        data = response.read()
        try:
            return json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            return {}

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


__all__ = ['ofd1OFD']
