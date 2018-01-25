=========================================================
pyofd - Python library for interacting with OFD providers
=========================================================

.. image:: https://travis-ci.org/sergelevin/pyofd.svg?branch=master
    :target: https://travis-ci.org/sergelevin/pyofd

.. image:: https://travis-ci.org/sergelevin/pyofd.svg?branch=aiopyofd
    :target: https://travis-ci.org/sergelevin/pyofd

``pyofd`` is a Python package for receipts query from OFD providers.
It is inspired by `bobby_boy`_ project.

There are two development branches of the library:

* `master <https://github.com/sergelevin/pyofd/tree/master>` is the main development branch. It is intended for
  conventional synchronous operations.
* `aiopyofd <https://github.com/sergelevin/pyofd/tree/aiopyofd>` is the development branch for pyofd, taking use
  of ``asyncio`` and ``aiohttp`` packages. It requires Python 3.5+ to run as it uses syntax sugar introduced in this
  version.

.. contents::

Installation
============

Install via `pip`_:

..::
..
..    $ pip install aiopyofd
..

Install from source:

::

    $ git clone git://github.com/sergelevin/pyofd.git
    $ cd pyofd
    $ git checkout -b aiopyofd origin/aiopyofd
    $ python setup.py install

Usage
=====

Here is basic usage example.

::

    import aiopyofd, datetime

    receipt = aiopyofd.OFDReceipt(
        fpd='FPD', total='total', rn_kkt='RN_KKT', fn='FN',
        fd='FD', inn='INN', purchase_date=datetime.datetime.now()
    )
    result = await receipt.load_receipt()

``OFDReceipt`` class might be constructed only with arguments known from receipt data, but omitting arguments
might narrow the list of OFD providers to be checked against, because different providers require different
subset of data to validate receipt

Examples
========

For some basic examples read unit tests in `test`_ directory. More complicated examples can be found within
`examples`_ directory.

* `load_receipt.py <https://github.com/sergelevin/pyofd/blob/aiopyofd/examples/load_receipt.py>`_: Load receipt by
  known attributes and save items into tab-delimited file.
* `xlsx_receipt.py <https://github.com/sergelevin/pyofd/blob/aiopyofd/examples/xlsx_receipt.py>`_: Load receipt by
  known attributes and export it to MS Excel (r) .xlsx file. If `nalog.ru <http://nalog.ru>`_ official receipt
  check application credentials are provided in ``PYOFD_NALOGRU_LOGIN`` and ``PYOFD_NALOGRU_PASSWORD`` environment
  variables, receipt lookup via ``NalogRu`` provider is also performed. Excel file is filled with formulas and
  conditional formatting suitable for my personal receipt handling needs - column *F* is for partial refund and
  columns *G* to *Z* - for receipt entries categorization with autocounting subtotal across categories.

.. _pip: https://pip.pypa.io/
.. _bobby_boy: https://github.com/ohbobbyboy/bobby_boy/
.. _test: https://github.com/sergelevin/pyofd/tree/master/test/
.. _examples: https://github.com/sergelevin/pyofd/tree/master/examples/

