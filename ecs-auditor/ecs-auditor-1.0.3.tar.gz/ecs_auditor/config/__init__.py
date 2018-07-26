import os
import sys
import yaml

settings=None

def get_relative_path():
    return os.path.abspath(os.path.dirname(__file__))

def load_config(file_name):
    f = open("{}/{}".format( os.getcwd(),file_name))
    data = yaml.load(f)
    f.close()

    return data
