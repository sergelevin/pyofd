# -*- coding: utf-8 -*-

import unittest
import aiopyofd.providers.ofd
import aiopyofd
from test import sync, AsyncTestCase


class OfdRuTest(AsyncTestCase):
    valid_receipt_items = [
        aiopyofd.ReceiptEntry(title='Салат"Новый русский"', qty=1, price=79 , subtotal=79 ),
        aiopyofd.ReceiptEntry(title='Бульон мал'          , qty=1, price=44 , subtotal=44 ),
        aiopyofd.ReceiptEntry(title='Рулетик куриный'     , qty=1, price=139, subtotal=139),
        aiopyofd.ReceiptEntry(title='Макароны'            , qty=1, price=45 , subtotal=45 ),
        aiopyofd.ReceiptEntry(title='Компот'              , qty=1, price=20 , subtotal=20 ),
        aiopyofd.ReceiptEntry(title='Хлеб'                , qty=1, price=3  , subtotal=3  ),
    ]

    def setUp(self):
        super(OfdRuTest, self).setUp()
        self.provider = aiopyofd.providers.ofd.ofdOfdRu()

    @sync
    async def test_provider_invalid(self):
        self.assertIsNone(await self.provider.validate(fpd='0'*10, rn_kkt='0'*16, inn='0'*10, fn='0'*16))

    @sync
    async def test_provider_minimal(self):
        self.assertIsNotNone(await self.provider.validate(fpd='2981623349', inn='7814339162', rn_kkt='0000489397013091', fn='8710000100617432'))

    @sync
    async def test_valid_parse(self):
        result = await self.provider.validate(fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432')
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    @sync
    async def test_provider(self):
        receipt = aiopyofd.OFDReceipt(fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432')

        result = await receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
