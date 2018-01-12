# -*- coding: utf-8 -*-

"""
pyofd.providers.platforma

Platforma OFD provider.
(c) Serge A. Levin, 2018
"""


from .base import Base
import pyofd
import lxml.html


class ofdPlatforma(Base):
    providerName = 'Platforma'
    urlTemplate = 'https://lk.platformaofd.ru/web/noauth/cheque?fn={cash_machine_no}&fp={signature}&i={receipt_no}'
    requiredFields = ('signature', 'cash_machine_no', 'receipt_no')

    def parse_response(self, data):
        tree = lxml.html.parse(data)
        root = tree.getroot()

        result = []
        receipt_base = root.find_class('check-sections')
        if len(receipt_base) < 1:
            return

        receipt_base = receipt_base[0]
        entries = receipt_base.find_class('check-section')
        if len(entries) < 3:
            return
        entries = entries[1:-2]
        for entry in entries:
            candidate = self._parse_entry(entry)
            if candidate:
                result.append(candidate)

        return result or None

    @staticmethod
    def _parse_entry(entry):
        try:
            rows = entry.find_class('check-col-right')

            title = entry.getchildren()[0].text.strip()

            qty_and_price = [ item for item in rows[0].text.split(' ') if item ]
            quantity = qty_and_price[0]
            price    = qty_and_price[2]
            subtotal = rows[2].text

            return pyofd.ReceiptEntry(title=title, price=price, qty=quantity, subtotal=subtotal)
        except:
            return None
