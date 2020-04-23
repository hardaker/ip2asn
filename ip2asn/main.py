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

    parser.add_argument("-o", "--output-file", default=sys.stdout,
                        type=argparse.FileType("w"),
                        help="Output the results to this file")

    parser.add_argument("-F", "--output-fsdb", action="store_true",
                        help="Output FSDB (tab-separated) formatted data")

    parser.add_argument("addresses", type=str, nargs="+",
                        help="Addresses to print information about")

    args = parser.parse_args()
    return args

def print_result(to, address, result):
    """Displays the results to the output terminal/stdout"""
    to.write("Address: {}\n".format(address))
    to.write("  Numeric ip: {}\n".format(result['ip_numeric']))
    to.write("         ASN: {}\n".format(result['ASN']))
    to.write("       Owner: {}\n".format(result['owner']))
    to.write("     Country: {}\n".format(result['country']))
    to.write("    ip_range: {}\n".format(result['ip_range']))
    to.write("\n")

def output_fsdb_row(outf, address, result):
    outf.append([address, 
                 result['ip_numeric'],
                 result['ASN'],
                 result['owner'],
                 result['country'],
                 result['ip_range']])
                
def main():
    "The meat of the ip2asn script"
    args = parse_args()

    if args.output_fsdb:
        import pyfsdb
        outf = pyfsdb.Fsdb(out_file_handle = args.output_file)
        outf.out_column_names = ['address', 'ip_numeric', 'ASN',
                                 'owner', 'country', 'ip_range']

    i2a = ip2asn.IP2ASN(args.ip2asn_database, ipversion=None)
    for address in args.addresses:
        result = i2a.lookup_address(address)
        if not result:
            print("ERROR: address '%s' was not found in the database".format(address))
            continue

        if args.output_fsdb:
            output_fsdb_row(outf, address, result)
        else:
            print_result(args.output_file, address, result)

if __name__ == "__main__":
    main()
