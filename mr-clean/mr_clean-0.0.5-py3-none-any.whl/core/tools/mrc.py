# -*- coding: utf-8 -*-
#import pandas as pd
import mr_clean.core.functions.basics as basics
from mr_clean.core.functions.scrub import smart_scrub
#import mr_clean.core.stats.summary as stats

def clean(df,error_rate = 0):
    """ Superficially cleans data, i.e. changing simple things about formatting.
    Parameters:
    df - DataFrame
        DataFrame to clean
    error_rate - float {0 <= error_rate <= 1}, default 0
        Maximum amount of errors/inconsistencies caused explicitly by cleaning, expressed
        as a percentage of total dataframe rows (0 = 0%, .5 = 50%, etc.)
        Ex: na values from coercing a column of data to numeric
    """
    df = df.copy()
    
    # Change colnames
    basics.clean_colnames(df)
    # Eventually use a more advanced function to clean colnames
    print('Changed colnames to {}'.format(df.columns))
    
    # Remove extra whitespace
    obj_col_list = df.select_dtypes(include = 'object').columns
    for col_name in obj_col_list:
        df[col_name] = basics.col_strip(df,col_name)
        print("Stripped extra whitespace from '{}'".format(col_name))
    
    # Coerce columns if possible
    for col_name in obj_col_list:
        new_dtype = coerce_col(df,col_name,error_rate)
        if new_dtype is not None:
            print("Coerced '{}' to datatype '{}'".format(col_name, new_dtype))

    # Scrub columns
    obj_col_list = df.select_dtypes(include = 'object').columns
    for col_name in obj_col_list:
        scrubf, scrubb = smart_scrub(df,col_name,1-error_rate)
        if scrubf is not None or scrubb is not None:
            print("Scrubbed '{}' from the front and '{}' from the back of column '{}'" \
                  .format(scrubf,scrubb,col_name))
    
    # Coerice columns if possible
    for col_name in obj_col_list:
        new_dtype = coerce_col(df,col_name,error_rate)
        if new_dtype is not None:
            print("Coerced '{}' to datatype '{}'".format(col_name, new_dtype))  
    return df
    # TODO For future implementation

def coerce_col(df,col_name,error_rate):
    pass