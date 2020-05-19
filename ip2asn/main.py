#!/usr/bin/python3

"""Converts a bunch of addresses to displayed details about them"""

import argparse
import sys
import os
import ip2asn
import pyfsdb

COLUMN_NAMES = ['address', 'ip_numeric', 'ASN', 'owner', 'country', 'ip_range']
ASN_COLUMN_NAMES = ['ASN', 'owner', 'country', 'ip_range']

def parse_args():
    """Handles argument parsing for the ip2asn script."""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Describes one or more IP addresses from an ip2asn database",
                                     epilog="""Example Usage: ip2asn -f ip2asn-v4-43.tsv 1.1.1.1""")

    parser.add_argument("-f", "--ip2asn-database", type=str,
                        default=os.environ['HOME'] + "/lib/ip2asn-combined.tsv",
                        help="The ip2asn database file to use (download from iptoasn.com)")

    parser.add_argument("-a", "--search-by-asn", action="store_true",
                        help="Instead of searching by IP address, search by an ASN number instead and return all records for that ASN number")

    parser.add_argument("-A", "--asn-limit", type=int, default=0,
                        help="Search by ASN, but limit the results to this number -- implies -a")

    parser.add_argument("-o", "--output-file", default=sys.stdout,
                        type=argparse.FileType("w"),
                        help="Output the results to this file")

    parser.add_argument("-F", "--output-fsdb", action="store_true",
                        help="Output FSDB (tab-separated) formatted data")

    parser.add_argument("-I", "--input-fsdb", type=argparse.FileType("r"),
                        help="Read an input FSDB and add columns to it; implies -F as well")
    
    parser.add_argument("-k", "--key", default="key", type=str,
                        help="The input key of the FSDB input file that contains the ip address to analyze")

    parser.add_argument("addresses", type=str, nargs="*",
                        help="Addresses to print information about")

    args = parser.parse_args()

    if args.asn_limit > 0:
        args.search_by_asn = True
        
    return args

def print_result(to, address, result):
    """Displays the results to the output terminal/stdout"""
    if 'ip_numeric' in result:
        to.write("Address: {}\n".format(address))
        to.write("  Numeric ip: {}\n".format(result['ip_numeric']))
    to.write("         ASN: {}\n".format(result['ASN']))
    to.write("       Owner: {}\n".format(result['owner']))
    to.write("     Country: {}\n".format(result['country']))
    to.write("    ip_range: {}\n".format(result['ip_range']))
    to.write("\n")

def output_fsdb_row(outf, address, result):
    if 'ip_numeric' in result:
        outf.append([address, 
                     result['ip_numeric'],
                     result['ASN'],
                     result['owner'],
                     result['country'],
                     result['ip_range']])
    else:
        outf.append([result['ASN'],
                     result['owner'],
                     result['country'],
                     result['ip_range']])

def process_fsdb(i2a, inh, outh, key, by_asn=False):
    inf = pyfsdb.Fsdb(file_handle = inh)
    outf = pyfsdb.Fsdb(out_file_handle = outh)
    if by_asn:
        outf.out_column_names = inf.column_names + ASN_COLUMN_NAMES[1:]
    else:
        outf.out_column_names = inf.column_names + COLUMN_NAMES[1:]

    key_col = inf.get_column_number(key)
    for row in inf:
        if by_asn:
            results = i2a.lookup_asn(row[key_col], limit=1)
            if len(results) == 0:
                row.extend(['-', '-', '-', '-', '-'])
            else:
                row.extend([results[0]['owner'],
                            results[0]['country'],
                            results[0]['ip_range']])

        else:
            result = i2a.lookup_address(row[key_col])
                
            if result:
                row.extend([result['ip_numeric'],
                            result['ASN'],
                            result['owner'],
                            result['country'],
                            result['ip_range']])
            else:
                row.extend(['-', '-', '-', '-', '-'])
        outf.append(row)
        
                
def main():
    "The meat of the ip2asn script"
    args = parse_args()

    i2a = ip2asn.IP2ASN(args.ip2asn_database, ipversion=None)

    if args.input_fsdb:
        import pdb ; pdb.set_trace()
        process_fsdb(i2a, args.input_fsdb, args.output_file,
                     args.key, by_asn=args.search_by_asn)
        exit()

    if args.output_fsdb:
        outf = pyfsdb.Fsdb(out_file_handle = args.output_file)
        if args.search_by_asn:
            outf.out_column_names = ASN_COLUMN_NAMES
        else:
            outf.out_column_names = COLUMN_NAMES

    for address in args.addresses:
        if args.search_by_asn:
            results = i2a.lookup_asn(address, limit=args.asn_limit)
        else:
            result = i2a.lookup_address(address)

            if not result:
                print("ERROR: address '{}' was not found in the database".format(address))
                continue

            results = [result]

        for result in results:
            if args.output_fsdb:
                output_fsdb_row(outf, address, result)
            else:
                print_result(args.output_file, address, result)

if __name__ == "__main__":
    main()
