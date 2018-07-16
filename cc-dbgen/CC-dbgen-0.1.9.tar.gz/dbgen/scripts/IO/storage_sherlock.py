from typing     import Tuple,List
from os         import environ
from subprocess import check_output

def storage_sherlock()->Tuple[List[str],List[str],List[str]]:
    """
    Reads DFT_LOGFILES to find a structured textfile with information
    about what directories should be considered 'roots'
    """
    path = '/scratch/users/ksb/share/reference/roots.txt'
    with open(path,'r') as f:
        rootdata  = [l.split()
                        for l in f.readlines()
                        if '#' not in l and l.strip()!='']
    paths,codes,labels = zip(*rootdata)
    return list(paths),list(codes),list(labels)
