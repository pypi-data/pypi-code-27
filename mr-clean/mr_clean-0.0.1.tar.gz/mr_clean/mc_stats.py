# -*- coding: utf-8 -*-
import pandas as pd

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
        return pd.concat([col_normalize(df,col_name,style) for col_name in df.columns],axis = 1)
    elif axis == 1:
        return pd.concat([row_normalize(df,row_name,style) for row_name in df.index])
    else:
        return normalize(df,style)

def percentiles(df):
    """ Takes a dataframe and returns the quartiles for each column,
    or an error message if there are no columns with quantitative data.
    """
    assert type(df) is pd.DataFrame
    try:
        return df.quantile(q = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1])
    except ValueError:
        return None#"No columns with numeric data."
    
def dtypes_summary(df):
    """ Takes in a dataframe and returns a dataframe with
    information on the data-types present in each column.
    """
    assert type(df) is pd.DataFrame
    output_df = pd.DataFrame([])
    row_count = df.shape[0]
    row_indexes = ['rows_numerical','rows_string','rows_date_time','category_count','largest_category','rows_na','rows_total']
    for colname in df:
        data = df[colname] # data is the pandas series associated with this column
        # number of numerical values in the column
        rows_numerical = pd.to_numeric(data,errors = 'coerce').count()
        # number of values that can't be coerced to a numerical
        rows_string = row_count - rows_numerical
        # number of values that can be coerced to a date-time object
        rows_date_time = pd.to_datetime(data,errors = 'coerce',infer_datetime_format = True).count()
        # categories in column
        value_counts = data.value_counts()
        # number of different values in the dataframe
        categories = data.value_counts().count()
        # largest category
        largest_category = value_counts[0]
        # number of null/missing values
        rows_na = data.isnull().sum()
        # build the output list
        output_data = [rows_numerical, rows_string, rows_date_time, categories, 
                       largest_category,rows_na,row_count]
        # add to dataframe
        output_df.loc[:,colname] = pd.Series(output_data)

    # row names
    output_df.index = row_indexes
    return output_df