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


class NalogRu(Base):
    apiLogin = None
    apiPassword = None

    urlTemplate = 'http://proverkacheka.nalog.ru:8888/' \
                  'v1/inns/*/kkts/*/fss/{fn:0>16}/tickets/{fd}?fiscalSign={fpd:0>10}&sendToEmail=no'
    requiredFields = ('fn', 'fd', 'fpd')

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

        return result or None

    @staticmethod
    def _fix_point(s):
        int = s[:-2] or '0'
        frac=s[-2:] or '0'
        if len(frac) == 1:
            frac = '0' + frac
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
