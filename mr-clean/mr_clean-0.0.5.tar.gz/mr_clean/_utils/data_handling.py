# -*- coding: utf-8 -*-
import numpy as np

def row_req(df,cutoff):
    return rows(df) * cutoff

def rows(df):
    return df.shape[0]

def cols(df):
    return df.shape[1]

#def is_num(series): #TODO improve this method
#    if (series.dtype == np.object):
#        return False
#    return True

def get_cutoff(column, cutoff):
    __value_or_container(column,cutoff,1)   

def bc_vec(df,value = True): # Boolean column vector
    return np.ones(rows(df),dtype=bool) if value else np.zeros(rows(df),dtype=bool)

def ic_vec(df,value = 0): # Boolean column vector
    if value == 0:
        return np.zeros(rows(df),dtype=np.int32)
    elif value == 1:
        return np.ones(rows(df),dtype=np.int32)
    else:
        return np.ones(rows(df),dtype=np.int32) * value

def __value_or_container(key,item,default):
    if type(item) is dict:
        return item[key] if key in item else default
    return item

def memory(df, col = None,index = None,deep = True):
    if col is None:
        index = True if index is None else index
        return df.memory_usage(index,deep)
    else:
        index = False if index is None else index
        return df[col].memory_usage(index,deep)