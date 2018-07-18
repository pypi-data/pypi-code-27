#!/usr/bin/env python3

import setuptools

def upload_command(*args, **kwargs):
    from distutils_twine import UploadCommand
    return UploadCommand(*args, **kwargs)

setuptools.setup(cmdclass={"release": upload_command})
