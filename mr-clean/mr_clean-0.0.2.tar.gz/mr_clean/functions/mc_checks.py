# -*- coding: utf-8 -*-
from mr_clean._utils.data_handling import rows
from mr_clean.functions.basics import colname_gen, col_scrubf,col_scrubb

def smart_scrub(df,col_name,cutoff = 1):
    scrubf = smart_scrubf(df,col_name,cutoff)
    scrubb = smart_scrubb(df,col_name,cutoff)
    return (scrubf, scrubb)

def smart_scrubf(df,col_name,cutoff = 1):
    scrubbed = ""
    while True:
        valcounts = df[col_name].str[:len(scrubbed)+1].value_counts()
        if not len(valcounts):
            break
        if not valcounts[0] >= cutoff * rows(df):
            break
        scrubbed=valcounts.index[0]
    if scrubbed == '':
        return None
    which = df[col_name].str.startswith(scrubbed)
    col_scrubf(df,col_name,which,len(scrubbed),True)
    if not which.all():
        new_col_name = colname_gen(df,"{}_sf-{}".format(col_name,scrubbed))
        df[new_col_name] = which
    return scrubbed

def smart_scrubb(df,col_name,cutoff = 1):
    scrubbed = ""
    while True:
        valcounts = df[col_name].str[-len(scrubbed)-1:].value_counts()
        if not len(valcounts):
            break
        if not valcounts[0] >= cutoff * rows(df):
            break
        scrubbed=valcounts.index[0]
    if scrubbed == '':
        return None
    which = df[col_name].str.endswith(scrubbed)
    col_scrubb(df,col_name,which,len(scrubbed),True)
    if not which.all():
        new_col_name = colname_gen(df,"{}_sb-{}".format(col_name,scrubbed))
        df[new_col_name] = which
    return scrubbed

def smart_coerce():
    pass
