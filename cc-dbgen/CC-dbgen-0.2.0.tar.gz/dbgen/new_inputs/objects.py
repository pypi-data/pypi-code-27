# External Modules
from typing import Any
# Internal Modules
from dbgen.support.datatypes.object     import new_model,NOTNULL,FK,UNIQUE,DEFAULT
from dbgen.support.datatypes.sqltypes   import SQLType,Int,Varchar,Text,Decimal
#############################################################################
kris = new_model('kris') # type: Any

class Job(kris):
    """
    DFT jobs
    """
    logfile             = Varchar(),NOTNULL,UNIQUE
    stordir             = Varchar(),NOTNULL
    code                = Varchar(),NOTNULL
    user                = Varchar()
    timestamp           = Int()
    working_directory   = Varchar()
    log                 = Text('long')
    pwinp               = Text()
    potcar              = Text('long')
    poscar              = Text()
    kptcar              = Text()
    paramdict           = Text('long')
    anytraj             = Text('long')
    job_type            = Varchar()
    job_name            = Varchar()
    ads_catalog         = Varchar()
    structure_catalog   = Varchar()

class Calc(kris):
    """
    DFT calc parameters
    """
    dftcode = Varchar(),NOTNULL,UNIQUE
    xc      = Varchar(),NOTNULL,UNIQUE
    pw      = Int(),    NOTNULL,UNIQUE
    psp     = Varchar(),NOTNULL,UNIQUE


class Cell(kris):
    """
    Periodic cells defined by three vectors
    """
    a0              = Decimal(),NOTNULL,UNIQUE
    a1              = Decimal(),NOTNULL,UNIQUE
    a2              = Decimal(),NOTNULL,UNIQUE
    b0              = Decimal(),NOTNULL,UNIQUE
    b1              = Decimal(),NOTNULL,UNIQUE
    b2              = Decimal(),NOTNULL,UNIQUE
    c0              = Decimal(),NOTNULL,UNIQUE
    c1              = Decimal(),NOTNULL,UNIQUE
    c2              = Decimal(),NOTNULL,UNIQUE
    surface_area    = Decimal()
    volume          = Decimal()
    a               = Decimal()
    b               = Decimal()
    c               = Decimal()

class Struct(kris):
    """
    Chemical structure defined in periodic cell
    """
    _components      = [Cell]
    raw              = Text(),   NOTNULL
    rawhash          = Varchar(),NOTNULL
    system_type      = Varchar()
    n_atoms          = Int()
    n_elems          = Int()
    composition      = Varchar()
    composition_norm = Varchar()
    metal_comp       = Varchar()
    str_symbols      = Varchar()
    str_constraints  = Varchar()
    symmetry         = Varchar()
    geo_graph        = Text('long')
    elemental        = Int()

class Element(kris):
    """
    Chemical element
    """
    symbol                  = Varchar(),NOTNULL
    atomic_weight           = Decimal(),NOTNULL
    name                    = Varchar(),NOTNULL
    atomic_radius           = Int()
    phase                   = Varchar()
    group_id                = Int()
    period                  = Int()
    pointgroup              = Varchar()
    spacegroup              = Int()
    evaporation_heat        = Decimal()
    melting_point           = Decimal()
    metallic_radius         = Decimal()
    vdw_radius              = Decimal()
    density                 = Decimal()
    en_allen                = Decimal()
    is_radioactive          = Int()
    lattice_struct          = Varchar()
    fusion_heat             = Decimal()
    econf                   = Varchar()
    covalent_radius_bragg   = Decimal()
    geochemical_class       = Varchar()
    abundance_crust         = Decimal()
    heat_of_formation       = Decimal()
    electron_affinity       = Decimal()
    atomic_volume           = Decimal()
    boiling_point           = Decimal()
    proton_affinity         = Decimal()
    covalent_radius_slater  = Decimal()
    lattice_constant        = Decimal()
    dipole_polarizability   = Decimal()
    en_ghosh                = Decimal()
    thermal_conductivity    = Decimal()
    en_pauling              = Decimal()
    gas_basicity            = Decimal()
    abundance_sea           = Decimal()

class Atom(kris):
    """
    An atom in a specific chemical structure
    """
    _parents     = [Struct]
    _components  = [Element]
    _many_to_one = True

    x            =  Decimal(),NOTNULL
    y            =  Decimal(),NOTNULL
    z            =  Decimal(),NOTNULL
    constrained  = Int(),NOTNULL
    magmom       = Decimal()

class Calc_other(kris):
    """
    Less important DFT Calculator Parameters
    """
    kx          = Int(),NOTNULL
    ky          = Int(),NOTNULL
    kz          = Int(),NOTNULL
    fmax        = Decimal()
    econv       = Decimal(10,7)
    dw          = Int()
    sigma       = Decimal(10,7)
    nbands      = Int()
    mixing      = Decimal()
    nmix        = Int()
    xtol        = Decimal(10,7)
    strain      = Decimal()
    gga         = Varchar()
    luse_vdw    = Int()
    zab_vdw     = Decimal()
    nelmdl      = Int()
    gamma       = Int()
    dipol       = Varchar()
    algo        = Varchar()
    ibrion      = Int()
    prec        = Varchar()
    ionic_steps = Int()
    lreal       = Varchar()
    lvhar       = Int()
    diag        = Varchar()
    spinpol     = Int()
    dipole      = Int()
    maxstep     = Int()
    delta       = Decimal()
    mixingtype  = Varchar()
    bonded_inds = Varchar()
    step_size   = Decimal()
    spring      = Decimal()
    cell_dofree = Varchar()
    cell_factor = Decimal()
    kpts        = Varchar()
    energy_cut_off = Decimal()

class Relax_job(kris):
    """
    Jobs that compute local minima for electronic energy
    """
    _parents    = [Job]
    _components = [Calc,Calc_other]

    reference   = Int()
    is_tom      = Int()

class Roots(kris):
    """
    Directories which are recursively searched for computation logfiles
    """
    root    = Varchar(),NOTNULL,UNIQUE
    code    = Varchar(),NOTNULL,UNIQUE
    label   = Varchar(),NOTNULL,UNIQUE
    active  = Int(),    NOTNULL,UNIQUE,DEFAULT(1)

class Pure_struct(kris):
    """
    Structure abstraction developed by Ankit Jain
    """
    name        = Varchar(),NOTNULL,UNIQUE
    spacegroup  = Int()
    free        = Int()
    nickname    = Varchar()

class Traj(kris):
    """
    A step in a relaxation
    """
    _parents     = [Relax_job]
    _components  = [Struct]
    _many_to_one = True

    final    = Int(),NOTNULL
    energy   = Decimal()
    fmax     = Decimal()
    kptden_x = Decimal()
    kptden_y = Decimal()
    kptden_z = Decimal()

class Adsorbate(kris):
    """
    Species that can adsorb onto a surface
    """
    name        = Varchar(),NOTNULL,UNIQUE
    composition = Varchar()

class Adsorbate_composition(kris):
    """
    Components of an adsorbate
    """
    _parents     = [Adsorbate,Element]

    number = Int(),NOTNULL

class Struct_adsorbate(kris):
    """
    An adsorbate considered on a particular surface
    """
    _parents     = [Adsorbate,Struct]
    _many_to_one = True

    site = Varchar()

#############################################################################
# INSTANCES
#----------
a1 = Atom('1')
a2 = Atom('2')
rj = Relax_job()
vw = kris._mkView([a1.x]) # type: ignore
