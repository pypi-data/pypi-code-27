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
    
#    print specio.root(telescope)
#    
#    #::: print stats on observed nights and #images
#    specio.print_stats(telescope, field_name, filter_band)
#    
#    #::: plot a light curve
#    specio.plot_lc(telescope, field_name, filter_band, obj_id=obj_id)
#    
#    #::: plot a light curve of a selected day
#    specio.plot_lc(telescope, field_name, filter_band, obj_id=obj_id, time_date='2018-02-03')
#    
#    #::: plot seeing / ccd_temp / fwhm
#    specio.plot_any(telescope, field_name, filter_band, 'SEEING')
#    specio.plot_any(telescope, field_name, filter_band, 'CCD-TEMP')
#    specio.plot_any(telescope, field_name, filter_band, 'FWHM')
    
#    print specio.get_available_keys(telescope, field_name, filter_band)
    
    #:: plot overview
#    print specio.plot_overview(telescope, field_name, filter_band, extra_keys=['RA', 'DEC'], obj_id=obj_id)
    
#    specio.plot_stackimage(telescope, field_name, filter_band, obj_id='SP000100', apt=False)    

#    field_name = 'Sp0805-3158'        
#    specio.save_observing_log()
#    df = specio.load_observing_log(telescope=telescope, field_name=field_name, filter_band=filter_band)
#    print(df)
    
#    print(specio.find_ccdx_ccdy(1610,445,telescope, field_name, filter_band))