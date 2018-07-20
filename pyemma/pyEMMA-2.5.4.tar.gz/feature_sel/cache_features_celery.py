#!/usr/bin/env python

from celery import Celery
from celery.utils.log import get_task_logger
import socket

from glob import glob

import tables
import h5py

import numpy as np
import pyemma


fast_folders_dir_src = '/nfs/group/ag_cmb/simulation-data/DESRES-Science2011-FastProteinFolding/'
#fast_folders_dir_dest = os.path.join(os.path.expanduser('~'), 'NO_BACKUP/data/feature_sel/')
fast_folders_dir_dest = '/group/ag_cmb/simulation-data/DESRES-Science2011-FastProteinFolding/'
test_systems = [
                # '1FME',
                # '2F4K',
                # '2JOF',
                # '2WAV',
                # 'A3D',
                'CLN025',
                # 'GTT',
                # 'lambda',
                # 'NuG2',
                # 'PRB',
                # 'UVF',
                # 'NTL9'
]

def copy_data():
    from distutils.dir_util import copy_tree
    for part in test_systems:
        pattern = fast_folders_dir_src + '/' + '*' + part + '*'
        dirs = glob(pattern)
        for d in dirs:
            print('copying %s ... ' % d)
            copy_tree(d, fast_folders_dir_dest)


def create_traj_top_pairs(test_system):
    # match trajectory files with topology

    if 'NTL9' not in test_system:
        patterns = fast_folders_dir_dest + '/*' + test_system + '*/*/*.dcd'
        top = glob(fast_folders_dir_dest + '/*' + test_system + '*/*' + test_system + '*/*.pdb')[0]
    else:
        patterns = fast_folders_dir_dest + '/' + test_system + '*/*.dcd'
        top = glob(fast_folders_dir_dest + '/' + test_system + '*/*.pdb')[0]

    trajs = sorted(glob(patterns))
    assert trajs
    assert top
    try:
        import mdtraj
        mdtraj.load_frame(trajs[0], top=top, index=0)
    except ValueError:
        raise RuntimeError('topology {} for {} does not match trajs'.format(top, test_system))
    trajs_with_top = [(traj, top) for traj in trajs]
    return trajs_with_top


#### features
def shrake_ruply(featurizer):
    def featurize(traj):
        import mdtraj
        res = mdtraj.shrake_rupley(traj, probe_radius=0.14, n_sphere_points=960, mode='residue')
        return res

    featurizer.add_custom_func(featurize, dim=featurizer.topology.n_residues)


def backbone(featurizer):
    featurizer.add_backbone_torsions(cossin=True)


def dist_ca(featurizer):
    featurizer.add_distances_ca()


def res_mindist(featurizer):
    featurizer.add_residue_mindist(scheme='closest-heavy')


def flex_torsions(featurizer):
    featurizer.add_sidechain_torsions(cossin=True)
    featurizer.add_backbone_torsions(cossin=True)


def side_sidechain_torsions(featurizer):
    print("adding feature sidechain torssions to featurizer")
    from mdtraj.geometry.dihedral import indices_chi1, indices_chi2, indices_chi3, indices_chi4, indices_chi5, \
        indices_omega
    top = featurizer.topology
    indices = np.vstack((indices_chi1(top),
                         indices_chi2(top),
                         indices_chi3(top),
                         indices_chi4(top),
                         indices_chi5(top),
                         indices_omega(top)))
    assert indices.shape[1] == 4
    from mdtraj import compute_dihedrals

    def compute_side_chains(traj):
        res = compute_dihedrals(traj, indices)
        # cossin
        rad = np.dstack((np.cos(res), np.sin(res)))
        rad = rad.reshape(rad.shape[0], rad.shape[1] * rad.shape[2])
        print('shape chunk:',rad.shape)
        return rad

    featurizer.add_custom_func(compute_side_chains, dim=len(indices)*2)


def dssp(featurizer):
    dim = featurizer.topology.n_residues
    from mdtraj import compute_dssp
    codes = ('H', 'B', 'E', 'G', 'I', 'T', 'S', ' ', )#'NA')

    mapping = {}
    for i, c in enumerate(codes):
        vec = np.zeros_like(codes, dtype=np.float32)
        vec[i] = 1
        mapping[c] = vec
    #
    mapping['NA'] = np.zeros_like(codes, dtype=np.float32)

    def _compute(traj):
        result = np.empty( (len(traj),  traj.topology.n_residues, len(codes)), dtype=np.float32)
        assignment = compute_dssp(traj, simplified=False)
        for i, a_ in enumerate(assignment):
            for j, a in enumerate(a_):
                val = mapping.get(a, None)
                if val is None:
                    raise Exception('code at position %s could not be decoded: "%s"' % (i,c))
                result[i, j, :] = val

        result = result.reshape((len(traj), -1))
        return result

    featurizer.add_custom_func(_compute, dim=dim*len(codes))


features = (
#dssp,
#    side_sidechain_torsions,
#    dist_ca,
#    res_mindist,
#    backbone,
#    shrake_ruply,
#    flex_torsions,
    shrake_ruply,
)
#### end of features



from sklearn.model_selection import ParameterGrid
import itertools
stuff = [create_traj_top_pairs(test_system=t) for t in test_systems]
flat = list(itertools.chain.from_iterable(stuff))
param_grid = {'traj_top': flat,
              'feature': features,
              }

grid = ParameterGrid(param_grid)
# this should be equal to njobs for slurm!
print("num total jobs:", len(list(grid)))

broker_url = 'amqp://marscher:foobar@goose:5672/myvhost'
app = Celery('tasks', broker=broker_url)


@app.task
def run(id):
    print('job number: %s' % id)
    import os
    os.chdir('/group/ag_cmb/marscher/feature_sel/cached_feat/')

    params = grid[id]
    pyemma.config.coordinates_check_output=True

    traj, top = params['traj_top']
    feature = params['feature']
    feature_name = feature.__name__

    print('running on:', socket.gethostname())
    print('top: {} \n\ntrajs: {}'.format(top, traj))

    try:
        reader = pyemma.coordinates.source([traj], top=top, chunksize=500)
        featurizer = reader.featurizer
        # add feature to featurizer.
        feature(featurizer)


        file_name = "{traj}_{feat}.h5".format(traj=os.path.basename(traj), feat=feature_name)
        print("writing to:", os.path.abspath(file_name))
        reader.write_to_hdf5(filename=file_name, data_set_prefix=feature_name,
                             h5_opt=dict(compression=32001, chunks=True, shuffle=True))
        with h5py.File(name=file_name, mode='a') as f:
            created_name = tuple(f.keys())[0]
            f[feature_name] = f[created_name]
            del f[created_name]

    except BaseException as e:
        print('bad:', e, id)
        import traceback
        traceback.print_last()

    print('successful')
    #handler.close()


def spawn(id):
    print("<START> id=", id)
    run(id)
    print("<END> id=", id)


if __name__ == '__main__':
    import os
    import sys
    id = int(sys.argv[1])
    spawn(id)
