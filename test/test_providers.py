# -*- coding: utf-8 -*-

import unittest
import pyofd
from datetime import datetime


receipts_data = {
    'Taxcom': {
        'fpd': 1027455652,
        'total': 1487,
        'rn_kkt': 1482558031668,
        'fd': 9960,
        'inn': 7814148471,
        'purchase_date': datetime(year=2018, month=1, day=7, hour=14, minute=51)
    },
    'Platforma': {
        'fpd': 504931317,
        'total': '822.91',
        'fn': 8710000100186516,
        'rn_kkt': '0000051440037872',
        'fd': 136682,
        'inn': 5036045205,
        'purchase_date': datetime(year=2018, month=1, day=10, hour=17, minute=37)
    },
    '1-OFD': {
        'fpd': 2819037689,
        'total': '1948.28',
        'fn': 8710000100828376,
        'fd': 87242,
        'inn': 7840016802,
        'purchase_date': datetime(year=2017, month=9, day=30, hour=16, minute=7)
    },
    'Yarus': {
        'fpd': 4023651155,
        'total': '526.00',
        'rn_kkt': 691164058512,
        'fd': 34113,
        'inn': 7705814643,
        'purchase_date': datetime(year=2018, month=1, day=13, hour=20, minute=44)
    },
    'OfdRu': {
        'fpd': 2981623349,
        'total': 330,
        'rn_kkt': 489397013091,
        'fd': 7481,
        'inn': 7814339162,
        'fn': 8710000100617432,
        'purchase_date': datetime(year=2018, month=1, day=16, hour=13, minute=11)
    },
    'Yandex': {
        'fpd': 3826178549,
        'total': '390',
        'rn_kkt': 840594031594,
        'fd': 238872,
        'inn': 7704340310,
        'purchase_date': datetime(year=2018, month=3, day=7, hour=10, minute=57)
    },
    'Kontur': {
        'fpd': 1753141947,
        'total': 838,
        'rn_kkt': 1573495028400,
        'fd': 3250,
        'inn': 7736567560,
        'fn': 8710000101500109,
        'purchase_date': datetime(year=2018, month=5, day=6, hour=19, minute=44)
    }
}


class ProvidersTest(unittest.TestCase):
    def _test_single_provider(self, provider):
        self.assertIn(provider, receipts_data)
        kwargs = receipts_data[provider]
        receipt = pyofd.OFDReceipt(**kwargs)
        result = receipt.load_receipt()

        self.assertIsNotNone(result)
        self.assertIsNotNone(receipt.provider)
        self.assertEqual(provider, receipt.provider.providerName)

    def test_taxcom(self):
        self._test_single_provider('Taxcom')

    def test_platforma(self):
        self._test_single_provider('Platforma')

    def test_first_ofd(self):
        self._test_single_provider('1-OFD')

    def test_yarus(self):
        self._test_single_provider('Yarus')

    def test_ofd_ru(self):
        self._test_single_provider('OfdRu')

    def test_yandex(self):
        self._test_single_provider('Yandex')

    def test_kontur(self):
        self._test_single_provider('Kontur')
