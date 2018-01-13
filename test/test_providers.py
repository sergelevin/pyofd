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
