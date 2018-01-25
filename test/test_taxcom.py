# -*- coding: utf-8 -*-

import unittest
import aiopyofd.providers.taxcom
import aiopyofd
from decimal import Decimal
from datetime import datetime
from test import sync, AsyncTestCase


class TaxcomTest(AsyncTestCase):
    valid_receipt_items = [
            aiopyofd.ReceiptEntry(title='Яйцо шок KINDER SURPRISE мол шок 20г'    , qty=2, price='69.89', subtotal='139.78'),
            aiopyofd.ReceiptEntry(title='Молоко ПРОСТОКВАШ отб ПЭТ 3,4-4,5% 930мл', qty=2, price='76.99', subtotal='153.98'),
            aiopyofd.ReceiptEntry(title='Гот завтрак NESTLE Nesquik пак 250г'     , qty=2, price='98.99', subtotal='197.98'),
            aiopyofd.ReceiptEntry(title='Морковь мытая п/э 1000г'                 , qty=1, price='39.99', subtotal='39.99'),
            aiopyofd.ReceiptEntry(title='Салат дуболистный зеленый в горшочке 1шт', qty=1, price='49.99', subtotal='49.99'),
            aiopyofd.ReceiptEntry(title='Сырок глаз АЛЕКСАНДРОВ мол шок ван26%50г', qty=7, price='39.91', subtotal='279.37'),
            aiopyofd.ReceiptEntry(title='Колбаса ПИТ ПРОДУКТ Докт вар ГОСТ400г'   , qty=1, price='268.99', subtotal='268.99'),
            aiopyofd.ReceiptEntry(title='Журнал За рулем'                         , qty=1, price='99.99', subtotal='99.99'),
            aiopyofd.ReceiptEntry(title='Хлеб КАРАВАЙ Столовый рж-пш полов 375г'  , qty=1, price='30.89', subtotal='30.89'),
            aiopyofd.ReceiptEntry(title='Батон КАРАВАЙ Наше солныш нарезн рез195' , qty=1, price='31.89', subtotal='31.89'),
            aiopyofd.ReceiptEntry(title='Конц-т пищ СУПЕРСУП горох с бекон 70г'   , qty=2, price='36.59', subtotal='73.18'),
            aiopyofd.ReceiptEntry(title='Суп б/п MAGGI Звезд сух/, обогащ.жел.54г', qty=2, price='15.99', subtotal='31.98'),
            aiopyofd.ReceiptEntry(title='Чай ПРИНЦЕССА КАНДИ Медиум лист. 200г'   , qty=1, price='88.99', subtotal='88.99'),
        ]

    def setUp(self):
        super(TaxcomTest, self).setUp()
        self.provider = aiopyofd.providers.taxcom.ofdTaxcom()

    @sync
    async def test_provider_invalid(self):
        self.assertIsNone(await self.provider.validate(fpd=0, total=0))

    @sync
    async def test_provider_minimal(self):
        self.assertIsNotNone(await self.provider.validate(fpd=1027455652, total=1487))

    @sync
    async def test_valid_parse(self):
        result = await self.provider.validate(fpd=1027455652, total=1487)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    @sync
    async def test_full_parse(self):
        result = await self.provider.validate(fpd=1027455652, total=1487)
        self.assertIsNotNone(result)
        self.assertEqual('ООО "Лента"', result.seller_name)
        self.assertEqual('197022, Санкт-Петербург, пр. Чкаловский, д. 50, ЛИТ.Б.', result.seller_address)
        self.assertEqual('7814148471', result.inn)
        self.assertEqual(Decimal('1487.00'), result.total)
        self.assertEqual('8710000101263672', result.fn)
        self.assertEqual(9960, result.fd)
        self.assertEqual('1027455652', result.fpd)
        self.assertEqual(43, result.shift_no)
        self.assertEqual(78, result.receipt_no)
        self.assertEqual('Кудаева Герта Харитоновна', result.cashier)
        self.assertEqual('0001482558031668', result.rn_kkt)
        self.assertEqual(datetime(year=2018, month=1, day=7, hour=14, minute=51), result.purchase_date)

    @sync
    async def test_provider(self):
        receipt = aiopyofd.OFDReceipt(fpd=1027455652, total=1487)

        result = await receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
