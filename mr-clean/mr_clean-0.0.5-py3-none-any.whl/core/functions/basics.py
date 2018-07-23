# -*- coding: utf-8 -*-
import pandas as _pd
import mr_clean._utils.data_handling as _dutils
import mr_clean._utils.globals as _globals
from collections import deque

#None of these functions should have much logic.


# --------- Blind ops on entire table ---------------------

def colname_gen(df,col_name = 'unnamed_col'):
    """ Returns a column name that isn't in the specified DataFrame
    Parameters:
    df - DataFrame
        DataFrame to analyze
    col_name - string, default 'unnamed_col'
        Column name to use as the base value for the generated column name
    """
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
    """ Cleans the column names on a DataFrame
    Parameters:
    df - DataFrame
        The DataFrame to clean
    """
    col_list = []
    for index in range(_dutils.cols(df)):
        col_list.append(df.columns[index].strip().lower().replace(' ','_'))
    df.columns = col_list

# ----- Blind ops on single columns-------------

def col_strip(df,col_name,dest = False):
    """ Performs str.strip() a column of a DataFrame
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to strip
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    if dest:
        df[col_name] = df[col_name].str.strip()
    else:
        return df[col_name].str.strip()

def col_scrubf(df,col_name,which,count = 1,dest = False):
    """ Removes characters from the front of the entries in DataFrame for a column
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to scrub
    which - boolean array
        Boolean array that determines which elements to scrub, where True means scrub
    count - integer, default 1
        amount of characters to scrub
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    if dest:
        df.loc[which,col_name] = df.loc[which,col_name].str[count:]
    else:
        new_col = df[col_name].copy()
        new_col[which] = df.loc[which,col_name].str[count:]
        return new_col

def col_scrubb(df,col_name,which, count = 1,dest = False):
    """ Removes characters from the back of the entries in DataFrame for a column
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to scrub
    which - boolean array
        Boolean array that determines which elements to scrub, where True means scrub
    count - integer, default 1
        amount of characters to scrub
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    if dest:
        df.loc[which,col_name] = df.loc[which,col_name].str[:-count]
    else:
        new_col = df[col_name].copy()
        new_col[which] = df.loc[which,col_name].str[:-count]
        return new_col

def col_to_numeric(df,col_name, dest = False):
    """ Coerces a column in a DataFrame to numeric
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to coerce
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    new_col = _pd.to_numeric(df[col_name], errors = 'coerce')
    if dest:
        set_col(df,col_name,new_col)
    else:
        return new_col

def col_to_dt(df,col_name,set_format = None,infer_format = True, dest = False):
    """ Coerces a column in a DataFrame to datetime
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to coerce
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    new_col = _pd.to_datetime(df[col_name],errors = 'coerce',
                                    format = set_format,infer_datetime_format = infer_format)
    if dest:
        set_col(df,col_name,new_col)
    else:
        return new_col

def col_to_cat(df,col_name, dest = False):
    """ Coerces a column in a DataFrame to categorical
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to coerce
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    new_col = df[col_name].astype('category')
    if dest:
        set_col(df,col_name,new_col)
    else:
        return new_col

# ------- Blind ops on single columns (destructive) ------

def set_col(df,col_name, new_values):
    """ Sets a column in a DataFrame
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to set
    new_values - Series
        The new values for that column
    """
    df[col_name] = new_values

def col_rename(df,col_name,new_col_name):
    """ Changes a column name in a DataFrame
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to change
    new_col_name - string
        New name of column
    """
    col_list = list(df.columns)
    for index,value in enumerate(col_list):
        if value == col_name:
            col_list[index] = new_col_name
            break
    df.columns = col_list

def col_mod(df,col_name,func,*args,**kwargs):
    """ Changes a column of a DataFrame according to a given function
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_name - string
        Name of column to modify
    func - function
        The function to use to modify the column
    """
    backup = df[col_name].copy()
    try:
        return_val = func(df,col_name,*args,**kwargs)
        if return_val is not None:
            set_col(df,col_name,return_val)
    except:
        df[col_name] = backup

# ------- Blind operations on multiple columns ----------

def cols_strip(df,col_list, dest = False):
    """ Performs str.strip() a column of a DataFrame
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_list - list of strings
        names of columns to strip
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    if not dest:
        return _pd.DataFrame({col_name:col_strip(df,col_name) for col_name in col_list})
    for col_name in col_list:
        col_strip(df,col_name,dest)

def cols_to_numeric(df, col_list,dest = False):
    """ Coerces a list of columns to numeric
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_list - list of strings
        names of columns to coerce
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    if not dest:
        return _pd.DataFrame({col_name:col_to_numeric(df,col_name) for col_name in col_list})
    for col_name in col_list:
        col_to_numeric(df,col_name,dest)

