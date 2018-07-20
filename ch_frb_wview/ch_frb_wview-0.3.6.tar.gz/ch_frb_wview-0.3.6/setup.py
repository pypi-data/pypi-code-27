#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from setuptools import setup
from codecs import open
#from os import path

#here = path.abspath(path.dirname(__file__))

#with open(path.join(here, 'requirements.txt')) as f:
#    requirements = f.readlines()

setup(
    name='ch_frb_wview',
    version='0.3.6',
    description='Web Application to operate the FRB L1 system.'
,

    author='Dustin Lang, Chitrang Patel',
    author_email='chitrang.patel@mail.mcgill.ca',
    url="https://github.com/CHIMEFRB/frb_monitoring.git",
   # packages= ['ch_frb_wview'],
   # data_files=[(".", ['ch_frb_wview/templates/includes/_messages.html',
   #                    'ch_frb_wview/templates/includes/_navbar.html',
   #                    'Pipfile',
   #                    'README.md',
   #                    'ch_frb_wview.service', 
   #                    'ch_frb_wview/config/l1_production_8beam_webapp.yaml',
   #                    'ch_frb_wview/static/*.js', 
   #                    'ch_frb_wview/static/*.css',
   #                    'ch_frb_wview/static/bootstrap-4/css/*.css', 
   #                    'ch_frb_wview/static/bootstrap-4/js/*.js',
   #                    'ch_frb_wview/templates/*.js',
   #                    'ch_frb_wview/templates/*.html',
   #                   ]
   #            )],
    package_data={'': ['ch_frb_wview.service',
                       'Pipfile',
                       'README.md',
                       'config/l1_production_8beam_webapp.yaml',
                       'static/d3.min.js',
                       'static/fullcalendar.css',
                       'static/fullcalendar.min.js',
                       'static/fullcalendar.print.css',
                       'static/jquery.js',
                       'static/moment.min.js', 
                       'static/bootstrap-4/css/*.css', 
                       'static/bootstrap-4/js/*.js',
                       'templates/*.js',
                       'templates/*.html',
                       'templates/includes/*.html',
                 ]},
    #py_modules=['webapp', 'chime_frb_operations', 'chlog_database', 'cnc_ssh', 'cnc_client'],
    include_package_data=True,
    install_requires=['flask',
                      'pyyaml',
                      'msgpack',
                      'numpy',
                      'sqlalchemy',
                      'passlib',
                      'zmq',
                      'scipy',
                      'requests',
                      'matplotlib']
)
