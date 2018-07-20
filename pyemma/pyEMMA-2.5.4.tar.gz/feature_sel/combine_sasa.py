#from celery import Celery, group
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'analysis'))

broker_url = 'amqp://marscher:foobar@wallaby:5672/myvhost'
#app = Celery('transform_task', broker=broker_url)


test_systems = ['1FME', '2F4K', '2JOF', '2WAV', 'A3D', 'CLN025', 'GTT', 'lambda', 'NuG2', 'PRB', 'UVF',
                'NTL9-0-protein_fixed_CC'
                ]

from glob import glob
files = glob('/group/ag_cmb/marscher/feature_sel/cached_feat/shrake_ruply_by_atom/*.h5')
assert files
import paths as p

topology_cache = {}


#@app.task
def merge_to_residue(file):
    print('transforming: ', file)
    import tables
    import h5py as h
    def t(ds, fn):
        """
  for (i = 0; i < n_frames; i++) {
    asa_frame(xyzlist + i*n_atoms*3, n_atoms, atom_radii, sphere_points,
	      n_sphere_points, wb1, wb2, outframebuffer);
    outframe = out + (n_groups * i);
    for (j = 0; j < n_atoms; j++) {
        outframe[atom_mapping[j]] += outframebuffer[j];
    }
  }
        """
        import numpy as np
        import mdtraj
        test_sys = os.path.basename(fn).split('-')[0]
        if test_sys not in topology_cache:
            traj_top_pairs = p.create_traj_top_pairs(test_sys)
            top = mdtraj.load(traj_top_pairs['top']).topology
            topology_cache[test_sys] = top
        else:
            top = topology_cache[test_sys]
        sasa_by_atom = ds[:,:]
        # mapping per residue
        atom_mapping = np.array(
            [a.residue.index for a in top.atoms], dtype=np.int32)
        mapped = np.zeros((len(sasa_by_atom), top.n_residues), dtype=np.float32)
        for by_atom, out in zip(sasa_by_atom, mapped):
            for j in range(top.n_atoms - 1):
                out[atom_mapping[j]] += by_atom[j]
        if np.all(sasa_by_atom != 0.0):
            assert np.all(mapped != 0.0)
        return mapped

    with h.File(file, mode='a') as f:
        if 'shrake_ruply_residue' in f:
            print('already transformed:', file)
            return 
        ds = f['/shrake_ruply']
        trans = t(ds, file)
        f.create_dataset('shrake_ruply_residue', chunks=True, compression=32001, data=trans)

if __name__ == '__main__':
    from progress_reporter import ProgressReporter_
    pg = ProgressReporter_()
    pg.register(len(files))
    for f in files[:]:
        merge_to_residue(f)
        pg.update(1)


