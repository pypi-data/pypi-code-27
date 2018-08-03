#!/usr/bin/env python3
import sys
import re
import os
from Bio import SeqIO
from Bio.Seq import Seq
#from Bio.Alphabet import IUPAC
import argparse


description = 'Filter the sequences by translating the protein coding genes (PCGs) with proper genetic code table, if one of the PCGs has interal stop codon, filter out this sequence. Beware: if the seq has Ns, then this script will translate the sub seqs with three frames (0, 1, 2), only when all these three kinds of frames have interal stopCodon the seq will be treated as have InternalStop!. By Guanliang MENG, see https://github.com/linzhi2013/breakSeqInNs_then_translate'

parser = argparse.ArgumentParser(description=description)

parser.add_argument('-seq', metavar='<seq>', required=False,
    help='input sequence')

parser.add_argument('-seqfile', metavar='<file>', required=False, 
    help='input fasta or genbank file')

parser.add_argument('-seqformat', default='fa', choices=['fa', 'gb'], 
    required=False, help='input -seqfile format [%(default)s]')

parser.add_argument('-code', metavar='<int>', default=1, type=int, 
    required=False, help='genetic code table [%(default)s]')

parser.add_argument('-nb', dest='breakNs', default=True, action='store_false', 
    required=False, help='do not break sequence in Ns when translate [break]')

parser.add_argument('-gb_genes', metavar='<int>', default=5, type=int, 
    required=False, help='if a genbank record has no less than -gb_genes PCGs and no more than -maxStopGenes PCGs has InternalStops, we keep this record. But if a genbank record has less than -gb_genes PCGs, then we will discard this record if any of its PCGs has InternalStops. This is because we may want to tolerate some assembly/sequencing errors. This has no effect on fasta input file. [%(default)s]')

parser.add_argument('-maxStopGenes', metavar='<int>', default=0, type=int, 
    required=False, help='the maximum number of PCGs can have InternalStops in a genbank record if do not discard it [%(default)s]')


def get_para():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    input_count = 0
    if args.seq:
        input_count += 1
        args.seq = args.seq.upper()

    if args.seqfile:
        input_count += 1

    if not input_count:
        sys.exit('you must input -seq or -seqfile')

    if input_count > 1:
        sys.exit('you can only input -seq or -seqfile at one time!')

    return args


def get_triple_seq(seq=None):
    '''
    if remains > 0, the end of return seq is not the end of the whole-seq.
    Thus, if such a return seq has stop codon in 3'-end of protein, 
    the whole-seq actually has internal stop codons!

    '''
    seqlen = len(seq)
    remains = seqlen % 3
    end = seqlen - remains
    return seq[0:end], remains


def pro_has_internal_stop(protein=None, remove_3end_stopcodon=True):
    protein = str(protein)
    if remove_3end_stopcodon:
        protein = re.sub(r'\*$', '', protein)
    if '*' in protein:
        return True
    return False


def translate_broken_seqs(raw_seqs=None, start_without_Ns=None, table=None):
    '''
    how the raw_seqs come from:
    (1) ATGC
    (2) ATGCNAGTT
    (3) NATGC
    '''
    seqs = []
    for seq in raw_seqs[:]:
        if len(seq) >= 3:
            seqs.append(seq)

    count = 0
    have_internal_stops = False
    for seq in seqs:
        count += 1
        if start_without_Ns and count == 1: # To do here, how to avoid Ns!
            seq_to_translate, remains = get_triple_seq(seq)
            seq_obj = Seq(seq_to_translate)
            protein = seq_obj.translate(table=table)
            if remains > 0:
                if pro_has_internal_stop(protein, remove_3end_stopcodon=False):
                    have_internal_stops = True
                    return have_internal_stops
            elif remains == 0:
                # even the first one subseq is times of triple,
                # but there are subseqs after the 'Ns', in such a case,
                # if the first one subseq has 3'end stopcodon, the stopcodon
                # still belongs to "internal stopcodon"
                if len(seqs) > 1:
                    if pro_has_internal_stop(protein, remove_3end_stopcodon=False):
                        have_internal_stops = True
                        return have_internal_stops
                else:
                    if pro_has_internal_stop(protein):
                        have_internal_stops = True
                        return have_internal_stops
            
            continue

        stopCodon = 0
        for i in range(0, 3):
            seq_to_translate, remains = get_triple_seq(seq[i:])
            if len(seq_to_translate) < 3:
                continue

            seq_obj = Seq(seq_to_translate)
            protein = seq_obj.translate(table=table)
            
            if remains > 0:
                if pro_has_internal_stop(protein, remove_3end_stopcodon=False):
                    stopCodon += 1
            else:
                if pro_has_internal_stop(protein):
                    stopCodon += 1

        if stopCodon == 3:
            have_internal_stops = True
            return have_internal_stops

    return have_internal_stops


