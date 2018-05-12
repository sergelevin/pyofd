# -*- coding: utf-8 -*-

"""
pyofd.providers.taxcom

Taxcom OFD provider.
(c) Serge A. Levin, 2018
"""

from .base import Base
import pyofd
import lxml.html
import datetime
from decimal import Decimal


def _strip(value):
    return str(value).strip()


def _to_datetime(value):
    """ Example: 10.01.2018 17:37

    :return: datetime
    """
    return datetime.datetime.strptime(str(value), '%d.%m.%Y %H:%M')


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
        report = root.find_class('receipt_report')
        if report:
            report = report[0]

        entries = report.getchildren()[1]
        for entry in entries.find_class('verticalBlock'):
            candidate = self._parse_entry(entry.xpath('.//table')[0])
            if candidate:
                result.append(candidate)

        tables = report.xpath('./table')
        if result:
            recognized_fields = {}
            recognized_fields.update(self._parse_top_entry(report.getchildren()[0]))
            recognized_fields.update(self._parse_receipt_details(tables[-2]))
            recognized_fields.update(self._parse_total(tables[-5]))

            return pyofd.providers.Result(items=result, **recognized_fields)

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

    @staticmethod
    def _parse_top_entry(entry):
        rows = entry.findall('tr')
        result = {
            'seller_name': _strip(rows[0].xpath('.//span')[0].text),
            'inn': _strip(rows[1].xpath('.//span')[0].text),
            'seller_address': _strip(rows[2].xpath('.//span')[1].text),
            'purchase_date': _to_datetime(rows[4].xpath('.//span')[1].text),
            'receipt_no': int(rows[5].xpath('.//span/span')[0].text),
            'shift_no': int(rows[6].xpath('.//span/span')[0].text),
            'cashier': _strip(rows[7].xpath('.//span/span')[1].text),
        }
        return result

    @staticmethod
    def _parse_receipt_details(entry):
        rows = entry.findall('tr')
        result = {
            'rn_kkt': _strip(rows[7].xpath('.//span')[1].text),
            'fn': _strip(rows[8].xpath('.//span')[1].text),
            'fd': int(rows[9].xpath('.//span')[1].text),
            'fpd': _strip(rows[11].xpath('.//span')[1].text),
        }
        return result

    @staticmethod
    def _parse_total(entry):
        rows = entry.findall('tr')
        return {'total': Decimal(rows[1].xpath('.//span')[0].text)}
