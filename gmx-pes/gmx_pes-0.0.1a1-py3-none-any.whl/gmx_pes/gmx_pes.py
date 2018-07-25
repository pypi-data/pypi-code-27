#!/usr/bin/env python

import os
import shutil
import multiprocessing as mp
import subprocess as sp


def grompp(f, p, c, o, n=None, r=None, raw=False):
    """Run grompp with the given arguments."""
    # TODO: setup path and environment.
    # TODO: test whether files exist
    # TODO: maxwarn?
    #  Bash reference:
    grompp = 'gmx grompp --quiet'
    args = [*grompp.split(),
            '-f', f,
            '-p', p,
            '-c', c,
            '-o', o]
    if n:
        args.extend(('-n', n))
    if r:
        args.extend(('-r', r))
    if raw:
        return sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE)
    else:
        return sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE)


def mdrun(deffnm, raw=False):
    """Run mdrun with the given arguments."""
    # TODO: setup path and environment.
    # TODO: mpirun support
    # TODO: test whether files exist
    mdrun = 'gmx mdrun --quiet'
    args = [*mdrun.split(),
            '-deffnm', deffnm]
    if raw:
        return sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE)
    else:
        return sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE)


class Reference:
    """Contains root data and collects all properties to be tested."""
    # TODO: export methods.
    # TODO: make this class more useful.
    def __init__(self, basedir):
        self.basedir = os.path.abspath(basedir)
        self.properties = {}

    def update_property(self, propname, prop):
        """Add a new property to the database."""
        self.properties[propname] = prop


class Property:
    """Header data and reference properties for each fitted property.

    This class contains basic info needed to reproduce the energy curve
    given as reference in the ref_file.

    It references the directory adn filename structure that is read only
    (rodir) when running the TestRun, as follows:
    workdir/
    |-- top/
    |   |-- system.top              # TODO: attribute?
    |   |-- molecule.itp            # NOTE: must include ../../parameter.prm
    |   |-- other.itp
    |   |   .
    |   |   .
    |   +-- freeze.itp              # if position restraints applicable
    |-- gro/
    |   |-- *.gro                   # format: groname = 'bend_NN_{:0.5f}.{}'
    |   |-- bend_NN_0.12345.gro
    |   |   .
    |   |   .
    |   +-- posres.gro              # if position restraints applicable
    +-- reference.dat               # it's actually ref_file, can be anywhere

    Attributes:
        workdir (str): path of the root dir in the structure above.
        groname (str): string pattern for the .gro file names.
                  It *must* contain a {:f} and end with .{} instead of '.gro'
        reference (Reference object): # TODO
        edr_propname (str): name of the gromacs energy property to be evaluated

    """

    def __init__(self, workdir, groname, edr_propname, reference):
        self.doc = None
        self.workdir = os.path.abspath(workdir)
        self.groname = groname          # "Bend_NN_{:0.5f}.{s}"
        self.edr_propname = edr_propname
        self.mdpfile = 'mdp/em.mdp'     # TODO: option?
        self.reference = reference
        self.data = {k: [] for k in reference.properties}
        # TODO: replace [] with empty pandas dataframe

    def read_reference(self, ref_file):
        """Read ref_file and save into self.reference_data as PANDAS table."""
        # TODO
        pass

    def write_formatted(self, out_file):
        """Write a formatted file with the header data and reference data."""
        with open(out_file, 'w') as f:
            print("[ Reference_property ]", file=f)
            print(self.doc, file=f)
            print("[ workdir ]", file=f)
            print(self.workdir, file=f)
            print("[ groname ]", file=f)
            print(self.groname, file=f)
            print("[ edr_propname ]", file=f)
            print(self.edr_propname, file=f)
            print("[ reference_data ]", file=f)
            for line in self.reference_data:
                print("{:f}\t{:f}".format(*line), file=f)


class TestRun:
    def __init__(self, reference, run_idx, workdir):
        self.run_idx = run_idx
        self.workdir = os.path.abspath(workdir)
        self.rundir = ''.join(self.workdir, '/', run_idx)
        self.properties = {k: [] for k in reference.properties}
        # TODO: replace [] with empty pandas dataframe
        self.ref = reference
        self.initialize_dir()

    def initialize_dir(self):
        """Create working directory and copy/symlink relevant files."""
        # TODO: try/except
        # TODO: avoid overiting stuff
        # TODO: safe filenames (slugs)
        os.mkdir(self.rundir)
        os.chdir(self.rundir)
        os.mkdir('run_parameters')
        shutil.copy(self.ref.itpfile, 'run_parameters')

        for prop in self.properties:
            os.chdir(self.rundir)           # NOTE Do I need this???
            self._init_prop(prop)

    def _init_prop(self, propname):
        """Create workdir for a property, copy/symplnk relevant files."""
        prop = self.ref.properties[propname]
        rodir = prop.workdir
        propdir = os.path.abspath(propname)
        os.mkdir(propdir)
        os.chdir(propdir)
        os.symlink(''.join(rodir, '/top'), propdir)
        os.mkdir('run')
        os.mkdir('gro')
        grofiles = (prop.groname.format(x, 'gro') for x in prop.data.x)
        for grofile in grofiles:
            os.symlink(''.join(rodir, '/gro/', grofile), 'gro')

    def run(self):
        """Run all properties."""
        # TODO: parallel? (num_cores)
        for prop in self.properties:
            self._run_prop(propname)

    def _run_prop(self, propname):
        prop = self.ref.properties[propname]
        rodir = prop.workdir
        propdir = os.path.abspath(''.join(self.rundir, '/', propname))
        gropath = ''.join('gro/', prop.groname)
        outpath = ''.join('run/', prop.groname)
        os.chdir(propdir)

        # TODO: parallelize
        grompp_result = []
        grompp_error = []
        grompp_tasks = ((self.ref.mdpfile,
                        prop.topfile,
                        gropath.format(x, 'gro'),
                        outpath.format(x, 'tpr')) for x in prop.data.x)
        with mp.Pool(None) as pool:
            pool.starmap(grompp,
                         grompp_tasks,
                         callback=grompp_result.append,
                         error_callback=grompp_error.append)

        # TODO: split mdrun??
        for x in prop.data.x:
            tprfile = os.abspath(outpath.format(x, tpr))[:-4]
            mdrun_process = mdrun(tprfile)
