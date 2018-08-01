#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

import pip

from lztools.Data.Text import regex
from lztools.Managers.TempPath import TempPath

def extract_module_version(text):
    return regex(" \d+\.\d+\.\d+", text, only_first=True)[1:]

def local_install(path, upload=False):
    output_func = _upload if upload else None
    _install(path, output_func)

def _upload(path):
    online = get_version_online(os.path.basename(path))
    local = get_version(path)
    if online == local:
        raise Exception("Error: Same version as online")
    else:
        subprocess.call(["twine", "upload", "dist/*"])

def _install(path, output_func=None):
    with TempPath(path) as rp:
        subprocess.call(["rm", "-rf", "dist"])
        subprocess.call(["python", "setup.py", "install"])
        e = None
        if output_func is not None:
            try:
                output_func(rp)
            except Exception as e:
                pass

        subprocess.call(["rm", "-rf", "build"])
        subprocess.call(["rm", "-rf", "dist"])
        subprocess.call(["rm", "-rf", "*.egg-info"])
        if e is not None:
            raise e

def get_version_online(name):
    out = subprocess.check_output(["python", "-m", "pip", "show", "-V", name])
    return extract_module_version(out).rstrip("\n")

def get_version(path):
    with TempPath(path) as rp:
        return subprocess.check_output(["python", "setup.py", "-V"]).rstrip("\n")

def pip_install(package):
    pip.main(['install', package])



