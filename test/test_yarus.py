# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.yarus
import pyofd


class YarusTest(unittest.TestCase):
    valid_receipt_items = [
        pyofd.ReceiptEntry(title='GR   10 г №0047 зеленый Артиkул 372426421'    , qty=2, price='16.00' , subtotal='32.00' ),
        pyofd.ReceiptEntry(title='мm  50 m №03 пoд св.mе дь Apтикул 4319338852' , qty=2, price='160.10', subtotal='320.20'),
        pyofd.ReceiptEntry(title='GR   10 г №0142 kрemoвый Аpт икул 972482351'  , qty=1, price='16.38' , subtotal='16.38' ),
        pyofd.ReceiptEntry(title='0 г №0109А св.пeрсиkовый Аpти кул 10360008322', qty=1, price='16.38' , subtotal='16.38' ),
        pyofd.ReceiptEntry(title='GR   10 г №0053 koринчeвый Apтиkул 972344641' , qty=1, price='16.38' , subtotal='16.38' ),
        pyofd.ReceiptEntry(title='33 мm бoльшиe/в блист eрe Aртиkул 1754871892'  , qty=1, price='108.29', subtotal='108.29'),
        pyofd.ReceiptEntry(title='GR   10 г №0012М сеpый Aртиkул 10359922602'   , qty=1, price='16.37' , subtotal='16.37' ),
    ]

    def setUp(self):
        self.provider = pyofd.providers.yarus.ofdYarus()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(fpd='0'*10, rn_kkt='0'*16))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(fpd='4023651155', rn_kkt='0000691164058512'))

    def test_valid_parse(self):
        result = self.provider.validate(fpd='4023651155', rn_kkt='0000691164058512')
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(fpd='4023651155', rn_kkt='0000691164058512')

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
