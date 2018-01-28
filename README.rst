=========================================================
pyofd - Python library for interacting with OFD providers
=========================================================

.. image:: https://travis-ci.org/sergelevin/pyofd.svg?branch=master
    :target: https://travis-ci.org/sergelevin/pyofd

``pyofd`` is a Python package for receipts query from OFD providers.
It is inspired by `bobby_boy`_ project.

.. contents::

Installation
============

Install via `pip`_:

::

    $ pip install pyofd

Install from source:

::

    $ git clone git://github.com/sergelevin/pyofd.git
    $ cd pyofd
    $ python setup.py install

Usage
=====

Here is basic usage example.

::

    import pyofd, datetime

    receipt = pyofd.OFDReceipt(
        fpd='FPD', total='total', rn_kkt='RN_KKT', fn='FN',
        fd='FD', inn='INN', purchase_date=datetime.datetime.now()
    )
    result = receipt.load_receipt()

``OFDReceipt`` class might be constructed only with arguments known from receipt data, but omitting arguments
might narrow the list of OFD providers to be checked against, because different providers require different
subset of data to validate receipt

Examples
========

For some basic examples read unit tests in `test`_ directory. More complicated examples can be found within
`examples`_ directory.

* `load_receipt.py <https://github.com/sergelevin/pyofd/blob/master/examples/load_receipt.py>`_: Load receipt by
  known attributes and save items into tab-delimited file.
* `xlsx_receipt.py <https://github.com/sergelevin/pyofd/blob/master/examples/xlsx_receipt.py>`_: Load receipt by
  known attributes and export it to MS Excel (r) .xlsx file. If `nalog.ru <http://nalog.ru>`_ official receipt
  check application credentials are provided in ``PYOFD_NALOGRU_LOGIN`` and ``PYOFD_NALOGRU_PASSWORD`` environment
  variables, receipt lookup via ``NalogRu`` provider is also performed. Excel file is filled with formulas and
  conditional formatting suitable for my personal receipt handling needs - column *F* is for partial refund and
  columns *G* to *Z* - for receipt entries categorization with autocounting subtotal across categories.

.. _pip: https://pip.pypa.io/
.. _bobby_boy: https://github.com/ohbobbyboy/bobby_boy/
.. _test: https://github.com/sergelevin/pyofd/tree/master/test/
.. _examples: https://github.com/sergelevin/pyofd/tree/master/examples/

