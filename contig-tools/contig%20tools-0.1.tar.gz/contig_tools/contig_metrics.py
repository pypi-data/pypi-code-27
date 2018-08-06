def Nx(contig_lengths, x = 50):
    '''return Nx of a list of contig lengths'''
    contig_lengths.sort(reverse=1)
    Nx_threshold = sum(contig_lengths) * x / 100
    
    cumulative_length = 0
    for length in contig_lengths:
        cumulative_length += length
        if cumulative_length >= Nx_threshold:
            Nx = length
            return Nx

def get_contig_metrics(contigs, min_contig_length = None, min_contig_coverage = None):
    '''return a dictionary of contig metrics given a path to a multi fasta file'''
    contig_metrics = {}
    # make a list of contig lengths
    contig_lengths = [len(contig.seq) for contig in contigs]
    contig_metrics['num_contigs'] = len(contig_lengths)
    contig_metrics['total_length'] = sum(contig_lengths) 
    contig_metrics['N50'] = Nx(contig_lengths, x = 50)
    return contig_metrics

