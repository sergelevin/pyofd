# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.yandex
import pyofd
from decimal import Decimal
from datetime import datetime

class YandexTest(unittest.TestCase):
    valid_receipt_items = [
            pyofd.ReceiptEntry(title='Перевозка пассажиров и багажа', qty=1, price='287.00', subtotal='287.00'),
            pyofd.ReceiptEntry(title='Перевозка пассажиров и багажа', qty=1, price='14.35' , subtotal='14.35' ),
        ]

    def setUp(self):
        self.provider = pyofd.providers.yandex.ofdYandex()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(rn_kkt=0, fd=0, fpd=0))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(rn_kkt=1563284018105, fd=144712, fpd=1637738986))

    def test_valid_parse(self):
        result = self.provider.validate(rn_kkt=1563284018105, fd=144712, fpd=1637738986)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    def test_full_parse(self):
        result = self.provider.validate(rn_kkt=1563284018105, fd=144712, fpd=1637738986)
        self.assertIsNotNone(result)
        self.assertEqual('ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ЯНДЕКС.ТАКСИ"', result.seller_name)
        self.assertEqual('Московская обл, г Ивантеевка, ул Заречная, д 1', result.seller_address)
        self.assertEqual('7704340310', result.inn)
        self.assertEqual(Decimal('301.35'), result.total)
        self.assertEqual('8710000101117311', result.fn)
        self.assertEqual('1637738986', result.fpd)
        self.assertEqual('undefined', result.cashier)
        self.assertEqual('0001563284018105', result.rn_kkt)
        self.assertEqual(datetime(year=2018, month=2, day=13, hour=20, minute=9), result.purchase_date)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(rn_kkt=1563284018105, fd=144712, fpd=1637738986)

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
