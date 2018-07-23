# -*- coding: utf-8 -*-
import pandas as pd
import mr_clean._utils.io as _io
import mr_clean._utils.data_handling as _utils
import mr_clean.core.stats.summary as stats

def diagnose(df,preview_rows = 2,
            display_max_cols = 0,display_width = None): 
    """ Prints information about the DataFrame pertinent to data cleaning.

    Parameters
    ----------
    df - DataFrame
        The DataFrame to summarize
    preview_rows - int, default 5
        Amount of rows to preview from the head and tail of the DataFrame
    display_max_cols - int, default None
        Maximum amount of columns to display. If set to None, all columns will be displayed.
        If set to 0, only as many as fit in the screen's width will be displayed
    display_width - int, default None
        Width of output. Can be width of file or width of console for printing.
        Set to None for pandas to detect it from console.
    """
    assert type(df) is pd.DataFrame
    # Diagnose problems with the data formats that can be addressed in cleaning
    
     # Get initial display settings
    initial_max_cols = pd.get_option('display.max_columns')
    initial_max_rows = pd.get_option('display.max_rows')
    initial_width = pd.get_option('display.width')

    # Reformat displays
    pd.set_option('display.max_columns', display_max_cols)
    pd.set_option('display.max_rows',None)
    if display_width is not None:
            pd.set_option('display.width',display_width)

    # --------Values of data-----------
    df_preview = _io.preview(df,preview_rows)
    
    df_info = _io.get_info(df,verbose = True, max_cols = display_max_cols, 
                               memory_usage = 'deep',null_counts = True)
    
    dtypes = stats.dtypes_summary(df).apply(_io.format_row,args = [_utils.rows(df)],axis = 1)
    
    potential_outliers = stats.df_outliers(df).dropna(axis = 1,how = 'all')
    potential_outliers = potential_outliers if _utils.rows(potential_outliers) \
                    else None

    # ----------Build lists------------
    
    title_list = \
    ['Preview','Info',
     'Data Types Summary','Potential Outliers']
    info_list = \
    [df_preview,df_info,
     dtypes,potential_outliers]
    error_list = [None,None,
                  None,'No potential outliers.']
    
    # ----------Build output------------
    
    output = ''
    for title, value,error_text in zip(title_list,info_list,error_list):
        if value is None:
            value = "{} skipped: {}".format(title,error_text)
        if str(value).endswith('\n'):
            value = value[:-1]
        output+='{}\n{}\n\n'.format(_io.title_line(title),value)

    # ----------Send to file/print to console------------
        # Potentially could change this to allow for output_safe to work with directories
    print(output)

    # Reset display settings
    pd.set_option('display.max_columns', initial_max_cols)
    pd.set_option('display.max_rows', initial_max_rows)
    pd.set_option('display.width', initial_width)    
    
    