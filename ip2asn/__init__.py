#!/usr/bin/python3

"""Reads an ip2asn file into memory, and uses the data to extract
information about an address.

Usage:
    Prep:

    curl -o ip2asn-v4-u32.tsv.gz https://iptoasn.com/data/ip2asn-v4-u32.tsv.gz
    gunzip ip2asn-v4-u32.tsv.gz
    pip3 install ip2asn

    Code:

    import ip2asn
    i2a = ip2asn.IP2ASN("ip2asn-v4-u32.tsv")
    result = i2a.lookup_address("93.184.216.34")
    print(result)
"""

import pyfsdb
import ipaddress
from bisect import bisect

class IP2ASN():
    """A container for accessing data within an ip2asn file"""
    def __init__(self, ip2asn_file, ipversion=4):
        self._file = ip2asn_file
        self._version = ipversion

        self.read_data()

    def read_data(self):
        """Read data from the ip2asn file"""
        if isinstance(self._file, str):
            # assume a file name
            iptoasn = pyfsdb.Fsdb(self._file)
        else:
            # assume it's a file handle instead
            iptoasn = pyfsdb.Fsdb(file_handle = self._file)

        # set the column names for pyfsdb
        iptoasn.column_names = ['start','end','ASN', 'country','name']

        (self._start_col, self._end_col,
         self._asn_col, self._country_col,
         self._name_col) = iptoasn.get_column_numbers(iptoasn.column_names)

        # XXX: fsdb should do this for us
        self._data = []
        self._left_keys = []
        for row in iptoasn:
            try:
                row[self._start_col] = int(row[self._start_col])
                row[self._end_col] = int(row[self._end_col])
            except:
                # must be addresses not ints
                row[self._start_col] = self.ip2int(row[self._start_col])
                row[self._end_col] = self.ip2int(row[self._end_col])

            self._data.append(row)
            self._left_keys.append(int(row[self._start_col]))

    def ip2int(self, address, version=None):
        """Converts an ascii represented IPv4 or IPv6 address into an
           integer.  If the ipversion isn't specified (4 or 6), it
           will attempt to guess based on whether the address has 
           a ':' character in it"""
        if version is None:
            version = self._version
        if self._version == 4:
            ip = int(ipaddress.IPv4Address(address))
        elif self._version == 6:
            ip = int(ipaddress.IPv6Address(address))
        else:
            if address.find(":") != -1:
                ip = int(ipaddress.IPv6Address(address))
            else:
                ip = int(ipaddress.IPv4Address(address))
        return ip

    def lookup_address_row(self, address):
        """Look up an ip address from the ip2asn data, and return its row."""
        # get a numeric representation
        ip = self.ip2int(address)

        point = bisect(self._left_keys, ip)
        if point != len(self._left_keys):
            row = self._data[point-1]
            if ip >= row[self._start_col] and ip <= row[self._end_col]:
                return row
            
    def lookup_address(self, address):
        """Look up an ip address (dotted string) and return a 
        dictionary of information about it.
        (transforming the row returned by lookup_address_row)"""
        results = self.lookup_address_row(address)
        ip = self.ip2int(address)
        return {
            'ip_text': address,
            'ip_numeric': ip,
            'ip_range': [results[self._start_col], results[self._end_col]],
            'ASN': results[self._asn_col],
            'country': results[self._country_col],
            'owner': results[self._name_col],
        }

def testmain():
    import os
    t = IP2ASN(os.environ['HOME'] + "/lib/ip2asn-v4-u32.tsv")
    print(t.lookup_address("8.8.8.8"))

if __name__ == "__main__":
    testmain()