def cols_to_dt(df, col_list,set_format = None,infer_format = True,dest = False):
    """ Coerces a list of columns to datetime
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_list - list of strings
        names of columns to coerce
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    if not dest:
        return _pd.DataFrame({col_name:col_to_dt(df,col_name,set_format,infer_format) for col_name in col_list})
    for col_name in col_list:
        col_to_dt(df,col_name,set_format,infer_format,dest)

def cols_to_cat(df, col_list,dest = False):
    """ Coerces a list of columns to categorical
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_list - list of strings
        names of columns to coerce
    dest - bool, default False
        Whether to apply the result to the DataFrame or return it.
        True is apply, False is return.
    """
    # Convert a list of columns to categorical
    if not dest:
        return _pd.DataFrame({col_name:col_to_cat(df,col_name) for col_name in col_list})
    for col_name in col_list:
        col_to_cat(df,col_name,dest)

def cols_(df,col_list,func,*args,**kwargs):
    """ Do a function over a list of columns and return the result
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_list - list of strings
        names of columns to coerce
    func - function
        function to use
    """
    return _pd.DataFrame({col_name:func(df,col_name,*args,**kwargs) for col_name in col_list})

# ------- Blind operations on multiple columns (destructive) ----------

def cols_rename(df,col_names, new_col_names):
    """ Rename a set of columns in a DataFrame
    Parameters:
    df - DataFrame
        DataFrame to operate on
    col_names - list of strings
        names of columns to change
    new_col_names - list of strings
        new names for old columns (order should be same as col_names)
    """
    assert len(col_names) == len(new_col_names)
    for old_name,new_name in zip(col_names,new_col_names):
        col_rename(df,old_name,new_name)

# ------- Get formatting information ----------

def col_dtypes(df): # Does some work to reduce possibility of errors and stuff
    """ Returns dictionary of datatypes in a DataFrame (uses string representation)
    Parameters:
    df - DataFrame
        The DataFrame to return the object types of
    
    Pandas datatypes are as follows:
    object,number,bool,datetime,category,timedelta,datetimetz
    This method uses queues and iterates over the columns in linear time.
    It does extra steps to ensure that no further work with numpy datatypes needs
    to be done.
    """
    test_list = [col_isobj,col_isnum,col_isbool,col_isdt,col_iscat,col_istdelt,col_isdtz]
    deque_list = [(deque(col_method(df)),name) \
                  for col_method,name in zip(test_list,_globals.__dtype_names) if len(col_method(df))]
    type_dict = {}
    for que, name in deque_list:
        while len(que):
            type_dict[que.popleft()] = name
    return type_dict

def col_isobj(df, col_name = None):
    """ Returns a list of columns that are of type object. If col_name is specified, returns 
    whether the column in the DataFrame is of type 'object' instead.
    Parameters:
    df - DataFrame
        DataFrame to check
    col_name - string, default None
        If specified, this function will True if df[col_name] is of type 'object'
    """
    col_list = df.select_dtypes(include = 'object').columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_isnum(df,col_name = None):
    """ Returns a list of columns that are of type 'number'. If col_name is specified, returns 
    whether the column in the DataFrame is of type 'number' instead.
    Parameters:
    df - DataFrame
        DataFrame to check
    col_name - string, default None
        If specified, this function will True if df[col_name] is of type 'number'
    """
    col_list = df.select_dtypes(include = 'number').columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_isbool(df,col_name = None):
    """ Returns a list of columns that are of type 'bool'. If col_name is specified, returns 
    whether the column in the DataFrame is of type 'bool' instead.
    Parameters:
    df - DataFrame
        DataFrame to check
    col_name - string, default None
        If specified, this function will True if df[col_name] is of type 'bool'
    """
    col_list = df.select_dtypes(include = 'bool').columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_isdt(df,col_name = None):
    """ Returns a list of columns that are of type 'datetime'. If col_name is specified, returns 
    whether the column in the DataFrame is of type 'datetime' instead.
    Parameters:
    df - DataFrame
        DataFrame to check
    col_name - string, default None
        If specified, this function will True if df[col_name] is of type 'datetime'
    """
    col_list = df.select_dtypes(include = 'datetime').columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_iscat(df,col_name = None):
    """ Returns a list of columns that are of type 'category'. If col_name is specified, returns 
    whether the column in the DataFrame is of type 'category' instead.
    Parameters:
    df - DataFrame
        DataFrame to check
    col_name - string, default None
        If specified, this function will True if df[col_name] is of type 'category'
    """
    col_list = df.select_dtypes(include = 'category').columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_istdelt(df,col_name = None):
    """ Returns a list of columns that are of type 'timedelta'. If col_name is specified, returns 
    whether the column in the DataFrame is of type 'timedelta' instead.
    Parameters:
    df - DataFrame
        DataFrame to check
    col_name - string, default None
        If specified, this function will True if df[col_name] is of type 'timedelta'
    """
    col_list = df.select_dtypes(include = 'timedelta').columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list

def col_isdtz(df,col_name = None):
    """ Returns a list of columns that are of type 'datetimetz'. If col_name is specified, returns 
    whether the column in the DataFrame is of type 'datetimetz' instead.
    Parameters:
    df - DataFrame
        DataFrame to check
    col_name - string, default None
        If specified, this function will True if df[col_name] is of type 'datetimetz'
    """
    col_list = df.select_dtypes(include = 'datetimetz').columns
    if col_name is None:
        return col_list
    else:
        return col_name in col_list
