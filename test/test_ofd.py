# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.ofd
import pyofd


class OfdRuTest(unittest.TestCase):
    valid_receipt_items = [
        pyofd.ReceiptEntry(title='Салат"Новый русский"', qty='1.0', price='79.00' , subtotal='79.00' ),
        pyofd.ReceiptEntry(title='Бульон мал'          , qty='1.0', price='44.00' , subtotal='44.00' ),
        pyofd.ReceiptEntry(title='Рулетик куриный'     , qty='1.0', price='139.00', subtotal='139.00'),
        pyofd.ReceiptEntry(title='Макароны'            , qty='1.0', price='45.00' , subtotal='45.00' ),
        pyofd.ReceiptEntry(title='Компот'              , qty='1.0', price='20.00' , subtotal='20.00' ),
        pyofd.ReceiptEntry(title='Хлеб'                , qty='1.0', price='3.00'  , subtotal='3.00'  ),
    ]

    def setUp(self):
        self.provider = pyofd.providers.ofd.ofdOfdRu()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(fpd='0'*10, rn_kkt='0'*16, inn='0'*10, fn='0'*16))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(fpd='2981623349', inn='7814339162', rn_kkt='0000489397013091', fn='8710000100617432'))

    def test_valid_parse(self):
        result = self.provider.validate(fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432')
        self.assertEqual(self.valid_receipt_items, result)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432')

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
