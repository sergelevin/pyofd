# -*- coding: utf-8 -*-

"""
load_receipt - PyOFD example to export single receipt to tab-delimited file
(c) Serge A. Levin, 2018
"""


import pyofd
import argparse
import sys
import os
import urllib.parse
import datetime

parser = argparse.ArgumentParser(description='Example script to export receipt to tab-delimited file')
parser.add_argument('-fp', '-fpd',
                    dest='fpd', help='Fiscal document fpd, also known as FPD')
parser.add_argument('-s', '--sum', '--total',
                    dest='total', help='Receipt total')
parser.add_argument('-i', '-fd',
                    dest='fd', help='Receipt number, also known as FD')
parser.add_argument('-fn',
                    dest='fn', help='Receipt fiscal number, also known as FN')
parser.add_argument('-inn',
                    dest='inn', help='Merchant taxpayer ID (INN)')
parser.add_argument('-kkt',
                    dest='rn_kkt', help='Cash machine registration number, also known as RN KKT')
parser.add_argument('-d', '--datetime',
                    dest='purchase_date', help='Date and time of purchase')
parser.add_argument('-url',
                    dest='url', help='URL from recognized QR-code')

parser.add_argument('-o', '--output',
                    dest='out_file_name', help='File name to write receipt data to. Desfault is to write'
                    'to standard output', default='-')

fields = ('fpd', 'total', 'fd', 'inn', 'rn_kkt', 'fn')


def smart_open(filename):
    if filename and filename != '-':
        return open(filename, mode='w')
    else:
        return os.fdopen(os.dup(sys.stdout.fileno()), 'w')


def parse_date_time(date_time_str):
    try:
        return datetime.datetime.strptime(date_time_str, '%Y%m%dT%H%M%S')
    except ValueError:
        return datetime.datetime.strptime(date_time_str, '%Y%m%dT%H%M')


def parse_url(url):
    mapping = {
        # first go standard fields. Date and time is parsed separately below
        's': 'total', 'fn': 'fn', 'i': 'fd', 'fp': 'fpd',
        # then - nonstandard, but used by providers
        'inn': 'inn', 'rn_kkt': 'rn_kkt'
    }
    fields = urllib.parse.parse_qs(url)

    result = {v: fields[k][0] for k, v in mapping.items() if k in fields}
    if 't' in fields:
        result['purchase_date'] = parse_date_time(fields['t'][0])
    return result


def main(argv):
    arguments = parser.parse_args(argv)
    receipt_fields = {k: getattr(arguments, k)
                      for k in fields
                      if hasattr(arguments, k) and getattr(arguments, k) is not None}
    date_time_str = getattr(arguments, 'purchase_date', None)
    if date_time_str is not None:
        receipt_fields['purchase_date'] = parse_date_time(date_time_str)
    url = getattr(arguments, 'url', None)
    if url is not None:
        receipt_fields.update(parse_url(url))

    receipt = pyofd.OFDReceipt(**receipt_fields)
    result = receipt.load_receipt()

    if not result:
        sys.stderr.write('Receipt not found')
        return 1

    with smart_open(arguments.out_file_name) as out:
        for entry in receipt.items:
            out.write('{title}\t{price}\t{qty}\t{subtotal}\n'.format(
                title=entry.title, price=entry.price, qty=entry.quantity, subtotal=entry.subtotal))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
