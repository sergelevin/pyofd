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


class ofd1OFD(Base):
    providerName = '1-OFD'
    urlTemplate = None
    requiredFields = ('signature', 'cash_machine_no', 'receipt_no')
    urlPhase1 = 'https://consumer.1-ofd.ru/api/tickets/find-ticket'
    urlPhase2 = 'https://consumer.1-ofd.ru/api/tickets/ticket/{receipt_guid}'

    def validate(
            self,
            signature=None,
            total=None,
            cash_machine_no=None,
            receipt_no=None,
            taxpayer_id=None,
            purchase_date=None,
    ):
        request_body = json.dumps({
            'fiscalDriveId': str(cash_machine_no),
            'fiscalDocumentNumber': str(receipt_no),
            'fiscalId': str(signature),
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
            return json.loads(data)
        except json.JSONDecodeError:
            return {}

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
