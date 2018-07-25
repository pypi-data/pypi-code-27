# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:53:23 2015

@author: rbanderson
"""
import pandas as pd
import libpysat.transform.remove_baseline as remove_baseline
import libpysat.transform.interp as interp
import libpysat.transform.mask as mask
import libpysat.transform.multiply_vector as multiply_vector
import libpysat.transform.peak_area as peak_area
import libpysat.transform.shift_spect as shift_spect
import libpysat.utils.folds as folds
import libpysat.transform.norm as norm
import libpysat.transform.deriv as deriv
import libpysat.transform.dim_red as dim_red
import libpysat.clustering.cluster as cluster
import libpysat.utils.outlier_removal as outlier_removal
from libpysat.utils.utils import enumerate_duplicates

class spectral_data(object):
    def __init__(self, df):

        #get the two levels of column names
        try:
            uppercols = df.columns.levels[0]
            lowercols = list(df.columns.levels[1].values)
        #if the columns are not multiindexes, then they should be tuples, so convert them
        except:
            # check for columns that are not tuples and remove them.
            # This can happen if two columns have identical labels on both levels:
            # the second one will be recorded as a string
            to_drop = []
            for i in range(len(df.columns)):
                if not isinstance(df.columns[i],tuple):
                    print('WARNING: '+str(df.columns[i])+' is not a tuple (this can be caused by duplicate column names). Removing this column.')
                    to_drop.append(df.columns[i])
            df.drop(columns=to_drop,inplace=True)
            df.columns = pd.MultiIndex.from_tuples(list(df.columns))
            uppercols = df.columns.levels[0]
            lowercols = list(df.columns.levels[1].values)

        for i, val in enumerate(lowercols):
            try:
                lowercols[i] = float(val)
            except:
                lowercols[i] = val

        levels = [uppercols, lowercols]
        df.columns.set_levels(levels, inplace=True)
        self.df = df

    def cal_tran(self):
        pass #Not yet implemented

    def cluster(self, col, method, params, kws):
        self.df = cluster.cluster(self.df, col = col, method = method, params = params, kws = kws)

    def deriv(self):
        self.df = deriv.deriv(self.df)

    def dim_red(self, col, method, params, kws, load_fit):
        self.df, self.dim_red = dim_red.dim_red(self.df, col = col, method = method, params = params, kws = kws, load_fit = load_fit)

    def interp(self, xnew):
        self.df = interp.interp(self.df, xnew)

    def shift(self, shift):
        self.df = shift_spect.shift_spect(self.df, shift)

    def mask(self, maskfile, maskvar):
        self.df = mask.mask(self.df,maskfile,maskvar=maskvar)

    def multiply_vector(self, vectorfile):
        self.df = multiply_vector.multiply_vector(self.df,vectorfile=vectorfile)

    def norm(self, ranges, col_var):
        self.df = norm.norm(self.df,ranges, col_var=col_var)

    def outlier_removal(self, col, method, params):
        self.df, self.outlier_removal = outlier_removal.outlier_removal(self.df, col = col, method = method, params = params)

    def peak_area(self, peaks_mins_file):
        self.df, self.peaks, self.mins = peak_area.peak_area(self.df,peaks_mins_file = peaks_mins_file)

    def random_folds(self, nfolds):
        self.df = folds.random(self.df,nfolds)

    def remove_baseline(self, method, segment, params):
        self.df = remove_baseline.remove_baseline(self.df, method = method, segment = segment, params = params)

    def stratified_folds(self):
        self.df, self.df_baseline = folds.stratified_folds(self.df, nfolds = 5, sortby = None)

    def enumerate_duplicates(self, col):
        self.df = enumerate_duplicates(self.df, col=col)