def deal_seq(args=None):
    # only break seq in Ns when the seq has Ns and the user ask for it!
    if 'N' in args.seq and args.breakNs:
        seqs = re.split(r'N+', args.seq)
        
        start_without_Ns = False
        if not args.seq.startswith('N'):
            start_without_Ns = True

        have_internal_stops = translate_broken_seqs(raw_seqs=seqs, 
            start_without_Ns=start_without_Ns, table=args.code)
        if have_internal_stops:
            print('sequence has interal sotp codons!', file=sys.stdout)

    else:
        seq_to_translate, remains = get_triple_seq(args.seq)
        seq_obj = Seq(seq_to_translate)
        protein = seq_obj.translate(table=args.code)
        print(protein, file=sys.stdout)


def deal_fasta_file(args=None):
    InternalStop_file = os.path.basename(args.seqfile) + '.InternalStop'
    NoInternalStop_file = os.path.basename(args.seqfile) + '.NoInternalStop'
    fh_InternalStop = open(InternalStop_file, 'w')
    fh_NoInternalStop = open(NoInternalStop_file, 'w')

    for rec in SeqIO.parse(args.seqfile, 'fasta'):
        clean_seqrec = str(rec.seq.upper())
        have_internal_stops = False
        if args.breakNs:
            seqs = re.split(r'N+', clean_seqrec)

            start_without_Ns = False
            if not clean_seqrec.startswith('N'):
                start_without_Ns = True

            have_internal_stops = translate_broken_seqs(raw_seqs=seqs, 
                start_without_Ns=start_without_Ns, table=args.code)
        else:
            seq_to_translate, remains = get_triple_seq(clean_seqrec)
            seq_obj = Seq(seq_to_translate)
            protein = seq_obj.translate(table=args.code)

            if remains > 0:
                have_internal_stops = pro_has_internal_stop(protein, remove_3end_stopcodon=False)
            else:
                have_internal_stops = pro_has_internal_stop(protein)


        if have_internal_stops:
            SeqIO.write(rec, fh_InternalStop, 'fasta')
        else:
            SeqIO.write(rec, fh_NoInternalStop, 'fasta')

    fh_InternalStop.close()
    fh_NoInternalStop.close()


def deal_gb_file(args=None):
    InternalStop_file = os.path.basename(args.seqfile) + '.InternalStop'
    NoInternalStop_file = os.path.basename(args.seqfile) + '.NoInternalStop'
    fh_InternalStop = open(InternalStop_file, 'w')
    fh_NoInternalStop = open(NoInternalStop_file, 'w')

    for rec in SeqIO.parse(args.seqfile, 'gb'):
        have_internal_stops = False
        tot_PCGS = 0
        PCGs_have_internal_stops = 0

        for fea in rec.features:
            if fea.type == 'CDS':
                tot_PCGS += 1
                if 'gene' in fea.qualifiers:
                    gene = fea.qualifiers['gene'][0]
                elif 'product' in fea.qualifiers:
                    product = fea.qualifiers['product'][0]
                    gene = product

                start = fea.location.start
                end = fea.location.end
                if fea.strand == -1:
                    clean_seqrec = str(rec[start:end].seq.reverse_complement().upper())
                else:
                    clean_seqrec = str(rec[start:end].seq.upper())

                if args.breakNs:
                    seqs = re.split(r'N+', clean_seqrec)

                    start_without_Ns = False
                    if not clean_seqrec.startswith('N'):
                        start_without_Ns = True

                    have_internal_stops = translate_broken_seqs(raw_seqs=seqs, 
                        start_without_Ns=start_without_Ns, table=args.code)
                else:
                    seq_to_translate, remains = get_triple_seq(clean_seqrec)
                    seq_obj = Seq(seq_to_translate)
                    protein = seq_obj.translate(table=args.code)
                    if remains > 0:
                        have_internal_stops = pro_has_internal_stop(protein, remove_3end_stopcodon=False)
                    else:
                        have_internal_stops = pro_has_internal_stop(protein)

                if have_internal_stops:
                    PCGs_have_internal_stops += 1
                    print(args.seqfile, rec.id, gene, 'has InternalStop!', file=sys.stderr)
 
        if tot_PCGS >= args.gb_genes:
            if PCGs_have_internal_stops <= args.maxStopGenes:
                SeqIO.write(rec, fh_NoInternalStop, 'gb')
            else:
                SeqIO.write(rec, fh_InternalStop, 'gb')

        elif tot_PCGS < args.gb_genes:
            if PCGs_have_internal_stops == 0:
                SeqIO.write(rec, fh_NoInternalStop, 'gb')
            else:
                SeqIO.write(rec, fh_InternalStop, 'gb')

    fh_InternalStop.close()
    fh_NoInternalStop.close()


def main():
    args = get_para()

    if args.seq:
        deal_seq(args=args)

    elif args.seqformat == 'fa':
        deal_fasta_file(args=args)

    elif args.seqformat == 'gb':
        deal_gb_file(args=args)
        

if __name__ == '__main__':
    main()

















