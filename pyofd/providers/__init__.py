# -*- coding: utf-8 -*-

"""
pyofd.providers
(c) Serge A. Levin, 2018
"""

from .providers import *

_ALL_CLASSES = [
    klass for
    name, klass in globals().items()
    if name.startswith('ofd')
]


def get_providers_classes():
    """

    :return: list of all known provider classes
    """
    return _ALL_CLASSES


def get_providers():
    """

    :return: list of instances of all known provider classes
    """
    return [klass() for klass in get_providers_classes()]
