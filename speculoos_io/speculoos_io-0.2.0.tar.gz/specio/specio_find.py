#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:01:08 2018

@author:
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""

import numpy as np
import specio_get
import os, glob
import astropy.io.fits as pyfits



def find_ccdx_ccdy(x, y, telescope, field_name, filter_band, max_sqdist=1000, fnames=None, root=None, roots=None, silent=True):

#    dic = specio_get.get(telescope, field_name, filter_band, ['OBJ_ID','CCDX','CCDY'], fnames=fnames, root=root, roots=roots, silent=silent)
#    print dic['CCDX'][100], dic['CCDY'][100], dic['OBJ_ID'][100]
    
    dic = specio_get.get(telescope, field_name, filter_band, ['OBJ_ID','CCDX','CCDY'], fnames=fnames, root=root, roots=roots, silent=silent)
#    xref = dic['CCDX']
#    yref = dic['CCDY']
    xref = np.nanmean(dic['CCDX'], axis=1)
    yref = np.nanmean(dic['CCDY'], axis=1)
    sqdist = (xref-x)**2 + (yref-y)**2
    if np.nanmin(sqdist)<max_sqdist:
        ind = np.nanargmin( sqdist )
        return dic['OBJ_ID'][ ind ]
    else:
        return None
    
    

def find_ccdx_ccdy_from_stacked_image(x, y, telescope, field_name, filter_band, max_sqdist=1000, fnames=None, root=None, roots=None, silent=True):
    roots = specio_get.standard_roots(telescope, root, silent)
    dirname = os.path.join( roots['nights'], 'StackImages', '' )
    posname = glob.glob( os.path.join( dirname, field_name+'_stack_catalogue_'+filter_band+'.fts' ) )[0]
    pos = {}
    with pyfits.open(posname) as hdulist:
        pos['OBJ_ID'] = np.array([ 'SP'+str(int(sn) - 1).zfill(6) for sn in hdulist[1].data['Sequence_number'] ]) #assume seq number is always obj_id+1...
        pos['X'] = hdulist[1].data['X_coordinate']
        pos['Y'] = hdulist[1].data['Y_coordinate']
    sqdist = (pos['X']-x)**2 + (pos['Y']-y)**2
    if np.nanmin(sqdist)<max_sqdist:
        ind = np.nanargmin( sqdist )
        return pos['OBJ_ID'][ ind ]
    else:
        return None
