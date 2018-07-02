# Typing Modules
import typing as typ

# External Modules
import os
import ase # type: ignore
from pymatgen.analysis.defects.point_defects 		import Interstitial # type: ignore
from pymatgen.transformations.site_transformations 	import InsertSitesTransformation # type: ignore
from pymatgen.io.ase 								import AseAtomsAdaptor # type: ignore
from pymatgen.symmetry.analyzer 					import SpacegroupAnalyzer # type: ignore

# Internal Modules
from catalog.misc.atoms import mag_elems

################################################################################

covalent_radii = {symb:rad for symb,rad in zip(ase.data.chemical_symbols,ase.data.covalent_radii)}

def getInterstitials(ase_in     : ase.Atoms
                    ,inter      : str
                    ,spinpol    : bool
                    ) -> typ.Any:
    """Helpful doc string"""
    pmg_init	= AseAtomsAdaptor.get_structure(ase_in)
    pmg_init2 	= SpacegroupAnalyzer(pmg_init).get_conventional_standard_structure()

    interstitial = Interstitial(pmg_init2,None,covalent_radii) #accuracy=high breaks...
    os.system('cls' if os.name == 'nt' else 'clear')
    output = []
    for i,site in enumerate(interstitial.enumerate_defectsites()):
        coordination =  int(round(interstitial.get_defectsite_coordination_number(i)))
        mult 	= 0 # interstitial.get_defectsite_multiplicity(i) -- broken ???
        insert  = InsertSitesTransformation([inter],[site.coords],coords_are_cartesian=True)
        try:
            pmg_new = insert.apply_transformation(pmg_init2.copy())
            ase_new = AseAtomsAdaptor.get_atoms(pmg_new)
            strname = '_%s-%dfold'%(inter,coordination)

            if spinpol:
                new_magmoms = [3 if e in mag_elems else 0 for e in ase_new.get_chemical_symbols()]
                ase_new.set_initial_magnetic_moments(new_magmoms)

            output.append((ase_new,strname))
        except ValueError: pass #ValueError: New site is too close to an existing site!
    return output
