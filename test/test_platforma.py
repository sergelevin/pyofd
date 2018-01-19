# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.platforma
import pyofd
from decimal import Decimal
from datetime import datetime

class PlatformaTest(unittest.TestCase):
    valid_receipt_items = [
        pyofd.ReceiptEntry(title='КАРАМЕЛЬ ЧУПА ЧУПС ФРУКТОВАЯ В' , qty='2'    , price='7.19' , subtotal='14.38'),
        pyofd.ReceiptEntry(title='БАНАНЫ ВЕС'                     , qty='1.035', price='53.90', subtotal='55.79'),
        pyofd.ReceiptEntry(title='КРУАССАНЫ 7 DAYS МИНИ КАКАО 30' , qty='1'    , price='96.90', subtotal='96.90'),
        pyofd.ReceiptEntry(title='СЫРОК-СУФЛЕ ГЛАЗИР.ВАНИЛЬ Б.Ю.' , qty='6'    , price='44.90', subtotal='269.40'),
        pyofd.ReceiptEntry(title='СЫРОК ГЛ. Б.Ю.АЛЕКСАНДРОВ 26%'  , qty='1'    , price='31.43', subtotal='31.43'),
        pyofd.ReceiptEntry(title='СЫРОК ГЛ. Б.Ю.АЛЕКСАНДРОВ 26%'  , qty='1'    , price='31.43', subtotal='31.43'),
        pyofd.ReceiptEntry(title='ДРАЖЕ ТИК ТАК МЯТА/АПЕЛЬСИН 16' , qty='1'    , price='45.00', subtotal='45.00'),
        pyofd.ReceiptEntry(title='ДРАЖЕ ТИК ТАК МЯТА/АПЕЛЬСИН 16' , qty='1'    , price='45.00', subtotal='45.00'),
        pyofd.ReceiptEntry(title='ЙОГУРТ РАСТИШКА 3% КЛУБНИКА 11' , qty='2'    , price='17.99', subtotal='35.98'),
        pyofd.ReceiptEntry(title='ХЛЕБ РЖАНОЙ БУЛОЧНАЯ №1 ПОДОВЫ', qty='1'    , price='14.90', subtotal='14.90'),
        pyofd.ReceiptEntry(title='ХЛЕБ РЖАНОЙ НАР.415Г КР'        , qty='1'    , price='24.90', subtotal='24.90'),
        pyofd.ReceiptEntry(title='ЯЙЦО КИНДЕР СЮРПРИЗ ИЗ МОЛОЧ.Ш' , qty='2'    , price='78.90', subtotal='157.80'),
    ]

    alt_valid_receipt_items = [
        pyofd.ReceiptEntry(title='Kонструктор LEGO CITY "Грузовой вертолет исследователей джунглей', qty=1, price=1195, subtotal=1195.00),
        pyofd.ReceiptEntry(title='Kонструктор LEGO Elves "Тайная лечебница Розалин"(41187)', qty=1, price=3399, subtotal=3399.00),
        pyofd.ReceiptEntry(title='Пакет LEGO Medium(Medium)', qty=1, price=0, subtotal=0),
    ]

    def setUp(self):
        self.provider = pyofd.providers.platforma.ofdPlatforma()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(fpd=0, fn=0, fd=0))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(fpd=504931317, fn=8710000100186516, fd=136682))

    def test_valid_parse(self):
        result = self.provider.validate(fpd=504931317, fn=8710000100186516, fd=136682)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    def test_full_parse(self):
        result = self.provider.validate(fpd=504931317, fn=8710000100186516, fd=136682)
        self.assertIsNotNone(result)
        self.assertEqual('АО "Дикси Юг" Дикси-78722', result.seller_name)
        self.assertEqual('197022, г. Санкт-Петербург Каменноостровский пр-кт, д. 64, лит. А', result.seller_address)
        self.assertEqual('5036045205', result.inn)
        self.assertEqual(Decimal('822.91'), result.total)
        self.assertEqual('5036045205', result.inn)
        self.assertEqual('8710000100186516', result.fn)
        self.assertEqual('136682', result.fd)
        self.assertEqual('504931317', result.fpd)
        self.assertEqual(336, result.shift_no)
        self.assertEqual(233, result.receipt_no)
        self.assertEqual('КА Олейникова', result.cashier)
        self.assertEqual('0000051440037872', result.rn_kkt)
        self.assertEqual(datetime(year=2018, month=1, day=10, hour=17, minute=37), result.purchase_date)

    def test_alt_receipt(self):
        result = self.provider.validate(fpd=1154793488, fn=8710000100199134, fd=12659)
        self.assertIsNotNone(result)
        self.assertEqual(self.alt_valid_receipt_items, result.items)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(fpd=504931317, fn=8710000100186516, fd=136682)

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
