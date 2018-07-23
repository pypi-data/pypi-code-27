# -*- coding: utf-8 -*-
import pandas as pd
import mr_clean._utils.io as _io
import os
import mr_clean._utils.data_handling as _utils
import mr_clean.core.stats.summary as stats
import mr_clean.core.stats.regression as regstats
# Pre-cleaning

# This method takes in a DataFrame object, as well as a few parameters,
# and outputs a DataFrame that summarizes some of the possible problems
# that might have to be addressed in cleaning
def summarize(df,preview_rows = 8,
            display_max_cols = None,display_width = None,
            output_path = None, output_safe = True,to_folder = False): 
    """ Prints information about the DataFrame to a file or to the prompt.

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
    output_path - path-like, default None
        If not None, this will be used as the path of the output file, and this
        function will print to a file instead of to the prompt
    output_safe - boolean, default True
        If True and output_file is not None, this function will not overwrite any
        existing files.
    output_csv: boolean, default False
        If True, will output to a directory with name of output_path with all data in 
        csv format. WARNING: If set to true, this function will overwrite existing files
        in the directory with the following names: 
            ['Preview.csv','Describe.csv','Info.csv','Percentile Details.csv',
             'Missing Values Summary.csv','Potential Outliers.csv','Correlation Matrix.csv']
    """
    assert type(df) is pd.DataFrame
    
    # Reformat displays
    initial_settings = pd_settings(display_max_cols, None, display_width)

    # --------Values of data-----------
    df_preview = _io.preview(df,preview_rows)
    df_desc_num, df_desc_cat = detailed_desc(df)
    percent_values = stats.percentiles(df)
    potential_outliers = stats.df_outliers(df).dropna(axis = 1,how = 'all')
    potential_outliers = potential_outliers if _utils.rows(potential_outliers) else None
    corr_values = regstats.corr_matrix(df)

    # ----------Build lists------------
    
    title_list = \
    ['Preview','Describe (Numerical)','Describe (Categorical)','Percentile Details',
     'Potential Outliers','Correlation Matrix']
    info_list = \
    [df_preview,df_desc_num, df_desc_cat,percent_values,
     potential_outliers,corr_values]
    error_list = [None,'No numerical data.','All numerical data.','No numerical data.',
                  'No potential outliers.','No categorical, bool, or numerical data.']
    
    # ----------Build output------------
    
    output = ''
    for title, value,error_text in zip(title_list,info_list,error_list):
        if value is None:
            value = "{} skipped: {}".format(title,error_text)
        if str(value).endswith('\n'):
            value = value[:-1]
        output+='{}\n{}\n\n'.format(_io.title_line(title),value)

    # ----------Send to file/print to console------------
    if output_path is None: 
        # Potentially could change this to allow for output_safe to work with directories
         print(output)
    else:
        if not to_folder:
            print('Outputting to file...')
            _io.output_to_file(output,output_path,output_safe)
        else:
            print('Outputting to folder...')
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            for title, value,error_text in zip(title_list,info_list,error_list):
                if value is None:
                    print("{} skipped: {}".format(title,error_text))
                else:
                    file_dir = os.path.join(output_path,"{}.csv".format(title))
                    if type(value) is pd.DataFrame:
                        # Eventually add a check to see if file exists
                        value.to_csv(file_dir)
                    else:
                        _io.output_to_file(value,file_dir,False) 
                        # Change to output_safe when directory output_safe is implemented
        print('Done!')

    # Reset display settings
    pd_settings(*initial_settings)


def pd_settings(max_cols,max_rows,disp_width):
    # Set pandas display settings and retrieve old settings
    initial_max_cols = pd.get_option('display.max_columns')
    initial_max_rows = pd.get_option('display.max_rows')
    initial_width = pd.get_option('display.width')
    
    pd.set_option('display.max_columns', max_cols)
    pd.set_option('display.max_rows', max_rows)
    if disp_width is not None:
        pd.set_option('display.width', disp_width)
    return (initial_max_cols,initial_max_rows,initial_width)

def detailed_desc(df):# Get information from df.describe past
    # The pandas implementation
    try:
        df_desc_num = df.describe(include = 'number').transpose()
    except ValueError:
        df_desc_num = None

    try:
        df_desc_cat = df.describe(exclude = 'number').transpose()
    except ValueError:
        df_desc_cat = None
    return (df_desc_num,df_desc_cat)