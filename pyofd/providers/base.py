# -*- coding: utf-8 -*-

"""
pyofd.providers.base

Base OFD provider. Concrete OFD providers should inherit from this base and have a name like ofdXXX
(c) Serge A. Levin, 2018
"""

import urllib.parse as _parse
import urllib.request as _request
import io


class Base:
    """Base class for simple sessionless OFD provider checker

    Performs single HTTP GET request to OFD provider website and tries to load receipt details from response
    """

    providerName = None
    """Human-readable OFD provider name 
    """

    urlTemplate = ''
    """URL to test receipt for validity. It may contain py-format placeholders
    for the fields identifying receipt.
    
    For any field with *name* field *q_name* is generated with URL-quoted value
    
    Used by @validate method
    """
    requiredFields = ()
    """Tuple of field names to be not None for the provider to try validating receipt
    
    Used by @is_candidate method 
    """

    def __init__(self):
        pass

    def is_candidate(self, **kwargs):
        """Checks whether receipt is handled by current OFD providers

        Basic check requires all the fields specified in @requiredFields are not None

        :param kwargs:  Receipt identification fields with their values
        :return: Boolean value indicating whether receipt is candidate to be handled by current OFD provider
        """
        for field in self.requiredFields:
            if field not in kwargs or kwargs[field] is None:
                return False

        return True

    def get_request_url(self, **context):
        """ Builds URL or Request object for the OFD

        :param context: receipt parameters with their url-quoted version
        :return: built URL
        """
        return self.urlTemplate.format(**context)

    def validate(
            self,
            fpd=None,
            total=None,
            rn_kkt=None,
            fd=None,
            fn=None,
            inn=None,
            purchase_date=None,
    ):
        """ Tries to load receipt detail from OFD provider website

        :param fpd: Receipt signature (FPD in terms of Tax service of Russia)
        :param total: Receipt total
        :param rn_kkt: Cash machine serial number (RN KKT)
        :param fd: Receipt number (FD)
        :param fn: Receipt fiscal number (FN)
        :param inn: Seller's taxpayer identifier (INN)
        :param purchase_date: Purchase date and time
        """
        context = {k: v for k, v in locals().items() if k != 'self'}

        q_context = { ('q_' + k): _parse.quote(str(v)) for k, v in context.items() if v is not None}
        context.update(q_context)

        url = self.get_request_url(**context)

        try:
            response = _request.urlopen(url)
        except IOError:
            return None

        if response.getcode() != 200:
            return None

        data = response.read()

        try:
            return self.parse_response(io.BytesIO(data))
        except:
            return None

    def parse_response(self, data):
        """overridable to try parsing data, received from server

        :param data: BytesIO with data to be parsed
        :return: list of pyofd.ReceiptEntry if data is recognised
        """
        pass
