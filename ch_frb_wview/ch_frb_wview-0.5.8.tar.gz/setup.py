#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from setuptools import setup
from codecs import open

setup(
    name='ch_frb_wview',
    version='0.5.8',
    description='Web Application to operate the FRB L1 system.'
,

    author='Dustin Lang, Chitrang Patel',
    author_email='chitrang.patel@mail.mcgill.ca',
    url="https://github.com/CHIMEFRB/frb_monitoring.git",
    packages= ['ch_frb_wview'],
    package_dir={'ch_frb_wview':'ch_frb_wview'},
    package_data={'ch_frb_wview': ['ch_frb_wview.service',
                       'Pipfile',
                       'README.md',
                       'ch_frb_wview/bin/run-webapp.sh',
                       'ch_frb_wview/bin/run-uwsgi.sh',
                       'ch_frb_wview/config/l1_production_8beam_webapp.yaml',
                       'ch_frb_wview/static/d3.min.js',
                       'ch_frb_wview/static/fullcalendar.css',
                       'ch_frb_wview/static/fullcalendar.min.js',
                       'ch_frb_wview/static/fullcalendar.print.css',
                       'ch_frb_wview/static/jquery.js',
                       'ch_frb_wview/static/moment.min.js', 
                       'ch_frb_wview/static/bootstrap-4/css/*.css', 
                       'ch_frb_wview/static/bootstrap-4/css/*.map', 
                       'ch_frb_wview/static/bootstrap-4/js/*.map', 
                       'ch_frb_wview/static/bootstrap-4/js/*.js', 
                       'ch_frb_wview/templates/strip-chart.js',
                       'ch_frb_wview/templates/includes/_navbar.html',
                       'ch_frb_wview/templates/includes/_messages.html',
                       'ch_frb_wview/templates/*.html',
                 ]},
    scripts=['ch_frb_wview/bin/run-uwsgi.sh', 'ch_frb_wview/bin/run-webapp.sh'],
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
