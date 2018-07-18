# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import io
import shutil

# --------- Memory Information ---------------------

# Simple statement of memory usage
def memory_statement(savings,task_name,statement):
    return  statement \
              .format( convert_memory(savings) ,task_name )

# Convert memeory to a readable form
def convert_memory(memory_value):
    unit_list = ['KB','MB','GB','TB']
    index = 0
    memory = memory_value / 1024
    while memory > 1000 and index < 3:
        memory/=1024
        index+=1
    return '{} {}'.format(round( memory, 1),unit_list[index])

# --------- Formatting outputs ---------------------

def preview(df,preview_rows = 5):#,preview_max_cols = 0):
    """ Returns a preview of a dataframe, which contains both header
    rows and tail rows.
    """
    assert type(df) is pd.DataFrame
    if preview_rows <= 0:
        preview_rows = 1
    return df.iloc[np.r_[0:preview_rows,-preview_rows:0]]
#    initial_max_cols = pd.get_option('display.max_columns')
#    pd.set_option('display.max_columns', preview_max_cols)
#    data = str(df.iloc[np.r_[0:preview_rows,-preview_rows:0]])
#    pd.set_option('display.max_columns', initial_max_cols)
#    return data

def get_info(df, verbose = None,max_cols = None, memory_usage = None, null_counts = None):
    """ Returns the .info() output of a dataframe
    """
    assert type(df) is pd.DataFrame
    buffer = io.StringIO()
    df.info(verbose, buffer, max_cols, memory_usage, null_counts)
    return buffer.getvalue()

def title_line(text):
    """Returns a string that represents the
    text as a title blurb
    """
    columns = shutil.get_terminal_size()[0]
    start = columns // 2 - len(text) // 2
    output = '='*columns + '\n\n' + \
            ' ' * start + str(text) + "\n\n" + \
            '='*columns + '\n'
    return output

#------------ Outputting --------------------

# Outputs to a file. If and only if ouput_safe is false, it will overwrite existing files
def output_to_file(data,output_file,output_safe):
    try:
        with open(output_file,'x' if output_safe else 'w') as file:
                file.write(data)
    except FileExistsError:
        print("Nothing outputted: file '{}' already exists".format(output_file))

def format_row(row, total_rows):
    output = []
    for item in row:
        output.append( "{} ({}%)".format(item, round(item/total_rows*100,2)) )
    return pd.Series(output)
