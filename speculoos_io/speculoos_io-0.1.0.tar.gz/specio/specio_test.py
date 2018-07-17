#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:52:31 2018

@author:
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""

import specio

###############################################################################
# Testing
###############################################################################
    
if __name__ == '__main__':
    
    telescope = 'Callisto'
    field_name = 'Sp0544-2433'
    filter_band = 'I+z'
    obj_id = 'SP000002'
    
    print specio.root(telescope)
    
    #::: print stats on observed nights and #images
    specio.print_stats(telescope, field_name, filter_band)
    
    #::: plot a light curve
    specio.plot_lc(telescope, field_name, filter_band, obj_id=obj_id)
    
    #::: plot a light curve of a selected day
    specio.plot_lc(telescope, field_name, filter_band, obj_id=obj_id, time_date='2018-02-03')
    
    #::: plot seeing / ccd_temp / fwhm
    specio.plot_any(telescope, field_name, filter_band, 'SEEING')
    specio.plot_any(telescope, field_name, filter_band, 'CCD-TEMP')
    specio.plot_any(telescope, field_name, filter_band, 'FWHM')
    
    