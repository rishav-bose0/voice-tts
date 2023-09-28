import time

import numpy

"""
This generates unique 14 alphanumeric characters to use as an Identifier for any entity. Logic used is same as in API
Service to make Razorpay Id consistent.

Logic: Last 4 characters are random generated. Rest is base 62 encoding of seed used, which is case sensitive alphabet
[52] and digits [10]). The decoded number is a unix timestamp since 1st Jan 2014.
"""


class UniqueIdGenerator(object):
    def __init__(self):
        # case sensitive alphabet [52] and digits [10]
        self.seed = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def generate_unique_id(self):
        nanotime = time.time_ns()
        return self.generate_unique_id_from_nanotime(nanotime)

    def generate_unique_id_from_nanotime(self, nanotime):
        b62 = self.nanotime_to_base62(nanotime)
        dec = int((numpy.random.bytes(5)).hex(), 16)
        rand = self.base62(dec)

        if len(rand) > 4:
            rand = rand[:-4]

        rand = rand.zfill(4)
        unique_id = b62 + rand

        return unique_id

    def nanotime_to_base62(self, nanotime):
        # Timestamp of 1st Jan 2014
        ts_1st_jan_2014 = 1388534400

        # Subtract nanotime of 1st jan 2014
        nanotime -= ts_1st_jan_2014 * 1000 * 1000 * 1000

        # Convert to base 62
        b62 = self.base62(nanotime)

        return b62

    def base62(self, num):
        index = self.seed

        res = ''

        while num:
            res = index[num % 62] + res
            num = int(num / 62)

        return res
