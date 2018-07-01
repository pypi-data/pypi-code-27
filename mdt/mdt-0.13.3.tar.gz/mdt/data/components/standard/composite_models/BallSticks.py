from mdt import CompositeModelTemplate
import numpy as np

__author__ = 'Robbert Harms'
__date__ = "2015-06-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class BallStick_r1(CompositeModelTemplate):

    description = 'The default Ball & Stick model'
    model_expression = '''
        S0 * ( (Weight(w_ball) * Ball) +
               (Weight(w_stick0) * Stick(Stick0)) )
    '''
    fixes = {'Ball.d': 3.0e-9,
             'Stick0.d': 1.7e-9}

    extra_optimization_maps = [
        lambda results: {'FS': results['w_stick0.w']},
        lambda results: {'FS.std': results['w_stick0.w.std']}
    ]
    extra_sampling_maps = [
        lambda samples: {'FS': np.mean(samples['w_stick0.w'], axis=1),
                         'FS.std': np.std(samples['w_stick0.w'], axis=1)}
    ]


class BallStick_r2(CompositeModelTemplate):

    description = 'The Ball & 2x Stick model'
    model_expression = '''
        S0 * ( (Weight(w_ball) * Ball) +
               (Weight(w_stick0) * Stick(Stick0)) +
               (Weight(w_stick1) * Stick(Stick1)) )
    '''
    fixes = {'Ball.d': 3.0e-9,
             'Stick0.d': 1.7e-9,
             'Stick1.d': 1.7e-9}

    sort_maps = [('w_stick0', 'w_stick1'), ('Stick0', 'Stick1')]

    extra_optimization_maps = [
        lambda results: {'FS': 1 - results['w_ball.w']},
        lambda results: {'FS.std': results['w_ball.w.std']}
    ]
    extra_sampling_maps = [
        lambda samples: {
            'FS': np.mean(samples['w_stick0.w'] + samples['w_stick1.w'], axis=1),
            'FS.std': np.std(samples['w_stick0.w'] + samples['w_stick1.w'], axis=1)}
    ]

    extra_prior = 'return w_stick1.w < w_stick0.w;'


class BallStick_r3(CompositeModelTemplate):

    description = 'The Ball & 3x Stick model'
    model_expression = '''
            S0 * ( (Weight(w_ball) * Ball) +
                   (Weight(w_stick0) * Stick(Stick0)) +
                   (Weight(w_stick1) * Stick(Stick1)) +
                   (Weight(w_stick2) * Stick(Stick2)) )
        '''
    fixes = {'Ball.d': 3.0e-9,
             'Stick0.d': 1.7e-9,
             'Stick1.d': 1.7e-9,
             'Stick2.d': 1.7e-9}
    inits = {'w_stick2.w': 0}

    sort_maps = [('w_stick0', 'w_stick1', 'w_stick2'), ('Stick0', 'Stick1', 'Stick2')]

    extra_optimization_maps = [
        lambda results: {'FS': 1 - results['w_ball.w']},
        lambda results: {'FS.std': results['w_ball.w.std']}
    ]
    extra_sampling_maps = [
        lambda samples: {
            'FS': np.mean(samples['w_stick0.w'] + samples['w_stick1.w'] + samples['w_stick2.w'], axis=1),
            'FS.std': np.std(samples['w_stick0.w'] + samples['w_stick1.w'] + samples['w_stick2.w'], axis=1)}
    ]

    extra_prior = 'return w_stick2.w < w_stick1.w && w_stick1.w < w_stick0.w;'
