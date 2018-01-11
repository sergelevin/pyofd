# -*- coding: utf-8 -*-

"""
pyofd.providers.dummy

Dummy OFD provider. It checks all receipts as invalid
(c) Serge A. Levin, 2018
"""


from .base import Base


class ofdDummy(Base):
    providerName = 'Dummy'
    urlTemplate = 'http://example.com/receipt?total={total}&signature={q_signature}'

    def parse_response(self, data):
        return None
