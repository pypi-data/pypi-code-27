#!/usr/bin/env python3
import sys
import os
import re
import argparse
from Bio import AlignIO


description = '''
To extract some sites (or codon) from a multiple sequence alignment. By Guanliang MENG, go to https://github.com/linzhi2013/extract_specific_sites_from_msa for more details.

'''

parser = argparse.ArgumentParser(description=description)

parser.add_argument('-infile', metavar='<file>', help='input multiple sequence alignment file')

parser.add_argument('-format', default='phylip-relaxed', 
    required=False, choices=['fasta', 'emboss', 'stockholm', 'phylip', 'phylip-relaxed', 'clustal'], help='input file format [%(default)s]')

parser.add_argument('-outformat', default='fasta', 
    required=False, choices=['fasta', 'emboss', 'stockholm', 'phylip', 'phylip-relaxed', 'clustal'], help='output file format [%(default)s]')

parser.add_argument('-outfile', metavar='<file>', help='outfile')

parser.add_argument('-config', metavar='<file>', required=False, help='a file containing the sites to be extracted (1 left-based). do not support 2-5, you should write 2 3 4 5 instead, the site numbers in config can be on one line or multiple lines.')

parser.add_argument('-codon', metavar='<int>', default=2, type=int, choices=[1, 2, 3], required=False, help='codon site to be extracted [%(default)s]')


def get_parameter():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    return args


def get_sites_by_codon(align_len=None, codon=2):
    sites = []
    for i in range(codon-1, align_len, 3):
        sites.append(i)

    return sites


def get_sits_from_file(configfile=None):
    sites = []
    with open(configfile, 'r') as fh:
        for i in fh:
            i = i.strip()
            if not i:
                continue
            line = i.split()
            for j in line:
                j = int(j) - 1
                sites.append(j)

    return sites


def main():
    args = get_parameter()

    alignment = AlignIO.read(args.infile, args.format)
    align_len=alignment.get_alignment_length()

    print("Number of rows: %i" % len(alignment))
    print('alignment length: ', align_len)

    if args.codon and not args.config:
        print('choose {0} th site of each codon'.format(args.codon))
        sites = get_sites_by_codon(align_len=align_len, codon=args.codon)

    elif args.config:
        print('choose sites from {0} file'.format(args.config))
        sites = get_sits_from_file(configfile=args.config)


    result_aln = alignment[:, 0:1]
    for site in sites[1:]:
        result_aln += alignment[:, site:site+1]

    print('output alignment length:', result_aln.get_alignment_length())
    AlignIO.write(result_aln, args.outfile, args.outformat)


if __name__ == '__main__':
    main()





















