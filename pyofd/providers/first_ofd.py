# -*- coding: utf-8 -*-

"""
pyofd.providers.first_ofd

1-OFD provider.
(c) Serge A. Levin, 2018
"""


from .base import Base
import pyofd
import urllib.request as _request
import json
from decimal import Decimal


class ofd1OFD(Base):
    providerName = '1-OFD'
    urlTemplate = None
    requiredFields = ('fpd', 'fn', 'fd')
    urlPhase1 = 'https://consumer.1-ofd.ru/api/tickets/find-ticket'
    urlPhase2 = 'https://consumer.1-ofd.ru/api/tickets/ticket/{receipt_guid}'

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

        return result or None

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
            subtotal = Decimal(str(entry['sum'])) / 100
            quantity = Decimal(str(entry['quantity']))
            price = Decimal(str(entry['price'])) / 100
            name = entry['name']

            return pyofd.ReceiptEntry(name, price, quantity, subtotal)
        except KeyError:
            return None
