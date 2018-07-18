# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import mr_clean._utils.data_handling as _utils
import mr_clean.core.functions.basics as _basics

def dtypes_summary(df):
    """ Takes in a dataframe and returns a dataframe with
    information on the data-types present in each column.
    Parameters:
    df - DataFrame
        Dataframe to summarize
    """
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
        value_counts = data.value_counts().reset_index()
        # number of different values in the dataframe
        categories = len(value_counts)
        # largest category
        largest_category = value_counts.iloc[0,1]
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

def percentiles(df,q =[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]):
    """ Takes a dataframe and returns the quantiles for each column,
    or an error message if there are no columns with quantitative data.
    Parameters:
    df - DataFrame
        The dataframe to analyze
    q - number or list of numbers, default [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
        Quantiles to get
    """
    try:
        return df.quantile(q = q)
    except ValueError:
        return None#"No columns with numeric data."

def df_outliers(df,sensitivity = 1.5):
    """ Finds outliers in the dataframe.
    Parameters:
    df - DataFrame
        The DataFrame to analyze.
    sensitivity - number, default 1.5
        The value to multipy by the iter-quartile range when determining outliers. This number is used
        for categorical data as well.
    """
    outlier_df = df.copy()
    dtypes = _basics.col_dtypes(df)
    for col_name in df.columns:
        outlier_df.loc[~outliers(df[col_name],'bool',dtypes[col_name],sensitivity),col_name] = np.nan
    outlier_df = outlier_df.dropna(how = 'all')
    return outlier_df

def outliers(df,output_type = 'values',dtype = 'number',sensitivity = 1.5):# can output boolean array or values
    """ Returns potential outliers as either a boolean array or a subset of the original.
    Parameters:
    df - array_like
        Series or dataframe to check
    output_type - string, default 'values'
        if 'values' is specified, then will output the values in the series that are suspected
        outliers. Else, a boolean array will be outputted, where True means the value is an outlier
    dtype - string, default 'number'
        the way to treat the object. Possible values are 'number','datetime',
        'timedelt','datetimetz','category',or 'object'
    sensitivity - number, default 1.5
        The value to multipy by the iter-quartile range when determining outliers. This number is used
        for categorical data as well.
    """
    if dtype in ('number','datetime','timedelt','datetimetz'):
        if not dtype == 'number':
            df = pd.to_numeric(df,errors = 'coerce')
        quart25, quart75 = percentiles(df,q = [.25,.75]) 
        out_range= sensitivity * (quart75 - quart25)
        lower_bound,upper_bound = quart25-out_range, quart75+out_range
        bool_array = (df < lower_bound)|(df > upper_bound)
    else:
        value_counts = df.value_counts() # Trying to find categorical outliers.
        quart25 = cum_percentile(value_counts,.25)
        quart75 = cum_percentile(value_counts,.75)
        out_values = int(sensitivity * (quart75 - quart25) + quart75 + 1)
        if out_values >= len(value_counts):
            bool_array = _utils.bc_vec(df,value = False)
        else:
            outlier_values = value_counts[value_counts <= value_counts.iloc[out_values]].index
            bool_array = df.isin(outlier_values)
        
    if output_type == 'values':
        return  df[bool_array]
    return bool_array

def cum_percentile(series,q):
    """ Takes a series of ordered frequencies and returns the value at a specified quantile
    Parameters:
    series - Series
        The series to analyze
    q - number
        Quantile to get the value of
    """
    total = series.sum()
    cum_sum = series.cumsum()
    return sum(cum_sum < total*q)
    
