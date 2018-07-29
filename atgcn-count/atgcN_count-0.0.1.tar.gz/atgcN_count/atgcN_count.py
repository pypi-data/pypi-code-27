#!/usr/bin/python3
import sys
import argparse

parser = argparse.ArgumentParser(description='To stat the counts of each base in a fasta file. By Guanliang MENG.')

parser.add_argument('-i', dest='infas', metavar='<file>', 
    help='input fasta file')

parser.add_argument('-v', dest='verbose', action='store_true', default=False, 
    help='also output statistics for each sequence [%(default)s]')

parser.add_argument('-d', dest='decimals', default=2, type=int, 
    metavar='<int>', help='decimals for output result [%(default)s]')

parser.add_argument('-N', dest='ATGC_only', action='store_true', 
    default=False, 
    help='do not take non-ATGC bases into account when caculate percentage [%(default)s]')


def base_count(seq):
    seq = seq.upper()
    base_dict = {}
    for i in range(0, len(seq)):
        base = seq[i]
        if base not in base_dict:
            base_dict[base] = 1
        else:
            base_dict[base] += 1
    return base_dict


def base_stat(seqid=None, base_dict=None, decimals=2, ATGC_only=False):
    total_bases = 0
    AT_count = 0
    GC_count = 0
    for base in base_dict.keys():
        if ATGC_only and base not in ['A', 'T', 'G', 'C']:
            continue
        if base in ["A", "T"]:
            AT_count += base_dict[base]
        elif base in ["G", "C"]:
            GC_count += base_dict[base]

        total_bases += base_dict[base]
               
    print(seqid)
    for base in base_dict.keys():
        if ATGC_only and base not in ['A', 'T', 'G', 'C']:
            print(base, format(base_dict[base], ","), sep="\t")
            continue
        print(base, format(base_dict[base], ","), round(100.0*base_dict[base]/total_bases, decimals), sep="\t")

    AT_rate = round(100.0*AT_count/total_bases, decimals)
    GC_rate = round(100.0*GC_count/total_bases, decimals)
    non_ATGC_rate = round(100-AT_rate-GC_rate, decimals)
    print("A+T:", AT_rate)
    print("G+C:", GC_rate)
    if not ATGC_only:
        print("non-ATGC:", non_ATGC_rate)
    print("total bases:", format(total_bases, ","))

def final_base_stat(base_dict=None, decimals=2, ATGC_only=False):
    total_bases = 0
    AT_count = 0
    GC_count = 0
    for base in base_dict.keys():
        if ATGC_only and base not in ['A', 'T', 'G', 'C']:
            continue
        if base in ["A", "T"]:
            AT_count += base_dict[base]
        elif base in ["G", "C"]:
            GC_count += base_dict[base]

        total_bases += base_dict[base]
    
    print('\nstatistics of all sequences:')
    for base in base_dict.keys():
        if ATGC_only and base not in ['A', 'T', 'G', 'C']:
            print(base, format(base_dict[base], ","), sep="\t")
            continue
        print(base, format(base_dict[base], ","), round(100.0*base_dict[base]/total_bases, decimals), sep="\t")

    AT_rate = round(100.0*AT_count/total_bases, decimals)
    GC_rate = round(100.0*GC_count/total_bases, decimals)
    non_ATGC_rate = round(100-AT_rate-GC_rate, decimals)
    
    print("A+T:", AT_rate)
    print("G+C:", GC_rate)
    if not ATGC_only:
        print("non-ATGC:", non_ATGC_rate)
    print("total bases:", format(total_bases, ","))


def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()

    total_base_dict = {}

    fh_in = open(args.infas, 'r')
    tmp = 1
    for line in fh_in:
        line = line.rstrip()
        if line.startswith(">"):
            if tmp == 1:
                tmp = 0
            else:
                base_dict = base_count(seq)

                if args.verbose:
                    base_stat(seqid=seqid, base_dict=base_dict, 
                        decimals=args.decimals, ATGC_only=args.ATGC_only)
                # add to total_base_dict
                for base in base_dict.keys():
                    if base not in total_base_dict:
                        total_base_dict[base] = 0
                    total_base_dict[base] += base_dict[base]

                del base_dict
            seqid = line
            seq = ""
        else:
            seq += line

    fh_in.close()

    # the last record
    base_dict = base_count(seq)
    if args.verbose:
        base_stat(seqid=seqid, base_dict=base_dict, 
            decimals=args.decimals, ATGC_only=args.ATGC_only)
    # the last record. add to total_base_dict
    for base in base_dict.keys():
        if base not in total_base_dict:
            total_base_dict[base] = 0
        total_base_dict[base] += base_dict[base]

    # statistics of all sequences 
    final_base_stat(total_base_dict, decimals=args.decimals, 
        ATGC_only=args.ATGC_only)


if __name__ == '__main__':
    main()
