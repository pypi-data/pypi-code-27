from codegenhelper import debug
import os
from code_engine import publish

def get_template_path():
    return os.path.join(os.path.split(__file__)[0], "..", "templates")

def gen(data, output_path):
    publish(debug(get_template_path(), "gen:template_path"), \
            "app", \
            data,
            debug(output_path, 'gen:output_path')
            )
    
