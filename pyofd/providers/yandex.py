# -*- coding: utf-8 -*-

"""
pyofd.providers.yandex

Yandex OFD provider.
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


def _strip_currency(value):
    return value.split(' ')[0]


def _keep_number(value):
    return ''.join(c for c in value if c.isdigit())


class ofdYandex(Base):
    providerName = 'Yandex'
    urlTemplate = 'https://ofd.yandex.ru/vaucher/{rn_kkt:0>16}/{fd}/{fpd:0>10}'
    requiredFields = ('fpd', 'rn_kkt', 'fd')

    def parse_response(self, data):
        tree = lxml.html.parse(data)
        root = tree.getroot()

        result = []
        report = root.find_class('vaucher_body')
        if report:
            report = report[0]

        entries = report.find_class('vaucher__item')
        for entry in entries:
            candidate = self._parse_entry(entry)
            if candidate:
                result.append(candidate)

        if result:
            recognized_fields = {}
            recognized_fields.update(self._parse_receipt_details(report))

            return pyofd.providers.Result(items=result, **recognized_fields)

    @staticmethod
    def _parse_entry(entry):
        try:
            title    = entry.find_class('vaucher__text_col_name' )[0].text
            quantity = entry.find_class('vaucher__text_col_count')[0].text
            price    = _strip_currency(entry.find_class('vaucher__text_col_cost')[0].text)
            subtotal = _strip_currency(entry.find_class('vaucher__text_col_sum' )[0].text)

            return pyofd.ReceiptEntry(title=title, price=price, qty=quantity, subtotal=subtotal)
        except:
            return None

    @staticmethod
    def _parse_receipt_details(entry):
        rows = entry.getchildren()
        result = {
            'seller_name': _strip(rows[0].text),
            'inn': _keep_number(rows[1].text),
            'seller_address': _strip(rows[2].text),
            'fn': _keep_number(rows[5].text),
            'rn_kkt': _keep_number(rows[6].text),
            'fpd': _keep_number(rows[7].text),
            'cashier': _strip(rows[9].text[7:]),
            'purchase_date': _to_datetime(rows[10].text[6:]),
            'total': Decimal(_strip_currency(entry.find_class('vaucher__text_type_total')[1].text)),
        }
        return result
