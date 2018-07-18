from typing     import Tuple,List
from os         import environ
from subprocess import check_output

def populate_storage()->Tuple[List[str],List[str],List[str]]:
    """
    Reads DFT_LOGFILES to find a structured textfile with information
    about what directories should be considered 'roots'
    """
    if environ['USER'] == 'ksb':
       print('warning, using smallroots')
       path = '/scratch/users/ksb/share/reference/smallroots.txt'
    else:
        path = '/scratch/users/ksb/share/reference/roots.txt'
    user = environ['SHERLOCK2_USERNAME']
    sher = '%s@login.sherlock.stanford.edu'%user
    data = check_output('ssh %s cat %s'%(sher,path),shell=True).decode('utf-8')
    rootdata  = [l.split()
                    for l in data.split('\n')
                    if '#' not in l and l.strip()!='']
    paths,codes,labels = zip(*rootdata)
    return list(paths),list(codes),list(labels)
