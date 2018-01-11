# -*- coding: utf-8 -*-


from os import listdir
from os.path import dirname
import unittest


def load_tests():
    suite = unittest.TestSuite()
    base = dirname(__file__)
    for file in listdir(base):
        if file.startswith("test_") and file.endswith(".py"):
            module_name = "test." + file[:-3]
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module_name))

    return suite


def run_tests():
    unittest.main(defaultTest='test.load_tests')
