import matplotlib
matplotlib.use('Agg')
import pylab

import pyemma

print('pyemma path:', pyemma.__path__)
import numpy as np
import sys
import os

from pyemma._ext.sklearn.parameter_search import ParameterGrid

test_systems = [
    #'1FME',
    #'2F4K',
    #'2JOF',
    #'2WAV',
    'A3D',
    #'CLN025',
    #'GTT',
    #'lambda',
    #'NuG2',
    #'PRB',
    #'UVF',
    #'NTL9',
]

k_per_system = {'A3D': 7,
                'CLN025': 5,
                'PRB': 10}


features = ['flex_torsions', 'res_mindist_expd']


grid = ParameterGrid([{'0_test_system': test_systems,
                       #'lag': [500],  # dt=200ps, lag=100ns
                       'lag': [500, 750, 1000, 1250, 1500, 1750, 2000],
                       '1_feature': features,
                       'k': [100],#, 150, 200, 250],
                       }])

from pprint import pprint
for i, p in enumerate(grid):
    print(i,p)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='/group/ag_cmb/marscher/feature_sel/msm_low_rank/')
parser.add_argument('id_', type=int)
args = parser.parse_args()

output_path = args.output

if not os.path.exists(output_path):
    sys.exit(23)


def get_output_file_name(grid, id_):
    params = grid[id_]
    feature = params['1_feature']
    test_system = params['0_test_system']
    k = params['k']

    fname_its = os.path.join(output_path, 'its_test_sys_{test_system}_nstates_{n_states}_feat_{feature}.pdf'.format(
        test_system=test_system,
        feature=feature,
        n_states=k
    ))
    fname_cktest = os.path.join(output_path, 'cktest_test_sys_{test_system}_nstates_{n_states}_feat_{feature}.pdf'.format(
         test_system=test_system,
         feature=feature,
         n_states=k
    ))
    fname_cluster = os.path.join(output_path, 'cl_test_sys_{sys}_nstates_{n_states}_feat_{feat}.h5'.format(
        sys=test_system, n_states=k, feat=feature))

    fname_msm = os.path.join(output_path, 'msm_score_test_sys_{sys}_lag_{lag}_feat_{feat}.npz'.format(
        sys=test_system, lag=params['lag'], feat=feature
    ))

    from collections import namedtuple
    t = namedtuple("output_names", ["its", "ck", "cl", "msm"])
    return t(fname_its, fname_cktest, fname_cluster, fname_msm)


def run(id):
    print('job number: ', id)
    params = grid[id]
    test_system = params['0_test_system']
    feature = grid[id]['1_feature']
    k = params['k']
    lag = params['lag']

    out_names = get_output_file_name(grid, id)
    print(out_names)
    fname_its = out_names.its
    fname_cktest = out_names.ck
    fname_cluster = out_names.cl
    fname_msm = out_names.msm

    if os.path.exists(fname_its):
        print("results file %s already exists. Skipping" % fname_its)

    print('current path: %s' % os.getcwd())
    try:
        if os.path.exists(fname_cluster):
            cluster = pyemma.load(fname_cluster)
        else:
            import paths as p
            if feature == 'xyz':
                reader = p.create_cartesian_reader(test_system)
            else:
                reader = p.create_fragmented_reader(test_system, feature)

            assert np.all(reader.trajectory_lengths() > 0)
            assert reader.chunksize > 0

            fname_cov = os.path.join(output_path, p.get_output_file_name(grid, id, include_k=False) + '_covs.h5')
            if os.path.exists(fname_cov):
                t = pyemma.load(fname_cov)
                t.data_producer = reader
            else:
                from pyemma.coordinates.transform import VAMP
                t = VAMP(lag=250, dim=5)
                t.estimate(reader)
            y = t.get_output(stride=3)

            cluster = pyemma.coordinates.cluster_kmeans(data=y, k=k, max_iter=100, stride=1, chunksize=20000)
            import collections
            dtrajs = collections.defaultdict(list)
            for itraj, x in t.iterator():
                dtrajs[itraj].append(cluster.assign(x))

            res = {}
            for itraj in dtrajs:
                res[itraj] = np.hstack(dtrajs[itraj])
                assert len(res[itraj]) == t.trajectory_length(itraj)

            cluster._dtrajs = [res[i] for i in range(reader.ntraj)]

            cluster.save(fname_cluster)

        msm = pyemma.msm.estimate_markov_model(cluster.dtrajs, lag=lag)
        scores_msm = msm.score_cv(cluster.dtrajs, score_k=k_per_system[test_system])
        np.save(fname_msm, arr=scores_msm)

        if not os.path.exists(fname_its):
            from pyemma.msm import timescales_msm
            from matplotlib.pylab import figure, savefig, title
            # its
            its = timescales_msm(cluster.dtrajs, lags=1000, errors='bayes', n_jobs=None, reversible=False)
            its.save(fname_its+'.h5')

            figure(1, figsize=(12, 8))
            ax = pyemma.plots.plot_implied_timescales(its, dt=.2, units='ns', nits=k_per_system[test_system])
            ax.axvline(500, linestyle='dashed', color='grey')
            title('Implied timescales for {sys} with feature {feat}'.format(sys=test_system, feat=feature))
            savefig(fname_its)
        # cktest
        #figure(1, figsize=(12, 8))
        # TODO: shouldn't this be 10 states, as we use 10 slowest processes in scoring?
        #ck = its.models[0].cktest(4)
        #pyemma.plots.plot_cktest(ck, diag=True)
        #savefig(fname_cktest)

    except BaseException as e:
        print('bad:', e, id)
        import traceback
        traceback.print_exc(file=sys.stdout)
        import pdb
        pdb.post_mortem()
        raise
    else:
        print('successful')


if __name__ == '__main__':
    run(args.id_)
