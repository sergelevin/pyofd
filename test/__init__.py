# -*- coding: utf-8 -*-


from os import listdir
from os.path import dirname
import unittest
from asyncio import get_event_loop, set_event_loop, sleep, new_event_loop


def sync(coro):
    def wrapper(*args, **kwargs):
        loop = get_event_loop()
        loop.run_until_complete(coro(*args, **kwargs))
    return wrapper


class AsyncTestCase(unittest.TestCase):
    def setUp(self):
        self.loop = new_event_loop()
        set_event_loop(self.loop)

    def tearDown(self):
        # See https://github.com/aio-libs/aiohttp/issues/1115
        self.loop.run_until_complete(sleep(0.1, loop=self.loop))
        self.loop.close()
        set_event_loop(None)
        self.loop = None


def test_suite():
    suite = unittest.TestSuite()
    base = dirname(__file__)
    for file in listdir(base):
        if file.startswith("test_") and file.endswith(".py"):
            module_name = "test." + file[:-3]
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module_name))

    return suite


def run_tests():
    unittest.main(defaultTest='test.test_suite')
