# External Modules
from typing import Tuple,List,TYPE_CHECKING
if TYPE_CHECKING:
    from ase import Atoms       # type: ignore
    from pymatgen import Site   # type: ignore

from pymatgen.analysis.structure_analyzer import VoronoiConnectivity  # type: ignore
from pymatgen.io.ase                      import AseAtomsAdaptor  # type: ignore
from math import floor
from json import dumps
from numpy import where,vectorize  # type: ignore

# Internal Modules
from dbgen.core.lists import flatten

##############################################################################

def solid_angle(atoms : 'Atoms'
               ,tol   : float   = 1 # MIN SOLID ANGLE
               ) -> str:
    """
    Take an Atoms object and return bonddata USING solid angles
    """

    positions = atoms.get_positions()
    floors    = vectorize(floor)

    pmg  = AseAtomsAdaptor().get_structure(atoms)
    vc   = VoronoiConnectivity(pmg)
    arr  = vc.connectivity_array
    output = []
    for i in range(len(atoms)):
        for j in range(i,len(atoms)):
            print('i = %d,j = %d'%(i,j))
            imgs = where( arr[i][j] > tol )
            angles = arr[i][j][imgs]
            offs   = vc.offsets[imgs]
            for a,(x,y,z) in zip(angles,offs):
                print((i,j,a,x,y,z))
                output.append((i,j,a,x,y,z))
    return dumps(output)
