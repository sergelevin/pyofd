# -*- coding: utf-8 -*-

"""
load_receipt - PyOFD example to export single receipt to tab-delimited file
(c) Serge A. Levin, 2018
"""


import pyofd
import argparse
import sys
import os

parser = argparse.ArgumentParser(description='Example script to export receipt to tab-delimited file')
parser.add_argument('-fp', '--signature', '--fpd',
                    dest='signature', help='Fiscal document signature, also known as FPD', required=True)
parser.add_argument('-s', '--sum', '--total',
                    dest='total', help='Receipt total')
parser.add_argument('-i', '-fd',
                    dest='receipt_no', help='Receipt number, also known as FD')
parser.add_argument('-fn',
                    dest='fiscal_no', help='Receipt fiscal number, also known as FN')
parser.add_argument('-inn', '--taxpayer',
                    dest='taxpayer_id', help='Merchant taxpayer ID (INN)')
parser.add_argument('-kkt', '--cash-machine-number',
                    dest='cash_machine_no', help='Cash machine registration number, also known as RN KKT')

parser.add_argument('-o', '--output',
                    dest='out_file_name', help='File name to write receipt data to. Desfault is to write'
                    'to standard output', default='-')

fields = ('signature', 'total', 'receipt_no', 'taxpayer_id', 'cash_machine_no')


def smart_open(filename):
    if filename and filename != '-':
        return open(filename, mode='w')
    else:
        return os.fdopen(os.dup(sys.stdout.fileno()), 'w')

def main(argv):
    arguments = parser.parse_args(argv)
    receipt_fields = {k: getattr(arguments, k) for k in fields if hasattr(arguments, k)}

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
