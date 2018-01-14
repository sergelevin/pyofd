# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.first_ofd
import pyofd


class FirstOFDTest(unittest.TestCase):
    valid_receipt_items = [
            pyofd.ReceiptEntry(title='ТРК -  3    A98', qty='41.63', price='46.80', subtotal='1948.28'),
        ]

    def setUp(self):
        self.provider = pyofd.providers.first_ofd.ofd1OFD()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(signature=0, cash_machine_no=0, receipt_no=0))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(signature=2819037689, cash_machine_no=8710000100828376, receipt_no=87242))

    def test_valid_parse(self):
        result = self.provider.validate(signature=2819037689, cash_machine_no=8710000100828376, receipt_no=87242)
        self.assertEqual(self.valid_receipt_items, result)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(signature=2819037689, cash_machine_no=8710000100828376, receipt_no=87242)

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
