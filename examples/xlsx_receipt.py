# -*- coding: utf-8 -*-

"""
xlsx_receipt - PyOFD example to export single receipt to MS Excel workbook
(c) Serge A. Levin, 2018
"""


import pyofd
import argparse
import sys
import os
import urllib.parse
import datetime
import xlsxwriter
from pyofd.providers import NalogRu

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
                    'to standard output', default='-', required=True)

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

    nalog = NalogRu()
    nalog.apiLogin = os.environ.get('PYOFD_NALOGRU_LOGIN', None)
    nalog.apiPassword = os.environ.get('PYOFD_NALOGRU_PASSWORD', None)
    
    receipt = pyofd.OFDReceipt(**receipt_fields)
    result = receipt.load_receipt(check_providers=nalog) or receipt.load_receipt()

    if not result:
        sys.stderr.write('Receipt not found')
        return 1

    xlsx_properties = {
        'strings_to_numbers': True,
        'in_memory': True,
    }
    with xlsxwriter.Workbook(arguments.out_file_name, xlsx_properties) as out:
        worksheet = out.add_worksheet()
        data = []
        for entry in receipt.items:
            data.append([entry.title, entry.price, entry.quantity, entry.subtotal])

        first_row = 3
        nrows = len(data)
        last_row = first_row + nrows - 1
        rows_spec = 'A2:D{}'.format(last_row)
        worksheet.add_table(rows_spec, {
            'data': data,
            'columns': [
                {'header': 'Item'},
                {'header': 'Price'},
                {'header': 'Qty'},
                {'header': 'Subtotal'},
            ]
        })

        worksheet.write('F2', 'Part')
        worksheet.write_formula('F{}'.format(last_row+1),
                                '=SUMPRODUCT($D$3:$D${last_row},$F$3:$F${last_row})'.format(last_row=last_row))

        format = out.add_format({'bg_color': 'yellow'})
#        for row in range(first_row, last_row+1):
        row_spec = '$G{row}:$Z{row}'.format(row=first_row)
        format_range = '$G{first_row}:$Z{last_row}'.format(first_row=first_row, last_row=last_row)
        worksheet.conditional_format(format_range, {
            'type': 'formula',
            'criteria': '=SUM({row_spec})<>1'.format(row_spec=row_spec),
            'format': format,
        })

        for col in 'GHIJKLMNOPQRSTUVWXYZ':
            worksheet.write_formula('{col}{row}'.format(col=col, row=last_row+1),
                                    '=SUMPRODUCT($D$3:$D{last_row},${col}$3:${col}${last_row})'.format(col=col, last_row=last_row))
        worksheet.freeze_panes(2, 1)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
