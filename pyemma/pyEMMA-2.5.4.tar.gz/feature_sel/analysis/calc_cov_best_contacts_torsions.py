import socket
from glob import glob

import pyemma
from paths import missing, get_output_file_name

print('pyemma path:', pyemma.__path__)
import numpy as np
import sys
import os
sys.path.append(os.path.expanduser('~/workspace/pyemma/feature_sel/analysis/'))

from pyemma._ext.sklearn.parameter_search import ParameterGrid

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


grid = ParameterGrid([{'0_test_system': test_systems,
                       'lag': [500],  # dt=200ps, lag=100ns
                       'score': ['VAMP2'],
                       '1_feature': ['flex_torsions+best_contact'],
                       }])


import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='/group/ag_cmb/scratch/marscher/feature_sel/')
parser.add_argument('--lag', type=int, default=500) # dt=200ps, lag=500ns
parser.add_argument('--best', action='store_true', default=True)
parser.add_argument('--only_best_c', action='store_true', default=False)
parser.add_argument('id_', type=int)
args = parser.parse_args()

output_path = args.output
if not os.path.exists(output_path):
    sys.exit(23)


print('grid len:', len(grid))


def __myrepr__(x):
    s = ",".join([str(x_) for x_ in x])
    return s


#print("missing:\n%s" % __myrepr__(missing(grid=grid, output_path=output_path)))

def best_scoring_contact_feature(test_system, score):
    # determine best scoring contact feature.
    pattern = '{out}/scores_test_sys_{sys}*_res_mindist_c*_score_{score}*.npz'.format(out=output_path, sys=test_system,
                                                                                      score=score)
    scores_contacts = glob(pattern)
    assert scores_contacts
    best = 0 if args.best else float('inf')
    best_scoring_contact_file = None
    print('maximize: ', args.best)

    def cmp(opt, b):
        if args.best:
            #print('{b} > {opt}'.format(opt=opt, b=b))
            res = b > opt
        else:
            #print('{b} < {opt}'.format(opt=opt, b=b))
            res = b < opt
        #print('better:', res)
        return res

    for fsc in scores_contacts:
        with np.load(fsc) as fh:
            # TODO: normalize with std deviation?!
            s = fh['scores'].mean()
            if cmp(best, s):
                print('new opt:', s)
                best = s
                best_scoring_contact_file = fsc
    assert best_scoring_contact_file
    assert best != 0

    print('best_scoring_contact_file:', best_scoring_contact_file)
    match = re.match('.*res_mindist_c_(.*)_score.*', best_scoring_contact_file)
    assert match
    c = float(match.group(1))

    return best_scoring_contact_file, c


def run(id_):
    print('job number: %s' % id_)
    params = grid[id_]

    test_system = params['0_test_system']
    lag = params['lag']
    score = params['score']
    try:
        best_scoring_contact_file, c = best_scoring_contact_feature(test_system=test_system, score=score)
        if args.only_best_c:
            sys.exit(0)

        import re
        import paths as p
        import estimate as e
        cov = None

        for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            grid.param_grid[0]['k'] = [k]
            fname = p.get_output_file_name(grid, id_)
            print('output file:', fname)
            if os.path.exists(fname):
                print("results file %s already exists. Skipping" % fname)
                continue

            fname_cov = os.path.join(output_path, p.get_output_file_name(grid, id_, include_k=False) + '_covs.h5')
            if not os.path.exists(fname_cov):
                print('estimating covs')
                #  create FragmentedReader per feature, which groups all the files of a system.
                # independent runs for each test system are named like $test_system-[0-9]-feat.dcd.h5
                reader_contacts = p.create_fragmented_reader(test_system=test_system, feature='res_mindist')
                reader_flextorsions = p.create_fragmented_reader(test_system=test_system, feature='flex_torsions')

                assert reader_contacts.n_frames_total()
                assert reader_flextorsions.n_frames_total()
                assert reader_contacts.n_frames_total() == reader_flextorsions.n_frames_total()

                # re-calc contacts (apply cutoffs)

                trans = p.DistTrans(reader_contacts.dimension(), c=c)
                trans.data_producer = reader_contacts
                reader_contacts = trans
                assert isinstance(reader_contacts, p.DistTrans)

                from pyemma.coordinates import combine_sources
                reader = combine_sources((reader_contacts, reader_flextorsions), chunksize=0)
                assert reader.n_frames_total()

                from pyemma.coordinates.estimation.covariance import Covariances
                cov = Covariances(n_covs=100, tau=lag, mode='sliding', n_save=1, fixed_seed=False)
                cov.estimate(reader)
                print('finished covs calc, scoring...')
                cov.save(fname_cov)
            elif cov is None:
                print('loading covs from', fname_cov)
                cov = pyemma.load(fname_cov)

            assert cov is not None

            from sklearn.model_selection import KFold
            splitter_input = KFold(n_splits=50)
            scores = cov.score_cv(n=100, k=k, n_jobs=8,
                                  scoring_method='VAMP2', splitter=splitter_input,
                                  return_singular_values=False)
            print('finished scoring... %s' % id_)
            parameters = np.array({'lag': lag,
                                   'splitter': 'kfold',
                                   'mode': 'sliding',
                                   'test_system': test_system,
                                   'scoring_method': score,
                                   'contact_cutoff': c,
                                   'k': k,
                                   })

            results = {'scores': scores}

            np.savez_compressed(fname, parameters=parameters, **results)

    except BaseException as e:
        print('bad:', e, id_)
        print('failed on node:', socket.gethostname())
        import traceback
        traceback.print_exc()
        import pdb
        pdb.post_mortem()
        sys.exit(1)
    else:
        print('successful %s' % id_)

if __name__ == '__main__':
    run(args.id_)
