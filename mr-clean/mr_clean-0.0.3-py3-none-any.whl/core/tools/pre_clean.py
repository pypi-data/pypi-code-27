# -*- coding: utf-8 -*-
import pandas as _pd
import mr_clean._utils.io as _io
#import preview,get_info,output_to_file,title_line,format_row
import mr_clean._utils.data_handling as _utils
import mr_clean.core.stats.summary_stats as stats
# Pre-cleaning

# This method takes in a DataFrame object, as well as a few parameters,
# and outputs a DataFrame that summarizes some of the possible problems
# that might have to be addressed in cleaning
def summarize(df,preview_rows = 5,preview_max_cols = 0,
            memory_usage = 'deep',display_width = None,
            output_file = None, output_safe = True):
    """ Prints information about the DataFrame to a file or to the prompt.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to summarize
    preview_rows : int, default 5
        Amount of rows to preview from the head and tail of the DataFrame
    preview_max_cols : int, default 0
        Maximum amount of columns to preview. Set to None to preview all
        columns, and set to 0 to preview as many as fit in the screen's width
    memory_usage : boolean or 'deep', default 'deep'
        Type of output that the 'memory usage' section of the .info() call should have
    display_width : int, default None
        Width of output. Can be width of file or width of console for printing.
        Set to None for pandas to detect it from console.
    output_file : path-like, default None
        If not None, this will be used as the path of the output file, and this
        function will print to a file instead of to the prompt
    output_safe : boolean, default True
        If True and output_file is not None, this function will not overwrite any
        existing files.
    """
    assert type(df) is _pd.DataFrame

    # --------Values of data-----------
    df_preview = _io.preview(df,preview_rows = 5,preview_max_cols = 0)
    info = _io.get_info(df,verbose = True, max_cols = None,memory_usage = memory_usage,null_counts = True)
    percent_values = stats.percentiles(df)
    dtypes = stats.dtypes_summary(df).apply(_io.format_row,args = [_utils.rows(df)],axis = 1)
    dtypes.columns = df.columns
    potential_outliers = stats.df_outliers(df) # TODO add support for formatting this dataframe

    # ----------Build lists------------
    title_list = ['Preview','Describe','Info']
    info_list = [df_preview,df.describe().transpose(),info]
    if percent_values is not None:
        title_list.append('Percentile Details')
        info_list.append(percent_values)
    else:
        print('Percentiles skipped: No numeric data')
    title_list+=['Missing Values Summary','Potential Outliers']
    info_list+=[dtypes,potential_outliers]
    output = zip(title_list,info_list)

    # -------Print or output-----------

    # Get initial display settings
    initial_max_cols = _pd.get_option('display.max_columns')
    initial_max_rows = _pd.get_option('display.max_rows')
    initial_width = _pd.get_option('display.width')

    # Reformat displays
    _pd.set_option('display.max_columns', None)
    _pd.set_option('display.max_rows',None)
    if display_width is not None:
            _pd.set_option('display.width',display_width)

    #Output information to print line or file
    if output_file is None:
         for title, value in output:
            print(_io.title_line(title))
            print(value)
    else:
        print('Outputting to file...')
        _io.output_to_file(df,output_file,output_safe)
    # Reset display settings
    _pd.set_option('display.max_columns', initial_max_cols)
    _pd.set_option('display.max_columns', initial_max_rows)
    _pd.set_option('display.max_columns', initial_width)
