import json
import os
import inspect
import api_builder
import time

EXECUTABLE_NAME = 'api_builder'
APPLICATION_DESCRIPTION = '''
This is a CLI to build, package, and release AWS APIs using API Gateway and Lambda.
'''
ZLAB_CONF_FILE = "zlab-conf.json"
STATIC_DIR = os.path.join(os.path.dirname(inspect.getfile(api_builder)), "static")

_base_dir = os.getcwd()
_build_dir = os.path.join(_base_dir, "build")
_private_dir = os.path.join(_build_dir, "private")
_deps_dir = os.path.join(_private_dir, "deps")
_zip_dir = os.path.join(_private_dir, "lib")
_project_name = os.path.basename(_base_dir)
_cf_dir = os.path.join(_base_dir, "cloudformation")


def check_bootstrap():
    if not os.path.exists(ZLAB_CONF_FILE):
        raise ValueError("Application not bootstrapped.  Run `zlab bootstrap --name {ApplicationName}` to boostrap")

def get_zlab_conf():
    with open(ZLAB_CONF_FILE) as conf:
        return json.load(conf)

def write_zlab_conf(conf):
    f = open(os.path.join(ZLAB_CONF_FILE), 'w')
    f.write(json.dumps(conf))
    f.close()