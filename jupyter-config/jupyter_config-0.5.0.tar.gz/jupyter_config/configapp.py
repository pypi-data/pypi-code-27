import glob
import os
import sys
import re 
import itertools

from jupyter_core.application import JupyterApp, base_aliases, base_flags
from notebook.nbextensions import NBCONFIG_SECTIONS
import jupyter_core.paths as jpaths
from traitlets.config import catch_config_error

config_aliases = {}
config_aliases.update(base_aliases)

config_flags = {}
config_flags.update(base_flags)

class JupyterConfigApp(JupyterApp):
    name = "jupyter-config"
    description = "A Jupyter Application for searching in and finding config files."
    # aliases = config_aliases
    # flags = config_flags
    
    
    # subcommands = dict(
    #     list=(JupyterConfigListApp, JupyterConfigListApp.description.splitlines()[0]),
    #     search=(JupyterConfigSearchApp, JupyterConfigSearchApp.description.splitlines()[0]),
    # )
    
    @catch_config_error
    def initialize(self, argv=None):
        super(JupyterConfigApp, self).initialize(argv)
        search_jupyter_paths(self.extra_args)
        

def generate_potential_paths():
    """Generate all of the potential paths available in the current context.
    
    
    """
    base_conf_paths = list(filter(os.path.isdir, jpaths.jupyter_config_path()))
        
    nbconfig_base_paths = list(filter(os.path.isdir, (os.path.join(d, 'nbconfig') 
                                                      for d in base_conf_paths)))
    conf_d_paths = list(filter(os.path.isdir, (os.path.join(d, 'jupyter_notebook_config.d') 
                                                            for d in base_conf_paths)))
    for d in nbconfig_base_paths:
        config_path_segment = list(filter(os.path.isdir, (os.path.join(d, section+'.d') 
                                                          for section in NBCONFIG_SECTIONS)))
        conf_d_paths.extend(config_path_segment)
    
    
    return {'base_conf_paths': base_conf_paths,
            'nbconfig_base_paths': nbconfig_base_paths,
            'conf_d_paths': conf_d_paths,
            }
    
def valid_conf_file(file_name):
# replace with canonical config validation checker
    return (os.path.isfile(file_name) 
            and os.path.splitext(file_name)[1] in ['.py', '.json'])
    

canonical_names_regex = re.compile(r"jupyter_(\w*_|)config")

def valid_local_conf_file(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    return (valid_conf_file(file_path) 
            and canonical_names_regex.match(file_name))
    
def valid_gen_conf_file(file_path, name_regex):
    file_name = os.path.basename(file_path)
    return (valid_conf_file(file_path) 
            and name_regex.match(file_name))
        
def search_jupyter_paths(search_term=''):
    
    if search_term is not '' and isinstance(search_term, list) and len(search_term)>0:
        search_term = search_term[0]
         
    
    potential_paths = generate_potential_paths()
    
    base_conf_re = re.compile(r"jupyter_(\w*_|)config\.(json|py)")
    local_conf_file_list = [f for f in glob.iglob("*")
                           if valid_gen_conf_file(f, base_conf_re)]
    
    base_conf_file_list = [f for d in potential_paths['base_conf_paths']
                           for f in glob.iglob(d+"/*")
                           if valid_gen_conf_file(f, base_conf_re)]
    
    
    nbconfig_pattern = r"({})\.json".format("|".join(n for n in NBCONFIG_SECTIONS))
    nbconfig_re = re.compile(nbconfig_pattern)
    nbconfig_file_list = [f for d in potential_paths['nbconfig_base_paths']
                          for f in glob.iglob(d+"/*")
                          if valid_gen_conf_file(f, nbconfig_re)]


    confd_re= re.compile(r"\w*\.json")
    confd_file_list = [f for d in potential_paths['conf_d_paths']
                       for f in sorted(glob.iglob(d+"/*"), reverse=True)
                       if valid_gen_conf_file(f, confd_re)]

    conf_file_list = list(itertools.chain(local_conf_file_list,
                                          base_conf_file_list,
                                          nbconfig_file_list,
                                          confd_file_list ))
    
    # go through files,
    # if search term found in file
    # print name, line_no, content
    for file_name in conf_file_list:
        if len(search_term)>0:
            print_indexed_content(file_name=file_name, search_term=search_term)
        else:
            print(file_name)
    
def print_indexed_content(file_name='', search_term=''):
    with open(file_name,"r") as f:
        if search_term in f.read():
            f.seek(0)
            line_numbers_match = []
            for line_no, text in enumerate(f,1):
                if search_term in text:
                    line_numbers_match.append((line_no,text.strip()))
            output = ["{}: {}".format(x,y) for x,y in line_numbers_match]
            print(file_name + "\n" + "\n".join(output),"\n")


main = launch_new_instance = JupyterConfigApp.launch_instance
