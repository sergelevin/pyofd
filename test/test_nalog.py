# -*- coding: utf-8 -*-

import unittest
import aiopyofd.providers.nalog
import aiopyofd
import aiopyofd.providers
import os
from test import sync, AsyncTestCase


class NalogRuTest(AsyncTestCase):
    valid_receipt_items = [
        aiopyofd.ReceiptEntry(title='Салат"Новый русский"', qty=1, price=79 , subtotal=79 ),
        aiopyofd.ReceiptEntry(title='Бульон мал'          , qty=1, price=44 , subtotal=44 ),
        aiopyofd.ReceiptEntry(title='Рулетик куриный'     , qty=1, price=139, subtotal=139),
        aiopyofd.ReceiptEntry(title='Макароны'            , qty=1, price=45 , subtotal=45 ),
        aiopyofd.ReceiptEntry(title='Компот'              , qty=1, price=20 , subtotal=20 ),
        aiopyofd.ReceiptEntry(title='Хлеб'                , qty=1, price=3  , subtotal=3  ),
    ]

    @classmethod
    def setUpClass(cls):
        aiopyofd.providers.nalog.NalogRu.apiLogin = os.environ.get('PYOFD_NALOGRU_LOGIN', None)
        aiopyofd.providers.nalog.NalogRu.apiPassword = os.environ.get('PYOFD_NALOGRU_PASSWORD', None)

    @classmethod
    def tearDownClass(cls):
        aiopyofd.providers.nalog.NalogRu.apiLogin = None
        aiopyofd.providers.nalog.NalogRu.apiPassword = None

    def setUp(self):
        super(NalogRuTest, self).setUp()
        self.provider = aiopyofd.providers.nalog.NalogRu()

    @staticmethod
    def _skip_if_no_credentials():
        if aiopyofd.providers.nalog.NalogRu.apiLogin is None or aiopyofd.providers.nalog.NalogRu.apiPassword is None:
            raise unittest.SkipTest('Nalog.Ru credentials not provided')

    @sync
    async def test_class(self):
        self.assertEqual(self.provider.__class__, aiopyofd.providers.NalogRu)

    @sync
    async def test_provider_invalid(self):
        self._skip_if_no_credentials()
        self.assertIsNone(await self.provider.validate(fpd='0'*10, rn_kkt='0'*16, inn='0'*10, fn='0'*16, fd=0))

    @sync
    async def test_provider_minimal(self):
        self._skip_if_no_credentials()
        self.assertIsNotNone(await self.provider.validate(
            fpd='2981623349', inn='7814339162', rn_kkt='0000489397013091', fn='8710000100617432', fd=7481))

    @sync
    async def test_valid_parse(self):
        self._skip_if_no_credentials()
        result = await self.provider.validate(
            fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432', fd=7481)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    @sync
    async def test_provider(self):
        self._skip_if_no_credentials()
        receipt = aiopyofd.OFDReceipt(
            fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432', fd=7481)

        result = await receipt.load_receipt(check_providers = self.provider)

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
