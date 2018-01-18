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
        self.assertIsNone(self.provider.validate(fpd=0, fn=0, fd=0))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(fpd=2819037689, fn=8710000100828376, fd=87242))

    def test_valid_parse(self):
        result = self.provider.validate(fpd=2819037689, fn=8710000100828376, fd=87242)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(fpd=2819037689, fn=8710000100828376, fd=87242)

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
