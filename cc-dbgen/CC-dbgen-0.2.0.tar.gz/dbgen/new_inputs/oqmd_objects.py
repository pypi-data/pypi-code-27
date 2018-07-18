from dbgen.support.datatypes.object     import Object,NOTNULL,FK,UNIQUE,DEFAULT,view
from dbgen.support.datatypes.sqltypes   import SQLType,Int,Varchar,Text,Decimal
#############################################################################
class Atoms(Object):
    """

    """
    element_id = Varchar()
    x          = Decimal()
    y          = Decimal()
    z          = Decimal()
    ox         = Decimal()
    fx         = Decimal()
    fy         = Decimal()
    fz         = Decimal()
    magmom     = Decimal()
    charge     = Decimal()
    volume     = Decimal()
    occupancy  = Decimal()

class Authors(Object):
    """

    """
    first_name = Varchar()
    last_name  = Varchar()

class Calculations(Object):
    """

    """
    configuration   = Varchar()
    label           = Varchar()
    path            = Varchar()
    settings        = Varchar()
    energy          = Decimal()
    energy_pa       = Decimal()
    magmom          = Decimal()
    magmom_pa       = Decimal()
    band_gap        = Decimal()
    attempt         = Int()
    nsteps          = Int()
    converged       = Int()
    runtime         = Int()
    natoms          = Int()
    irreducible_kpoints  = Int()


class Calculations_element_set(Object):
    """

    """


class Calculations_hubbard_set(Object):
    """

    """


class Calculations_metadata(Object):
    """

    """


class Calculations_potential_set(Object):
    """

    """


class Compositions(Object):
    """

    """


class Compositions_element_set(Object):
    """

    """


class Dos(Object):
    """

    """


class Elements(Object):
    """

    """


class Entries(Object):
    """

    """


class Entries_element_set(Object):
    """

    """


class Entries_metadata(Object):
    """

    """


class Entries_species_set(Object):
    """

    """


class Expt_formation_energies(Object):
    """

    """


class Fits(Object):
    """

    """


class Fits_dft(Object):
    """

    """


class Fits_elements(Object):
    """

    """


class Fits_experiments(Object):
    """

    """


class Formation_energies(Object):
    """

    """


class Hubbard_corrections(Object):
    """

    """


class Hubbards(Object):
    """

    """


class Journals(Object):
    """

    """


class Metadata(Object):
    """

    """


class Operations(Object):
    """

    """


class Prototypes(Object):
    """

    """


class Publications(Object):
    """

    """


class Publications_author_set(Object):
    """

    """


class Reference_energies(Object):
    """

    """


class Rotations(Object):
    """

    """


class Sites(Object):
    """

    """


class Spacegroups(Object):
    """

    """


class Spacegroups_centering_vectors(Object):
    """

    """


class Spacegroups_operations(Object):
    """

    """


class Species(Object):
    """

    """


class Structures(Object):
    """

    """


class Structures_element_set(Object):
    """

    """


class Structures_metadata(Object):
    """

    """


class Structures_species_set(Object):
    """

    """


class Translations(Object):
    """

    """


class Vasp_potentials(Object):
    """

    """


class Wyckoffsites(Object):
    """

    """
