# -*- coding: utf-8 -*-
import pandas as _pd
import mr_clean._utils.data_handling as _dutils
import mr_clean._utils.globals as _globals
from collections import deque

#None of these functions should have much logic.


# --------- Blind ops on entire table ---------------------

def colname_gen(df,col_name = 'unnamed_col'):
        if col_name not in df.keys():
            yield col_name
        id_number = 0
        while True:
            col_name = col_name + str(id_number)
            if col_name in df.keys():
                id_number+=1
            else:
                return col_name

# --------- Blind ops on entire table (destructive) ----------------

def clean_colnames(df):
    col_list = []
    for index in range(_dutils.cols(df)):
        col_list.append(df.columns[index].strip().lower().replace(' ','_'))
    df.columns = col_list

def reindex(df):
    df.reset_index()

# ----- Blind ops on single columns-------------

def col_strip(df,col_name,dest = False):
    if dest:
        df[col_name] = df[col_name].str.strip()
    else:
        return df[col_name].str.strip()

def col_scrubf(df,col_name,which,count = 1,dest = False):
    if dest:
        df.loc[which,col_name] = df.loc[which,col_name].str[count:]
    else:
        new_col = df[col_name].copy()
        new_col[which] = df.loc[which,col_name].str[count:]
        return new_col

def col_scrubb(df,col_name,which, count = 1,dest = False):
    if dest:
        df.loc[which,col_name] = df.loc[which,col_name].str[:-count]
    else:
        new_col = df[col_name].copy()
        new_col[which] = df.loc[which,col_name].str[:-count]
        return new_col

def col_to_numeric(df,col_name, dest = False):
    new_col = _pd.to_numeric(df[col_name], errors = 'coerce')
    if dest:
        set_col(df,col_name,new_col)
    else:
        return new_col

def col_to_dt(df,col_name,set_format = None,infer_format = True, dest = False):
    new_col = _pd.to_datetime(df[col_name],errors = 'coerce',
                                    format = set_format,infer_datetime_format = infer_format)
    if dest:
        set_col(df,col_name,new_col)
    else:
        return new_col

def col_to_cat(df,col_name, dest = False):
    new_col = df[col_name].astype('category')
    if dest:
        set_col(df,col_name,new_col)
    else:
        return new_col

# ------- Blind ops on single columns (destructive) ------

def set_col(df,col_name, new_values):
    df[col_name] = new_values

def col_rename(df,col_name,new_col_name):
    col_list = list(df.columns)
    for index,value in enumerate(col_list):
        if value == col_name:
            col_list[index] = new_col_name
            break
    df.columns = col_list

def col_mod(df,col_name,func,*args,**kwargs):
    backup = df[col_name].copy()
    try:
        return_val = func(df,col_name,*args,**kwargs)
        if return_val is not None:
            set_col(df,col_name,return_val)
    except:
        df[col_name] = backup

# ------- Blind operations on multiple columns ----------

def cols_strip(df,col_list, dest = False):
    if not dest:
        return [col_strip(df,col_name) for col_name in col_list]
    for col_name in col_list:
        col_strip(df,col_name,dest)

def cols_to_numeric(df, col_list,dest = False):
    if not dest:
        return [col_to_numeric(df,col_name) for col_name in col_list]
    for col_name in col_list:
        col_to_numeric(df,col_name,dest)

def cols_to_dt(df, col_list,set_format = None,infer_format = True,dest = False):
    if not dest:
        return [col_to_dt(df,col_name,set_format,infer_format) for col_name in col_list]
    for col_name in col_list:
        col_to_dt(df,col_name,set_format,infer_format,dest)

def cols_to_cat(df, col_list,dest = False):
    # Convert a list of columns to categorical
    if not dest:
        return [col_to_cat(df,col_name) for col_name in col_list]
    for col_name in col_list:
        col_to_cat(df,col_name,dest)

def cols_(df,col_list,func,*args,**kwargs):
    #Do a function over a list of columns and return the result
    return [func(df,col_name,*args,**kwargs) for col_name in col_list]

# ------- Blind operations on multiple columns (destructive) ----------

def cols_rename(df,col_names = [], new_col_names = []):
    assert len(col_names) == len(new_col_names)
    for old_name,new_name in zip(col_names,new_col_names):
        col_rename(df,old_name,new_name)

# ------- Get formatting information ----------

def col_dtypes(df): # Does some work to reduce possibility of errors and stuff
    """
    Pandas datatypes are as follows:
    object,number,datetime,category,timedelta,datetimetz
    This method uses queues and iterates over the columns in linear time.
    It does extra steps to ensure that no further work with numpy datatypes needs
    to be done.
    """
    test_list = [col_isobj,col_isnum,col_isdt,col_iscat,col_istdelt,col_isdtz]
    deque_list = [(deque(col_method(df)),name) \
                  for col_method,name in zip(test_list,_globals.__dtype_names) if len(col_method(df))]
    type_dict = {}
    for col_name in df.columns:
        for que,name in deque_list:
            if len(que):
                if que[0] == col_name:
                    que.popleft()
                    type_dict[col_name] = name
                    break
    return type_dict

def col_isobj(df, col_name = None):
    col_list = df.select_dtypes(include = ['object']).columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_isnum(df,col_name = None):
    col_list = df.select_dtypes(include = ['number']).columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_isdt(df,col_name = None):
    col_list = df.select_dtypes(include = ['datetime']).columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_iscat(df,col_name = None):
    col_list = df.select_dtypes(include = ['category']).columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_istdelt(df,col_name = None):
    col_list = df.select_dtypes(include = ['timedelta']).columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_isdtz(df,col_name = None):
    col_list = df.select_dtypes(include = ['datetimetz']).columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list
