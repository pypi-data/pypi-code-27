# External modules
from ase.io     import read     # type: ignore
from glob       import glob
# Internal modules
from dbgen.scripts.Pure.Atoms.traj_to_json import traj_to_json
################################################################################
def anytraj_sherlock(root : str) -> str:
    """
    ASE IO read function - takes any traj it can find
    """
    trajs = glob('%s/*.traj'%root)
    if len(trajs) == 0:
        raise ValueError('Get Traj could not find any traj in '+root)
    else:
        atoms = read(trajs[0])
        return traj_to_json(atoms)

if __name__=='__main__':
    import sys
    print(anytraj_sherlock(sys.argv[1]))
