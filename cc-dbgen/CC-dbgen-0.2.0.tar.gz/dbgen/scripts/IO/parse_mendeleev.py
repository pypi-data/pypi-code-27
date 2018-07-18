from typing     import List,Tuple
from json       import loads
from os         import environ
from subprocess import check_output

def parse_mendeleev()->Tuple[List[int],List[int],List[str]
                                ,List[float],List[int],List[str]]:
    """
    Extracts information of elements
    """
    # Get data from public JSON file
    #-------------------------------
    json = '/scratch/users/ksb/share/reference/element.json'
    user = environ['SHERLOCK2_USERNAME']
    sher = '%s@login.sherlock.stanford.edu'%user
    data = check_output('ssh %s cat %s'%(sher,json),shell=True)
    elems = loads(data)
    ############################
    # Constants
    #----------
    cols = ['atomic_number','atomic_weight','spacegroup','pointgroup'] # etc

    allcols = ['atomic_number', 'symbol', 'name', 'atomic_weight','atomic_radius'
              , 'phase','evaporation_heat', 'pointgroup','spacegroup'
              , 'melting_point', 'metallic_radius', 'vdw_radius'
              , 'density', 'en_allen' , 'is_radioactive'
              , 'lattice_structure' , 'fusion_heat'
              , 'econf', 'period', 'covalent_radius_bragg'
              , 'geochemical_class', 'abundance_crust', 'heat_of_formation'
              , 'electron_affinity', 'atomic_volume',  'boiling_point'
              , 'proton_affinity', 'covalent_radius_slater'
              , 'lattice_constant', 'dipole_polarizability'
              , 'en_ghosh', 'thermal_conductivity', 'group_id', 'en_pauling'
              , 'gas_basicity'
              ,'abundance_sea']

    # Initialize Variables
    #----------------------
    output = []
    for e in elems:
        output.append([e.get(k) for k in allcols])

    return tuple(map(list,zip(*output))) # type: ignore
