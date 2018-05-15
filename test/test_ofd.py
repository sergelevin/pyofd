# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.ofd
import pyofd


class OfdRuTest(unittest.TestCase):
    valid_receipt_items = [
        pyofd.ReceiptEntry(title='Салат"Новый русский"', qty=1, price=79 , subtotal=79 ),
        pyofd.ReceiptEntry(title='Бульон мал'          , qty=1, price=44 , subtotal=44 ),
        pyofd.ReceiptEntry(title='Рулетик куриный'     , qty=1, price=139, subtotal=139),
        pyofd.ReceiptEntry(title='Макароны'            , qty=1, price=45 , subtotal=45 ),
        pyofd.ReceiptEntry(title='Компот'              , qty=1, price=20 , subtotal=20 ),
        pyofd.ReceiptEntry(title='Хлеб'                , qty=1, price=3  , subtotal=3  ),
    ]

    def setUp(self):
        self.provider = pyofd.providers.ofd.ofdOfdRu()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(fpd='0'*10, rn_kkt='0'*16, inn='0'*10, fn='0'*16, fd=0))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(fpd='2981623349', inn='7814339162', rn_kkt='0000489397013091', fn='8710000100617432', fd=7481))

    def test_valid_parse(self):
        result = self.provider.validate(fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432', fd=7481)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432', fd=7481)

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)

    def test_issue_1(self):
        '''
        Test case for https://github.com/sergelevin/pyofd/issues/1
        '''
        self.assertIsNotNone(self.provider.validate(fpd='1626880333', inn='7825439514', rn_kkt='0000520679026739', fn='8710000100767988', fd=160669))
