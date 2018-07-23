# -*- coding: utf-8 -*-
import pandas as _pd

def normalize(df, style = 'mean'):
    """ Returns a normalized version of a DataFrame or Series
    Parameters:
    df - DataFrame or Series
        The data to normalize
    style - function or string, default 'mean'
        The style to use when computing the norms. Takes 'mean' or 'minmax' to
        do mean or min-max normalization respectively. User-defined functions that take
        a pandas Series as input and return a normalized pandas Series are also accepted
    """
    if style == 'mean':
        df_mean,df_std = df.mean(),df.std()
        return (df-df_mean)/df_std
    elif style == 'minmax':
        col_min,col_max = df.min(),df.max()
        return (df-col_min)/(col_max-col_min)
    else:
        return style(df)

def col_normalize(df,col_names, style = 'mean'):
    """ Returns a normalized version of a set of columns in the input Dataframe 
    Parameters:
    df - pandas DataFrame
        The input data to normalize
    col_names - list or string, default None
        The column(s) to use when computing the norms
    style - function or string, default 'mean'
        The style to use when computing the norms. Takes 'mean' or 'minmax' to
        do mean or min-max normalization respectively. User-defined functions that take
        a pandas Series as input and return a normalized pandas Series are also accepted
    """
    return normalize(df[col_names],style)

def row_normalize(df,row_names,style = 'mean'):
    """ Returns a normalized version of a set of rows in the input Dataframe
    Parameters:
    df - pandas DataFrame
        The input data to normalize
    row_names - list or string, default None
        The row(s) to use when computing the norms
    style - function or string, default 'mean'
        The style to use when computing the norms. Takes 'mean' or 'minmax' to
        do mean or min-max normalization respectively. User-defined functions that take
        a pandas Series as input and return a normalized pandas Series are also accepted
    """
    return normalize(df.loc[row_names,:],style)

def norms(df, col_names = None,row_names = None,style = 'mean', as_group = False, axis = 0):
    """ Returns a normalized version of the input Dataframe
    Parameters:
    df - pandas DataFrame
        The input data to normalize
    col_names - list or string, default None
        The column(s) to use when computing the norms
    row_names - list or string, default None
        The row(s) to use when computing the norms
    style - function or string, default 'mean'
        The style to use when computing the norms. Takes 'mean' or 'minmax' to
        do mean or min-max normalization respectively. User-defined functions that take
        a pandas Series as input and return a normalized pandas Series are also accepted
    as_group - bool, default False
        Whether to normalize accross the entire range or by row/column. If true, will normalize
        by the entire DataFrame
    axis - int or string, default 0
        Which axis to perform the normalization on. Accepts 0 or 'columns' to do normalization by
        columns, and 1 or 'rows' to do normalization by rows
    """
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
    if axis == 0 or str(axis).startswith('column'):
        return _pd.concat([col_normalize(df,col_name,style) for col_name in df.columns],axis = 1)
    elif axis == 1 or str(axis).startswith('row'):
        return _pd.concat([row_normalize(df,row_name,style) for row_name in df.index])
    else:
        return normalize(df,style)

