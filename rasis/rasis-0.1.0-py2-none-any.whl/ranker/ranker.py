# -*- coding: utf-8 -*-

"""Module ranker contains class Ranker.
"""


import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    import pandas
import json
import numpy

class Ranker:

    """Ranker processes the ranking data from crawler and do some simple
    analysis jobs.

    """

    df_score = None
    df_tune = None

    def __init__(self, workdir):

        """__init__ reads output of crawler and initializes the dataframes.

        Parameters
        ----------
        workdir : str

        """

        self.df_score = pandas.read_csv(workdir + '/scores.csv', encoding='utf-8',
            index_col=['rank', 'tune_id'], dtype={
                'rank': numpy.int,
                'score': numpy.int,
                'tune_id': numpy.int,
            }
        )
        self.df_tune = pandas.read_csv(workdir + '/tunes.csv', encoding='utf-8',
            index_col='id', dtype={
                'id': numpy.int,
                'level': numpy.int,
            }
        )

    def puc(self, tune_info):

        """puc returns the puc players of a tune.

        Parameters
        ----------
        tune_info : (title, diff)
            A tuple. The first element is the title of the tune, and the second
            is the diff. The possible values of diff are {'nov', 'adv',
            'exh', 'mxm', 'grv', 'hvn', 'inf'}

        Returns
        -------
        pandas.DataFrame

        """

        title, diff = tune_info
        tune_id = self.df_tune[(self.df_tune['title'] == title) &
            (self.df_tune['diff'] == diff)].index[0]
        df_tune_score = self.df_score.xs(tune_id, level='tune_id')
        return df_tune_score[df_tune_score['score'] == 10000000]
