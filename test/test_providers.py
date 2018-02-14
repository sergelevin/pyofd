# -*- coding: utf-8 -*-

import unittest
import aiopyofd
from datetime import datetime
from asyncio import wait, Task, ALL_COMPLETED
from test import AsyncTestCase, sync

receipts_data = {
    'Taxcom': {
        'fpd': 1027455652,
        'total': 1487,
        'rn_kkt': 1482558031668,
        'fd': 9960,
        'inn': 7814148471,
        'purchase_date': datetime(year=2018, month=1, day=7, hour=14, minute=51)
    },
    'Platforma': {
        'fpd': 504931317,
        'total': '822.91',
        'fn': 8710000100186516,
        'rn_kkt': '0000051440037872',
        'fd': 136682,
        'inn': 5036045205,
        'purchase_date': datetime(year=2018, month=1, day=10, hour=17, minute=37)
    },
    '1-OFD': {
        'fpd': 2819037689,
        'total': '1948.28',
        'fn': 8710000100828376,
        'fd': 87242,
        'inn': 7840016802,
        'purchase_date': datetime(year=2017, month=9, day=30, hour=16, minute=7)
    },
    'Yarus': {
        'fpd': 4023651155,
        'total': '526.00',
        'rn_kkt': 691164058512,
        'fd': 34113,
        'inn': 7705814643,
        'purchase_date': datetime(year=2018, month=1, day=13, hour=20, minute=44)
    },
    'OfdRu': {
        'fpd': 2981623349,
        'total': 330,
        'rn_kkt': 489397013091,
        'fd': 7481,
        'inn': 7814339162,
        'fn': 8710000100617432,
        'purchase_date': datetime(year=2018, month=1, day=16, hour=13, minute=11)
    },
    'Yandex': {
        'fpd': 1637738986,
        'total': '301.35',
        'rn_kkt': 1563284018105,
        'fd': 144712,
        'inn': 7704340310,
        'purchase_date': datetime(year=2018, month=2, day=13, hour=20, minute=9)
    },
}


class ProvidersTest(AsyncTestCase):
    async def _test_single_provider(self, provider):
        self.assertIn(provider, receipts_data)
        kwargs = receipts_data[provider]
        receipt = aiopyofd.OFDReceipt(**kwargs)
        result = await receipt.load_receipt()

        self.assertIsNotNone(result)
        self.assertIsNotNone(receipt.provider)
        self.assertEqual(provider, receipt.provider.providerName)

    @sync
    async def test_taxcom(self):
        await self._test_single_provider('Taxcom')

    @sync
    async def test_platforma(self):
        await self._test_single_provider('Platforma')

    @sync
    async def test_first_ofd(self):
        await self._test_single_provider('1-OFD')

    @sync
    async def test_yarus(self):
        await self._test_single_provider('Yarus')

    @sync
    async def test_ofd_ru(self):
        await self._test_single_provider('OfdRu')

    @sync
    async def test_yandex(self):
        await self._test_single_provider('Yandex')

    @sync
    async def test_parallel(self):
        all_tasks = [Task(self._test_single_provider(k)) for k in receipts_data.keys()]
        await wait(all_tasks, loop=self.loop, return_when=ALL_COMPLETED)
        results = [task.result() for task in all_tasks]

