# Copyright (c) 2018 Dominic Benjamin
#
# The author is not affiliated with the On-Line Encyclopedia of Integer
# Sequences (OEIS).
#
# For more information on OEIS, visit https://oeis.org/
#
# Main logic - parsing arguments and calling relevant functionality.

import argparse
import oeis_cli.process as process
import oeis_cli.search as search

def main():
    parser = argparse.ArgumentParser(description='Lookup an integer sequence.')
    search_terms = parser.add_argument_group()
    search_terms.add_argument('-n', '--name',
                              help='name of sequence to search for',
                              default = "")
    search_terms.add_argument('terms', type=int, nargs='*', default=[],
                               help='integer terms to search for')
    parser.add_argument('-u', '--unordered', 
                        help='ignore order of terms',
                        action='store_true')
    args = parser.parse_args()
    if args.terms == [] and args.name == "":
        parser.print_help()
    else:
        data = search.get_data(args.terms, args.name, args.unordered) 
        print(process.format_data(data))

