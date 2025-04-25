#!/usr/bin/python3

"""Reads an ip2asn file into memory, and uses the data to extract
information about an address.

Usage:
    Prep:

    curl -o ip2asn-combined.tsv.gz https://iptoasn.com/data/ip2asn-combined.tsv.gz
    gunzip ip2asn-combined.tsv.gz
    pip3 install ip2asn

    Code:

    import ip2asn
    i2a = ip2asn.IP2ASN("ip2asn-combined.tsv")
    result = i2a.lookup_address("93.184.216.34")
    result = i2a.lookup_address("2606:2800:220:1:248:1893:25c8:1946")
    print(result)
"""

import os
import pyfsdb
import ipaddress
import msgpack
import io
from copy import deepcopy

__VERSION__ = "1.6.3"

from typing import List
from logging import error, warning
from bisect import bisect


class IP2ASN:
    """A container for accessing data within an ip2asn file"""

    def __init__(self, ip2asn_file, ipversion=None, cache_contents: bool = False):
        self._file = ip2asn_file
        self._version = ipversion

        self._msgpack_extension = ".msgpack"

        # TODO(hardaker): this probably shouldn't be forced called in init()
        self.read_data(cache_contents)

    @property
    def file_name(self):
        if isinstance(self._file, str):
            return self._file
        elif isinstance(self._file, io.StringIO):
            return "BOGUSFILE"
        else:
            return self._file.name

    def read_data(self, cache_contents: bool = False):
        self.read_data_internal()
        if cache_contents:
            self.save_msgpack_file()

    def save_large_numbers32(self, dataset: List[int]) -> List[int | List[int]]:
        transformmed = []
        for item in dataset:
            if item >= 2**32:
                transformmed.append(
                    [
                        (item & 0xFFFFFFFF000000000000000000000000) >> 12 * 8,
                        (item & 0xFFFFFFFF0000000000000000) >> 8 * 8,
                        (item & 0xFFFFFFFF00000000) >> 4 * 8,
                        (item & 0xFFFFFFFF),
                    ]
                )
            else:
                transformmed.append(item)
        return transformmed

    def load_large_numbers32(self, dataset: List[int | List[int]]) -> List[int]:
        transformmed = []
        for item in dataset:
            if isinstance(item, list):
                item = (
                    (item[0] << 12 * 8)
                    + (item[1] << 8 * 8)
                    + (item[2] << 4 * 8)
                    + (item[3])
                )
            transformmed.append(item)
        return transformmed

    def save_large_numbers64(self, dataset: List[int]) -> List[int | List[int]]:
        """Convert a list of up to 128 bit integers and return an encoded list of 64 bit integers."""
        transformmed = []
        for item in dataset:
            if item >= 2**64:
                transformmed.append(
                    [
                        (item & 0xFFFFFFFFFFFFFFFF0000000000000000) >> 8 * 8,
                        (item & 0xFFFFFFFFFFFFFFFF),
                    ]
                )
            else:
                transformmed.append(item)
        return transformmed

    def load_large_numbers64(self, dataset: List[int | List[int]]) -> List[int]:
        """Convert a list of encoded 64 bit integers into an original list of up to 128 bit integers."""
        transformmed = []
        for item in dataset:
            if isinstance(item, list):
                item = (item[0] << 8 * 8) + (item[1])
            transformmed.append(item)
        return transformmed

    def save_data_numbers64(self, dataset: List[int]) -> List[int | List[int]]:
        transformmed = deepcopy(dataset)
        for item in transformmed:
            if item[0] >= 2**64:
                item[0] = [
                    (item[0] & 0xFFFFFFFFFFFFFFFF0000000000000000) >> 8 * 8,
                    (item[0] & 0xFFFFFFFFFFFFFFFF),
                ]
            if item[1] >= 2**64:
                item[1] = [
                    (item[1] & 0xFFFFFFFFFFFFFFFF0000000000000000) >> 8 * 8,
                    (item[1] & 0xFFFFFFFFFFFFFFFF),
                ]
        return transformmed

    def load_data_numbers64(self, dataset: List[int | List[int]]) -> List[int]:
        """Convert a list of encoded 64 bit integers into an original list of up to 128 bit integers."""
        transformmed = []
        for item in dataset:
            if isinstance(item[0], list):
                item[0] = (item[0][0] << 8 * 8) + (item[0][1])
            if isinstance(item[1], list):
                item[1] = (item[1][0] << 8 * 8) + (item[1][1])
            transformmed.append(item)
        return transformmed

    def read_msgpack_file(self) -> bool:
        """Read a msgpack compressed version of the database if available."""
        msgpack_filename = self.file_name + self._msgpack_extension
        if not os.path.exists(msgpack_filename):
            return False

        contents = msgpack.load(open(msgpack_filename, "rb"))

        if contents["version"] != __VERSION__:
            warning(
                f"This ip2asn cache file was created with an older version ({contents['version']}) -- things may break."
            )

        self._data = self.load_data_numbers64(contents["data"])
        self._left_keys = self.load_large_numbers64(contents["left_keys"])
        self._start_col = contents["start_col"]
        self._end_col = contents["end_col"]
        self._asn_col = contents["asn_col"]
        self._country_col = contents["country_col"]
        self._name_col = contents["name_col"]

        return True

    def save_msgpack_file(self) -> None:
        """Save the stored data into a msgpack file."""

        msgpack_filename = self.file_name + self._msgpack_extension

        contents = {
            "version": __VERSION__,
            "data": self.save_data_numbers64(self._data),
            "left_keys": self.save_large_numbers64(self._left_keys),
            "start_col": self._start_col,
            "end_col": self._end_col,
            "asn_col": self._asn_col,
            "country_col": self._country_col,
            "name_col": self._name_col,
        }
        msgpack.pack(contents, open(msgpack_filename, "wb"))

    def read_data_internal(self) -> None:
        """Read data from the ip2asn file."""

        if self.read_msgpack_file():
            return

        if isinstance(self._file, str):
            # assume a file name
            iptoasn = pyfsdb.Fsdb(self._file)
        else:
            # assume it's a file handle instead
            iptoasn = pyfsdb.Fsdb(file_handle=self._file)

        # set the column names for pyfsdb
        iptoasn.column_names = ["start", "end", "ASN", "country", "name"]

        (
            self._start_col,
            self._end_col,
            self._asn_col,
            self._country_col,
            self._name_col,
        ) = iptoasn.get_column_numbers(iptoasn.column_names)

        # XXX: fsdb should do this for us
        self._data = []
        self._left_keys = []
        for row in iptoasn:
            try:
                row[self._start_col] = int(row[self._start_col])
                row[self._end_col] = int(row[self._end_col])
            except Exception:
                # must be addresses not ints
                try:
                    row[self._start_col] = self.ip2int(row[self._start_col])
                    row[self._end_col] = self.ip2int(row[self._end_col])
                except Exception:
                    error(f"failed to parse {row}")
                    continue

            self._data.append(row)
            self._left_keys.append(int(row[self._start_col]))

    def ip2int(self, address, version=None):
        """Converts an ascii represented IPv4 or IPv6 address into an
        integer.  If the ipversion isn't specified (4 or 6), it
        will attempt to guess based on whether the address has
        a ':' character in it"""
        if version is None:
            if self._version:
                verison = self._version
            elif ":" in address:
                version = 6
            elif "." in address:
                version = 4
            else:
                raise ValueError(f"unknown address type: {address}")
        if version == 4:
            ip = int(ipaddress.IPv4Address(address))
        elif version == 6:
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
            row = self._data[point - 1]
            if ip >= row[self._start_col] and ip <= row[self._end_col]:
                return row

    def lookup_address(self, address):
        """Look up an ip address (dotted string) and return a
        dictionary of information about it.
        (transforming the row returned by lookup_address_row)"""
        results = self.lookup_address_row(address)
        if not results:
            return results
        ip = self.ip2int(address)
        return {
            "ip_text": address,
            "ip_numeric": ip,
            "ip_range": [results[self._start_col], results[self._end_col]],
            "ASN": results[self._asn_col],
            "country": results[self._country_col],
            "owner": results[self._name_col],
        }

    def lookup_asn(self, asn, limit=None):
        """Lookups all the entries in the database containing a
        particular ASN"""

        asn = str(asn)  # turn an into back to a string

        results = []
        for record in self._data:
            if record[self._asn_col] == asn:
                results.append(
                    {
                        "ip_range": [record[self._start_col], record[self._end_col]],
                        "ASN": record[self._asn_col],
                        "country": record[self._country_col],
                        "owner": record[self._name_col],
                    }
                )
                if limit and len(results) == limit:
                    return results

        return results


def testmain():
    import os

    t = IP2ASN(os.environ["HOME"] + "/lib/ip2asn-v4-u32.tsv")
    print(t.lookup_address("8.8.8.8"))


if __name__ == "__main__":
    testmain()
