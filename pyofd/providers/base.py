# -*- coding: utf-8 -*-

"""
pyofd.providers.base

Base OFD provider. Concrete OFD providers should inherit from this base and have a name like ofdXXX
(c) Serge A. Levin, 2018
"""

import urllib.parse as _parse
import urllib.request as _request
import io


class Base:
    providerName = None
    urlTemplate = ''
    requiredFields = ()

    def __init__(self):
        pass

    def is_candidate(self, **kwargs):
        for field in self.requiredFields:
            if not field in kwargs or kwargs[field] is None:
                return False

        return True

    def validate(self, signature, total):
        context = {
            'signature': signature,
            'total'    : total,
        }
        q_context = { ('q_' + k): _parse.quote(str(v)) for k, v in context.items() }
        context.update(q_context)

        url = self.urlTemplate.format(**context)

        try:
            response = _request.urlopen(url)
        except IOError:
            return None

        if response.getcode() != 200:
            return None

        data = response.read()

        try:
            return self.parse_response(io.BytesIO(data))
        except:
            return None

    def parse_response(self, data):
        """
        overridable to try parsing data, received from server
        :param data: BytesIO with data to be parsed
        :return: list of pyofd.ReceiptEntry if data is recognised
        """
        pass
