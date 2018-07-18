from typing     import List,Tuple
from os         import listdir
from glob       import glob
################################################################################
def get_catalog_sherlock(rootpath : str
                        ,existing : str
                    ) -> Tuple[List[str],List[str],List[str]
                              ,List[str],List[str],List[str]
                              ,List[str],List[str],List[str]]:
    """
    Searches for DFT calculation folders. Returns unzipped (stordir,logfile,code) triples

    to get anytraj: \$(cat \$(ls \$f/*.traj | head -1))
    """
    ######################
    # Initialize Variables
    #---------------------
    filt  = set(existing.split(","))
    files = set(listdir(rootpath))
    dirs,logfiles,codes,logs,pws,pots,pos,kpts,params =[],[],[],[],[],[],[],[],[]

    # Main Program
    #-------------
    for d in files - filt:
        dir = rootpath +'/'+d
        ds = listdir(dir)

        assert 'runtime.json' in ds,'Failed sanity check'

        pwinps = glob(dir+'*/pw.inp')

        # DFTcode-specific stuff
        #------------------------
        if len(pwinps) == 1:
            code    = 'quantumespresso'
            logfile = dir+'/log'
            with open(pwinps[0],'r') as f:
                pwinp = f.read()

            poscar,potcar,kptcar = '','',''

        elif 'OUTCAR' in ds:
            code = 'vasp'
            logfile = dir+'/OUTCAR'
            pwinp = ''
            with open(dir+'/POSCAR','r') as f:
                poscar = f.read()
            with open(dir+'/POTCAR','r') as f:
                potcar = f.read()
            with open(dir+'/KPOINTS','r') as f:
                kptcar = f.read()

        else:
            code    = 'gpaw'
            logfile = dir+'/log'
            pwinp,poscar,potcar,kptcar = '','','',''

        # Common attributes
        #------------------
        with open(logfile,'r') as f:
            log = f.read()

        with open(dir+'/params.json','r') as f:
            paramjson = f.read()


        # Store results
        #------------
        dirs.append(dir)
        logfiles.append(logfile)
        codes.append(code)
        logs.append(log)
        pws.append(pwinp)
        pots.append(potcar)
        pos.append(poscar)
        kpts.append(kptcar)
        params.append(paramjson)

    return dirs,logfiles,codes,logs,pws,pots,pos,kpts,params

if __name__ == '__main__':
    import sys
    print(get_catalog_sherlock(sys.argv[1],''))
