# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from mr_clean_func_utils import coerce,get_colname_gen,get_cutoff,ic_vec,is_num,row_req,rows


   

def remove_whitespace(df): # removes whitespace from string columns
    for column in (column for column in df if not is_num( df[column] )  ):
        pass

def rename_index(df):
    if not (type(df.index) is pd.RangeIndex or type(df.index) is pd.DatetimeIndex):
         # reset the index
        return True

#%%
def coerce_col(df, column,
               numeric_cutoff, coerce_numeric, 
               dt_cutoff, coerce_dt, dt_format,
               categorical_cutoff,coerce_categorical):
    success = True
    if column in coerce_numeric:
            pass
    elif column in coerce_dt:
        if dt_format is None:
            coerce(df, column, 
                    pd.to_datetime(df[column],errors = 'coerce',infer_datetime_format = True))
        else:
            coerce(df, column, 
                    pd.to_datetime(df[column],errors = 'coerce',format = dt_format))
    elif column in coerce_categorical:
        coerce(df, column, df[column].astype('category'))
    else:
        success = __infer_coerce(df, column,
               get_cutoff( column,numeric_cutoff ),
               get_cutoff( column,dt_cutoff ),
               get_cutoff( column,categorical_cutoff ) )
    return success

def __infer_coerce(df, column,
               numeric_cutoff,dt_cutoff,categorical_cutoff):
    
    cat_coerced = df[column].astype('category')
    num_coerced = pd.to_numeric(df[column], errors = 'coerce')
    dt_coerced = pd.to_datetime(df[column],errors = 'coerce',infer_datetime_format = True)
    
    all_cutoffs = [categorical_cutoff,numeric_cutoff,dt_cutoff]
    all_coerced = [cat_coerced,num_coerced,dt_coerced]
    all_counts = [coerced.count() for coerced in all_coerced]
    all_counts[0] = rows(df)-len(all_coerced[0].value_counts())
    all_scores = [count-row_req(df,cutoff) for count,cutoff in zip(all_counts,all_cutoffs)]
    high_score = max(*all_scores)
    for index in range(3):
        if all_scores[index] == high_score and \
            all_scores[index] >= 0:
            coerce(df, column, all_coerced[index])
            return True
    return False







