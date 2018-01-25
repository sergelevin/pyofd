# -*- coding: utf-8 -*-

import aiopyofd.providers.first_ofd
import aiopyofd
from test import sync, AsyncTestCase


class FirstOFDTest(AsyncTestCase):
    valid_receipt_items = [
            aiopyofd.ReceiptEntry(title='ТРК -  3    A98', qty='41.63', price='46.80', subtotal='1948.28'),
        ]

    def setUp(self):
        super(FirstOFDTest, self).setUp()
        self.provider = aiopyofd.providers.first_ofd.ofd1OFD()

    @sync
    async def test_provider_invalid(self):
        self.assertIsNone(await self.provider.validate(fpd=0, fn=0, fd=0))

    @sync
    async def test_provider_minimal(self):
        self.assertIsNotNone(await self.provider.validate(fpd=2819037689, fn=8710000100828376, fd=87242))

    @sync
    async def test_valid_parse(self):
        result = await self.provider.validate(fpd=2819037689, fn=8710000100828376, fd=87242)
        self.assertIsNotNone(result)
        self.assertEqual(self.valid_receipt_items, result.items)

    @sync
    async def test_provider(self):
        receipt = aiopyofd.OFDReceipt(fpd=2819037689, fn=8710000100828376, fd=87242)

        result = await receipt.load_receipt()

        self.assertEqual(True, result)
        self.assertIs(receipt.provider.__class__, self.provider.__class__)
        self.assertEqual(self.valid_receipt_items, receipt.items)
