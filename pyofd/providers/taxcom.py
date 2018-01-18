# -*- coding: utf-8 -*-

"""
pyofd.providers.taxcom

Taxcom OFD provider.
(c) Serge A. Levin, 2018
"""

from .base import Base
import pyofd
import lxml.html


class ofdTaxcom(Base):
    providerName = 'Taxcom'
    urlTemplate = 'https://receipt.taxcom.ru/v01/show?fp={fpd}&s={total}'
    requiredFields = ('fpd', 'total')

    not_found = 'Такой чек не найден'

    def parse_response(self, data):
        tree = lxml.html.parse(data)
        root = tree.getroot()

        for h1 in root.iter(tag='h1'):
            if h1.text == self.not_found:
                return

        result = []
        for report in root.find_class('receipt_report'):
            entries = report.getchildren()[1]
            for entry in entries.find_class('verticalBlock'):
                candidate = self._parse_entry(entry.xpath('.//table')[0])
                if candidate:
                    result.append(candidate)

        if result:
            return pyofd.providers.Result(items=result)

    @staticmethod
    def _parse_entry(entry):
        try:
            rows = entry.findall('tr')

            title    = rows[0].xpath('.//span')[0].text
            quantity = rows[1].xpath('.//span')[0].text
            price    = rows[1].xpath('.//span')[1].text
            subtotal = rows[3].xpath('.//span')[1].text

            return pyofd.ReceiptEntry(title=title, price=price, qty=quantity, subtotal=subtotal)
        except:
            return None
