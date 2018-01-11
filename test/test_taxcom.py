# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.taxcom
import pyofd

class TaxcomTest(unittest.TestCase):
    valid_receipt_items = [
            pyofd.ReceiptEntry(title='Яйцо шок KINDER SURPRISE мол шок 20г'    , qty='2.000', price='69.89', subtotal='139.78'),
            pyofd.ReceiptEntry(title='Молоко ПРОСТОКВАШ отб ПЭТ 3,4-4,5% 930мл', qty='2.000', price='76.99', subtotal='153.98'),
            pyofd.ReceiptEntry(title='Гот завтрак NESTLE Nesquik пак 250г'     , qty='2.000', price='98.99', subtotal='197.98'),
            pyofd.ReceiptEntry(title='Морковь мытая п/э 1000г'                 , qty='1.000', price='39.99', subtotal='39.99'),
            pyofd.ReceiptEntry(title='Салат дуболистный зеленый в горшочке 1шт', qty='1.000', price='49.99', subtotal='49.99'),
            pyofd.ReceiptEntry(title='Сырок глаз АЛЕКСАНДРОВ мол шок ван26%50г', qty='7.000', price='39.91', subtotal='279.37'),
            pyofd.ReceiptEntry(title='Колбаса ПИТ ПРОДУКТ Докт вар ГОСТ400г'   , qty='1.000', price='268.99', subtotal='268.99'),
            pyofd.ReceiptEntry(title='Журнал За рулем'                         , qty='1.000', price='99.99', subtotal='99.99'),
            pyofd.ReceiptEntry(title='Хлеб КАРАВАЙ Столовый рж-пш полов 375г'  , qty='1.000', price='30.89', subtotal='30.89'),
            pyofd.ReceiptEntry(title='Батон КАРАВАЙ Наше солныш нарезн рез195' , qty='1.000', price='31.89', subtotal='31.89'),
            pyofd.ReceiptEntry(title='Конц-т пищ СУПЕРСУП горох с бекон 70г'   , qty='2.000', price='36.59', subtotal='73.18'),
            pyofd.ReceiptEntry(title='Суп б/п MAGGI Звезд сух/, обогащ.жел.54г', qty='2.000', price='15.99', subtotal='31.98'),
            pyofd.ReceiptEntry(title='Чай ПРИНЦЕССА КАНДИ Медиум лист. 200г'   , qty='1.000', price='88.99', subtotal='88.99'),
        ]

    def setUp(self):
        self.provider = pyofd.providers.taxcom.ofdTaxcom()

    def test_provider_invalid(self):
        self.assertIsNone(self.provider.validate(signature=0, total=0))

    def test_provider_minimal(self):
        self.assertIsNotNone(self.provider.validate(signature=1027455652, total=1487))

    def test_valid_parse(self):
        result = self.provider.validate(signature=1027455652, total=1487)
        self.assertEqual(self.valid_receipt_items, result)

    def test_provider(self):
        receipt = pyofd.OFDReceipt(signature=1027455652, total=1487)

        result = receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
