# -*- coding: utf-8 -*-

import unittest
import pyofd
from datetime import datetime


receipts_data = {
    'Taxcom': {
        'signature': 1027455652,
        'total': 1487,
        'cash_machine_no': 1482558031668,
        'receipt_no': 9960,
        'taxpayer_id': 7814148471,
        'purchase_date': datetime(year=2018, month=1, day=7, hour=14, minute=51)
    },
    'Platforma': {
        'signature': 504931317,
        'total': '822.91',
        'cash_machine_no': 8710000100186516,
        'receipt_no': 136682,
        'taxpayer_id': 5036045205,
        'purchase_date': datetime(year=2018, month=1, day=10, hour=17, minute=37)
    },
    '1-OFD': {
        'signature': 2819037689,
        'total': '1948.28',
        'cash_machine_no': 8710000100828376,
        'receipt_no': 87242,
        'taxpayer_id': 7840016802,
        'purchase_date': datetime(year=2017, month=9, day=30, hour=16, minute=7)
    },
    'Yarus':{
        'signature': 4023651155,
        'total': '526.00',
        'cash_machine_no': 691164058512,
        'receipt_no': 34113,
        'taxpayer_id': 7705814643,
        'purchase_date': datetime(year=2018, month=1, day=13, hour=20, minute=44)
    },
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
