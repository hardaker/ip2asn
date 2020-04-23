#!/usr/bin/python3

"""Converts a bunch of addresses to displayed details about them"""

import argparse
import sys
import os
import ip2asn

def parse_args():
    """Handles argument parsing for the ip2asn script."""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Describes one or more IP addresses from an ip2asn database",
                                     epilog="""Example Usage: ip2asn -f ip2asn-v4-43.tsv 1.1.1.1""")

    parser.add_argument("-f", "--ip2asn-database", type=str,
                        default=os.environ['HOME'] + "/lib/ip2asn-v4-u32.tsv",
                        help="The ip2asn database file to use (download from iptoasn.com)")

    parser.add_argument("addresses", type=str, nargs="+",
                        help="Addresses to print information about")

    args = parser.parse_args()
    return args

def print_result(address, result):
    """Displays the results to the output terminal/stdout"""
    print("Address: {}".format(address))
    print("  Numeric ip: {}".format(result['ip_numeric']))
    print("         ASN: {}".format(result['ASN']))
    print("       Owner: {}".format(result['owner']))
    print("     Country: {}".format(result['country']))
    print("    ip_range: {}".format(result['ip_range']))
    print("")

def main():
    "The meat of the ip2asn script"
    args = parse_args()

    i2a = ip2asn.IP2ASN(args.ip2asn_database, ipversion=None)
    for address in args.addresses:
        result = i2a.lookup_address(address)
        if not result:
            print("ERROR: address '%s' was not found in the database".format(address))
            continue

        print_result(address, result)

if __name__ == "__main__":
    main()
