#!/usr/bin/python3

"""Converts a bunch of addresses to displayed details about them"""

import argparse
import sys
import os
import ip2asn
import requests
import pyfsdb
import logging
import ipaddress
from logging import info, error
from pathlib import Path

COLUMN_NAMES = ["address", "ip_numeric", "ASN", "owner", "country", "ip_range"]
ASN_COLUMN_NAMES = ["ASN", "owner", "country", "ip_range"]

default_store = Path(os.environ["HOME"]).joinpath(".local/share/ip2asn/database.tsv")


def parse_args():
    """Handles argument parsing for the ip2asn script."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Describes one or more IP addresses from an ip2asn database",
        epilog="""Example Usage: ip2asn -f ip2asn-v4-43.tsv 1.1.1.1""",
    )

    parser.add_argument(
        "--fetch", action="store_true", help="Fetch/update the cached IP2ASN dataset."
    )

    parser.add_argument(
        "-f",
        "--ip2asn-database",
        type=str,
        default=default_store,
        help="The ip2asn database file to use (download from iptoasn.com)",
    )

    parser.add_argument(
        "-a",
        "--search-by-asn",
        action="store_true",
        help="Instead of searching by IP address, search by an ASN number instead and return all records for that ASN number",
    )

    parser.add_argument(
        "-A",
        "--asn-limit",
        type=int,
        default=0,
        help="Search by ASN, but limit the results to this number -- implies -a",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        default=sys.stdout,
        type=argparse.FileType("w"),
        help="Output the results to this file",
    )

    parser.add_argument(
        "-F",
        "--output-fsdb",
        action="store_true",
        help="Output FSDB (tab-separated) formatted data",
    )

    parser.add_argument(
        "-T",
        "--output-pcap-filter",
        action="store_true",
        help="Output the results as a libpcap / tcpdump filter expression",
    )

    parser.add_argument(
        "-I",
        "--input-fsdb",
        type=argparse.FileType("r"),
        help="Read an input FSDB and add columns to it; implies -F as well",
    )

    parser.add_argument(
        "-k",
        "--key",
        default="key",
        type=str,
        help="The input key of the FSDB input file that contains the ip address to analyze",
    )

    parser.add_argument(
        "-C",
        "--cache-database",
        action="store_true",
        help="After loading the ip2asn file, cache it in a msgpack file for faster loading next time.",
    )

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "addresses", type=str, nargs="*", help="Addresses to print information about"
    )

    args = parser.parse_args()

    if args.asn_limit > 0:
        args.search_by_asn = True

    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")

    return args


def print_result(to, address, result):
    """Displays the results to the output terminal/stdout"""
    if "ip_numeric" in result:
        to.write("Address: {}\n".format(address))
        to.write("  Numeric ip: {}\n".format(result["ip_numeric"]))
    to.write("         ASN: {}\n".format(result["ASN"]))
    to.write("       Owner: {}\n".format(result["owner"]))
    to.write("     Country: {}\n".format(result["country"]))
    if ":" in address:
        range_addresses = [str(ipaddress.IPv6Address(x)) for x in result["ip_range"]]
    else:
        range_addresses = [str(ipaddress.IPv4Address(x)) for x in result["ip_range"]]
    to.write("    ip_range: {} - {}\n".format(*range_addresses))
    to.write("\n")


def output_fsdb_row(outf, address, result):
    if "ip_numeric" in result:
        outf.append(
            [
                address,
                result["ip_numeric"],
                result["ASN"],
                result["owner"],
                result["country"],
                result["ip_range"],
            ]
        )
    else:
        outf.append(
            [result["ASN"], result["owner"], result["country"], result["ip_range"]]
        )


def output_pcap_filter(results: list) -> None:
    sys.stdout.write("( ")
    expressions = []
    for result in results:
        (left, right) = result["ip_range"]
        if left <= 2**33:
            left = ipaddress.IPv4Address(left)
            right = ipaddress.IPv4Address(right)
        else:
            left = ipaddress.IPv6Address(left)
            right = ipaddress.IPv6Address(right)
        ranges = ipaddress.summarize_address_range(left, right)
        for range in ranges:
            expressions.append(f"net {range}")

    sys.stdout.write(" or ".join(expressions))
    print(" )")


def process_fsdb(i2a, inh, outh, key, by_asn=False):
    inf = pyfsdb.Fsdb(file_handle=inh)
    outf = pyfsdb.Fsdb(out_file_handle=outh)
    if by_asn:
        outf.out_column_names = inf.column_names + ASN_COLUMN_NAMES[1:]
    else:
        outf.out_column_names = inf.column_names + COLUMN_NAMES[1:]

    key_col = inf.get_column_number(key)
    for row in inf:
        if by_asn:
            results = i2a.lookup_asn(row[key_col], limit=1)
            if len(results) == 0:
                row.extend(["-", "-", "-", "-", "-"])
            else:
                row.extend(
                    [results[0]["owner"], results[0]["country"], results[0]["ip_range"]]
                )

        else:
            result = i2a.lookup_address(row[key_col])

            if result:
                row.extend(
                    [
                        result["ip_numeric"],
                        result["ASN"],
                        result["owner"],
                        result["country"],
                        result["ip_range"],
                    ]
                )
            else:
                row.extend(["-", "-", "-", "-", "-"])
        outf.append(row)


def get_ip2asn_db_path(args, exit_on_error: bool = True):
    "Find the ip2asn database if it exists."

    database: str = default_store

    if Path(args.ip2asn_database).exists():
        database = args.ip2asn_database
    elif Path("ip2asn-combined.tsv").exists():
        info("using ./ip2asn-combined.tsv")
        database = "ip2asn-combined.tsv"
    elif exit_on_error:
        error("Cannot find the ip2asn-combined.tsv or other similar database file.")
        error("Please specify a location with -f or download from ip2asn.com.")
        error("Run with --fetch to download a copy using this tool.")
        error(f"Default storage location: {database}")
        sys.exit(1)

    return database


def fetch_ip2asn_db(storage_location: str):
    request_url = "https://iptoasn.com/data/ip2asn-combined.tsv.gz"

    info(f"starting download")

    # convert to a Path
    if not isinstance(storage_location, Path):
        storage_location = Path(storage_location)

    if not storage_location.parent.is_dir():
        storage_location.parent.mkdir(parents=True)

    # fetch the contents to our storage location
    with requests.get(request_url, stream=True) as request:
        if request.status_code != 200:
            error(f"failed to fetch {request_url}")
            sys.exit(1)

        with storage_location.open("wb") as storage:
            for chunk in request.iter_content(chunk_size=4096 * 16):
                storage.write(chunk)

    info(f"saved new data to {storage_location}")


def main():
    "The meat of the ip2asn script"
    args = parse_args()

    database = get_ip2asn_db_path(args, exit_on_error=(not args.fetch))

    if args.fetch:
        fetch_ip2asn_db(database)
        sys.exit()

    i2a = ip2asn.IP2ASN(
        str(database), ipversion=None, cache_contents=args.cache_database
    )

    if args.input_fsdb:
        process_fsdb(
            i2a, args.input_fsdb, args.output_file, args.key, by_asn=args.search_by_asn
        )
        sys.exit()

    if args.output_fsdb:
        outf = pyfsdb.Fsdb(out_file_handle=args.output_file)
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
                print(
                    "ERROR: address '{}' was not found in the database".format(address)
                )
                continue

            results = [result]

        if args.output_pcap_filter:
            output_pcap_filter(results)
        else:
            for result in results:
                if args.output_fsdb:
                    output_fsdb_row(outf, address, result)
                else:
                    print_result(args.output_file, address, result)


if __name__ == "__main__":
    main()
