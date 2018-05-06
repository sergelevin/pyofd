# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.kontur
import pyofd


class KonturTest(unittest.TestCase):
    valid_receipt_items = [
        pyofd.ReceiptEntry(title='Мясная (трад, 23 см)'      , qty=1, price='419.00', subtotal=419),
        pyofd.ReceiptEntry(title='Пицца Джона (трад, 23 см)' , qty=1, price='419.00', subtotal=419),
    ]

    def setUp(self):
        self.provider = pyofd.providers.kontur.ofdKontur()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(fpd='0'*10, fn='0'*16, fd=0))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(fpd='1753141947', fn='8710000101500109', fd=3250))

    def test_valid_parse(self):
        result = self.provider.validate(fpd='1753141947', fn='8710000101500109', fd=3250)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(fpd='1753141947', fn='8710000101500109', fd=3250)

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
