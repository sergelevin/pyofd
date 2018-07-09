# -*- coding: utf-8 -*-

"""
pyofd.providers.platforma

Platforma OFD provider.
(c) Serge A. Levin, 2018
"""


from .base import Base
import pyofd
import lxml.html
import pyofd.providers
from decimal import Decimal
import datetime


def _strip(value):
    return str(value).strip()


def _undup_spaces(line):
    return ' '.join(i for i in line.split() if i)


def _to_decimal(value):
    return Decimal(str(value))


def _to_decimal100(value):
    return Decimal(str(value)) / 100


def _to_datetime(value):
    """ Example: 10.01.2018 17:37

    :return: datetime
    """
    return datetime.datetime.strptime(str(value), '%d.%m.%Y %H:%M')

def _extract_inn(value):
    return _strip(value[3:])

class ofdPlatforma(Base):
    providerName = 'Platforma'
    urlTemplate = 'https://lk.platformaofd.ru/web/noauth/cheque?fn={fn}&fp={fpd}&i={fd}'
    requiredFields = ('fpd', 'fn', 'fd')

    def parse_response(self, data):
        tree = lxml.html.parse(data)
        root = tree.getroot()

        result = []
        receipt_base = root.find_class('check-sections')
        if len(receipt_base) < 1:
            return

        receipt_base = receipt_base[0]
        sections = receipt_base.find_class('check-section')
        if len(sections) < 3:
            return
        entries = sections[1:-2]
        for entry in entries:
            candidate = self._parse_entry(entry)
            if candidate:
                result.append(candidate)

        if result:
            recognized_fields = {}
            recognized_fields.update(self._parse_top_entry(sections[0]))
            recognized_fields.update(self._parse_receipt_details(sections[-1]))
            recognized_fields.update(self._parse_totals(sections[-2]))
            check_top = root.find_class('check-top')[0]
            recognized_fields.update(self._parse_caption(check_top))
            check = root.find_class('check')[0]
            recognized_fields.update(self._extract_receipt_no(check))

            return pyofd.providers.Result(items=result, **recognized_fields)

    @staticmethod
    def _parse_entry(entry):
        try:
            rows = entry.find_class('check-col-right')

            title = entry.getchildren()[0].text.strip()

            qty_and_price = [item for item in rows[0].text.split(' ') if item]
            quantity = qty_and_price[0]
            price    = qty_and_price[2]
            subtotal = rows[-1].text

            return pyofd.ReceiptEntry(title=title, price=price, qty=quantity, subtotal=subtotal)
        except:
            return None

    @staticmethod
    def _parse_top_entry(entry):
        rows = entry.find_class('check-col-right')
        result = {
            'purchase_date': _to_datetime(_strip(rows[0].text)),
            'shift_no': int(_strip(rows[1].text)),
            'cashier': _strip(rows[2].text),
        }
        return result

    @staticmethod
    def _parse_receipt_details(entry):
        rows = entry.find_class('check-col-right')
        result = {
            'fn': _strip(rows[0].text),
            'rn_kkt': _strip(rows[1].text),
            'fd': _strip(rows[2].text),
            'fpd': _strip(rows[3].text),
        }
        return result

    @staticmethod
    def _parse_totals(entry):
        rows = entry.find_class('check-col-right')
        text = _strip(rows[0].text)
        text = text.lstrip('= ')
        result = {'total': Decimal(text)}
        return result

    @staticmethod
    def _parse_caption(fragment):
        children = fragment.xpath('.//div')

        result = {
            'seller_name': _undup_spaces(_strip(children[0].text)),
            'seller_address': _undup_spaces(_strip(children[1].text)),
            'inn': _extract_inn(_strip(children[2].text)),
        }
        return result

    @staticmethod
    def _extract_receipt_no(receipt):
        headline = receipt.find_class('check-headline')[0]
        entry = headline.xpath('.//span')[0]
        return {'receipt_no': int(entry.text)}
