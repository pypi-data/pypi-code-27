# -*- coding: utf-8 -*-
import pandas as _pd

def normalize(df, style = 'mean'):
    if style == 'mean':
        df_mean,df_std = df.mean(),df.std()
        return (df-df_mean)/df_std
    elif style == 'minmax':
        col_min,col_max = df.min(),df.max()
        return (df-col_min)/(col_max-col_min)

def col_normalize(df,col_name, style = 'mean'):
    return normalize(df[col_name],style)

def row_normalize(df,row_name,style = 'mean'):
    return normalize(df.loc[row_name,:],style)

def norms(df, col_names = None,row_names = None,style = 'mean', as_group = False, axis = 0):
    if col_names is None:
        if row_names is not None:
            df = df.loc[row_names,:]
    else:
        if row_names is None:
            df = df.loc[:,col_names]
        else:
            df = df.loc[row_names,col_names]
    if as_group:
        return normalize(df,style)
    if axis == 0:
        return _pd.concat([col_normalize(df,col_name,style) for col_name in df.columns],axis = 1)
    elif axis == 1:
        return _pd.concat([row_normalize(df,row_name,style) for row_name in df.index])
    else:
        return normalize(df,style)

