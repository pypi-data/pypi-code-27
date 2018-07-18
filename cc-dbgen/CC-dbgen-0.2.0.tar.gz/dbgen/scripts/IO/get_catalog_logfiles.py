from typing     import List,Tuple
from os         import environ
from os.path    import join,exists
from subprocess import check_output,DEVNULL

str9 = Tuple[str,str,str,str,str,str,str,str,str]
################################################################################
def get_catalog_logfiles(rootpath : str
                    ) -> '''Tuple[List[str],List[str],List[str]
                                 ,List[str],List[str],List[str]
                                 ,List[str],List[str],List[str]]''':
    """
    Searches for DFT calculation folders. Returns unzipped (stordir,logfile,code) triples

    """
    # Auxillary Functions
    #--------------------
    def process(dir:str,log:str,pw:str,pot:str,pos:str,out:str,kpt:str,param:str)->str9:
        if out:
            code    = 'vasp'
            logfile = dir+'/OUTCAR'
            log     = out
        elif pw:
            code    ='quantumespresso'
            logfile = dir+'/log'
        else:
            code    = 'gpaw'
            logfile = dir+'/log'
        return dir,logfile,code,log,pw,pot,pos,kpt,param

    # Initialize Variables
    #---------------------
    user   = environ['SHERLOCK2_USERNAME']
    login  = '%s@login.sherlock.stanford.edu'%user
    delim1 = '***???***'
    delim2 = '~~~***~~~'
    d1     = ';echo "%s";done;'%delim1
    d2     = 'echo "%s";cat $f/'%delim2
    loop   = r'for f in %s/*;'%rootpath
    dirs,logfiles,codes,logs,pws,pots,pos,kpts,params = [['']]*9

    # Main Program
    #-------------
    cmd  = '{2} do echo $f;{1}log;{1}pw.inp;{1}POTCAR;{1}POSCAR;{1}OUTCAR;{1}KPOINTS;{1}params.json{0}'.format(d1,d2,loop,delim2)
    output =  check_output(['ssh', login,cmd],stderr=DEVNULL).decode('utf-8')
    fdata = [process(*map(str.strip,o.split(delim2))) for o in output.split(delim1)[1:-1]]

    dirs,logfiles,codes,logs,pws,pots,pos,kpts,params = zip(*fdata)

    return list(dirs),list(logfiles),list(codes),list(logs),list(pws),list(pots),list(pos),list(kpts),list(params)

if __name__ == '__main__':
    import sys
    print(get_catalog_logfiles(sys.argv[1]))
