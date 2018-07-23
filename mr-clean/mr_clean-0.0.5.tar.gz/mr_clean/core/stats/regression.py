# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
#import mr_clean.core.functions.basics as basics
from mr_clean._utils.data_handling import rows,cols

def corr_matrix(df,method = 'pearson'):
    """ Returns a matrix of correlations between columns of a DataFrame. For categorical columns,
    it first changes those to a set of dummy variable columns. Booleans are converted to
    numerical as well. Also ignores any indexes set on the DataFrame
    Parameters:
    df - DataFrame
        DataFrame to analyze
    method - {'pearson', 'kendall', 'spearman'}
        * pearson : standard correlation coefficient
        * kendall : Kendall Tau correlation coefficient
        * spearman : Spearman rank correlation
    """
    # Remove all but categoricals,booleans, and numerics
    df = df.reset_index(drop = True)
    cat_cols = df.select_dtypes(include = 'category')
    bool_cols = df.select_dtypes(include = 'bool')
    df = df.select_dtypes(include = 'number')
    if not cols(df) + cols(bool_cols) + cols(cat_cols):
        return None # quit if there's none of the possible datatypes present

    #Convert categoricals to boolean columns
    insert = np.ones(rows(df))
    for col_name in cat_cols:
        cat_df = pd.concat([cat_cols[[col_name]],pd.Series(insert)],axis = 1) # Add a column of ones as values for the pivot
        cat_ptable = cat_df.pivot(columns = col_name).reset_index(drop = True)
        cat_ptable.columns = [col_name+ "_{}".format(value) for value in
                                  cat_ptable.columns.get_level_values(col_name)]
        df = pd.concat([df,cat_ptable.fillna(0)],axis = 1)
    df = pd.concat([df,bool_cols * 1], axis = 1)
    return df.corr(method,0)

#
#%%%
#np.array([1,2,3,1,2,3,1,2,3,2])
#df = pd.DataFrame({'col1':np.array([1,2,3,1,2,3,1,2,3,2]),'col2':np.array([1,2,3,1,2,3,1,2,3,2]),'col3':np.array([1,2,3,1,2,3,1,2,3,2])})
#df.index = ['oneboi','twodne','threeoain','fouroqwn','five','size','sven','ight','noef','tinnny']
#col_name = 'col1'
#df[col_name] = df[col_name].astype('category')
#df['col2'] = df['col2'].astype('category')
#ndf = df.pivot(columns = col_name).reset_index(drop = True).iloc[:,0:len(df[col_name].cat.categories)]
#ndf.columns = [col_name+ "_{}".format(value) for value in ndf.columns.get_le
#vel_values(col_name)]
#fdf = ndf.notna() * 1