# -*- coding: utf-8 -*-
import mr_clean._utils.data_handling as _utils
import mr_clean.core.functions.basics as _basics

def smart_scrub(df,col_name,cutoff = 1):
    """ Scrubs from the front and back of an 'object' column in a DataFrame
    until the scrub would semantically alter the contents of the column. If only a 
    subset of the elements in the column are scrubbed, then a boolean array indicating which
    elements have been scrubbed is appended to the dataframe. Returns a tuple of the strings removed
    from the front and back of the elements
    df - DataFrame
        DataFrame to scrub
    col_name - string
        Name of column to scrub
    cutoff - number, default 1
        The cutoff that determines when to stop scrubbing. Should be a number between 0 and 1,
        where 0 means that the entire column is scrubbed, and 1 means that only elements that are similar accross
        all elements are scrubbed.
    """
    scrubf = smart_scrubf(df,col_name,cutoff)
    scrubb = smart_scrubb(df,col_name,cutoff)
    return (scrubf, scrubb)

def smart_scrubf(df,col_name,cutoff = 1):
    """ Scrubs from the front of an 'object' column in a DataFrame
    until the scrub would semantically alter the contents of the column. If only a 
    subset of the elements in the column are scrubbed, then a boolean array indicating which
    elements have been scrubbed is appended to the dataframe. Returns the string that was scrubbed
    df - DataFrame
        DataFrame to scrub
    col_name - string
        Name of column to scrub
    cutoff - number, default 1
        The cutoff that determines when to stop scrubbing. Should be a number between 0 and 1,
        where 0 means that the entire column is scrubbed, and 1 means that only elements that are similar accross
        all elements are scrubbed.
    """
    scrubbed = ""
    while True:
        valcounts = df[col_name].str[:len(scrubbed)+1].value_counts()
        if not len(valcounts):
            break
        if not valcounts[0] >= cutoff * _utils.rows(df):
            break
        scrubbed=valcounts.index[0]
    if scrubbed == '':
        return None
    which = df[col_name].str.startswith(scrubbed)
    _basics.col_scrubf(df,col_name,which,len(scrubbed),True)
    if not which.all():
        new_col_name = _basics.colname_gen(df,"{}_sf-{}".format(col_name,scrubbed))
        df[new_col_name] = which
    return scrubbed

def smart_scrubb(df,col_name,cutoff = 1):
    """ Scrubs from the back of an 'object' column in a DataFrame
    until the scrub would semantically alter the contents of the column. If only a 
    subset of the elements in the column are scrubbed, then a boolean array indicating which
    elements have been scrubbed is appended to the dataframe. Returns the string that was scrubbed.
    df - DataFrame
        DataFrame to scrub
    col_name - string
        Name of column to scrub
    cutoff - number, default 1
        The cutoff that determines when to stop scrubbing. Should be a number between 0 and 1,
        where 0 means that the entire column is scrubbed, and 1 means that only elements that are similar accross
        all elements are scrubbed.
    """
    scrubbed = ""
    while True:
        valcounts = df[col_name].str[-len(scrubbed)-1:].value_counts()
        if not len(valcounts):
            break
        if not valcounts[0] >= cutoff * _utils.rows(df):
            break
        scrubbed=valcounts.index[0]
    if scrubbed == '':
        return None
    which = df[col_name].str.endswith(scrubbed)
    _basics.col_scrubb(df,col_name,which,len(scrubbed),True)
    if not which.all():
        new_col_name = _basics.colname_gen(df,"{}_sb-{}".format(col_name,scrubbed))
        df[new_col_name] = which
    return scrubbed

def smart_coerce():
    """
    """
    pass
