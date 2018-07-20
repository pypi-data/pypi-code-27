import sys

import numpy as np
sys.path.append('/home/mi/marscher/workspace/pyemma/feature_sel/analysis/')
sys.path.append('/home/feature_sel/analysis/')

from pyemma._ext.sklearn.parameter_search import ParameterGrid
import progress_reporter
pg = progress_reporter.ProgressReporter_()

test_systems = [
   '1FME',
   '2F4K',
   '2JOF',
   '2WAV',
   'A3D',
   'CLN025',
   'GTT',
   'lambda',
   'NuG2',
   'PRB',
   'UVF',
   'NTL9',
]

features = ('xyz',
            'dist_ca', # TODO: this is the same feature as res_mindist basically.
            'flex_torsions',
            'shrake_ruply_residue',
            'res_mindist',
            'res_mindist_d1',
            'res_mindist_d2',
            'res_mindist_expd',
            'res_mindist_c_0.4',
            'res_mindist_c_0.5',
            'res_mindist_c_0.6',
            'res_mindist_c_0.8',
            'res_mindist_c_1.0',
            )

# prefix test sys and feature to force sorting group these.
grid = ParameterGrid([{'0_test_system': test_systems,
                       '1_feature': list(features),
                       }])

def compute_mean(reader, chunk=100):
    mean = np.zeros(reader.ndim)
    n = 1
    pg.register(reader.n_chunks(chunk), 'compute mean')
    for chunk in reader.iterator(chunk=chunk, return_trajindex=False):
        mean += (chunk - mean).sum(axis=0) / float(n)
        n += len(chunk)
        pg.update(0)
    return mean


import paths as p
if __name__ == '__main__':
    for test_sys in test_systems:
        for feat in features:
            if feat == 'xyz':
                reader = p.create_cartesian_reader(test_sys)
            else:
                reader = p.create_fragmented_reader(test_sys, feat)

            mean = compute_mean(reader)
            np.save('mean_test_sys_{test_sys}_feat_{feat}.npy', mean)
            break
