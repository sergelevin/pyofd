# -*- coding: utf-8 -*-

import unittest
import pyofd.providers.nalog
import pyofd
import pyofd.providers
import os


class NalogRuTest(unittest.TestCase):
    valid_receipt_items = [
        pyofd.ReceiptEntry(title='Салат"Новый русский"', qty=1, price=79 , subtotal=79 ),
        pyofd.ReceiptEntry(title='Бульон мал'          , qty=1, price=44 , subtotal=44 ),
        pyofd.ReceiptEntry(title='Рулетик куриный'     , qty=1, price=139, subtotal=139),
        pyofd.ReceiptEntry(title='Макароны'            , qty=1, price=45 , subtotal=45 ),
        pyofd.ReceiptEntry(title='Компот'              , qty=1, price=20 , subtotal=20 ),
        pyofd.ReceiptEntry(title='Хлеб'                , qty=1, price=3  , subtotal=3  ),
    ]

    @classmethod
    def setUpClass(cls):
        pyofd.providers.nalog.NalogRu.apiLogin = os.environ.get('PYOFD_NALOGRU_LOGIN', None)
        pyofd.providers.nalog.NalogRu.apiPassword = os.environ.get('PYOFD_NALOGRU_PASSWORD', None)

    @classmethod
    def tearDownClass(cls):
        pyofd.providers.nalog.NalogRu.apiLogin = None
        pyofd.providers.nalog.NalogRu.apiPassword = None

    def setUp(self):
        self.provider = pyofd.providers.nalog.NalogRu()

    def _skip_if_no_credentials(self):
        if pyofd.providers.nalog.NalogRu.apiLogin is None or pyofd.providers.nalog.NalogRu.apiPassword is None:
            raise unittest.SkipTest('Nalog.Ru credentials not provided')

    def test_class(self):
        self.assertEqual(self.provider.__class__, pyofd.providers.NalogRu)

    def test_provider_invalid(self):
        self._skip_if_no_credentials()
        self.assertIsNone(self.provider.validate(fpd='0'*10, rn_kkt='0'*16, inn='0'*10, fn='0'*16, fd=0))

    def test_provider_minimal(self):
        self._skip_if_no_credentials()
        self.assertIsNotNone(self.provider.validate(
            fpd='2981623349', inn='7814339162', rn_kkt='0000489397013091', fn='8710000100617432', fd=7481))

    def test_valid_parse(self):
        self._skip_if_no_credentials()
        result = self.provider.validate(
            fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432', fd=7481)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    def test_provider(self):
        self._skip_if_no_credentials()
        receipt = pyofd.OFDReceipt(
            fpd='2981623349', rn_kkt='0000489397013091', inn='7814339162', fn='8710000100617432', fd=7481)

        result = receipt.load_receipt(check_providers = self.provider)

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
