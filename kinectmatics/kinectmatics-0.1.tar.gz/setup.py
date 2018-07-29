"""kinectmatics setup script."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('kinectmatics', 'version.py')) as vf:
    exec(vf.read())
    
# Copy in long description.
#  Note: this is a partial copy from the README
#    Only update here in coordination with the README, to keep things consistent.
long_description = \
"""
========================================
kinectmatics: Kinect computer vision toolbox for movement kinematics
========================================
This is where a description of kinectmatics would go... if there was one.
"""

setup(
    name = 'kinectmatics',
    version = __version__,
    description = 'computer vision toolbox for analyzing movement kinematics from video',
    long_description = long_description,
    author = 'Translational Neural Engineering Lab',
    author_email = 'pgabriel@eng.ucsd.edu',
    url = 'https://gitlab.com/pgabriel/kinectmatics',
    packages = find_packages(),
    license = 'Apache License, 2.0',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
#        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    download_url = 'https://gitlab.com/pgabriel/kinectmatics/tags',
    keywords = ['kinematics', 'kinect', 'video processing', 'optical flow', 'computer vision'],
    install_requires = ['numpy', 'scipy'],
) 