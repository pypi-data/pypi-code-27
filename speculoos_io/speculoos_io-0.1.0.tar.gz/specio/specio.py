# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:22:11 2016

@author:
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import specio_get
import pickle
import os



###############################################################################
# Define version
###############################################################################
__version__ = '0.1.0'

    
'''
Note that cfitsio/fitsio is 20x faster than astropy/pyfits for single objects
pyfits (all objects, 5x) 29.4824950695s
fitsio (all objects, 5x) 30.8622791767s
pyfits (one object, 5x)  8.09786987305s
fitsio (one object, 5x)  0.49312210083s
'''



###############################################################################
# Finder (Main Program)
###############################################################################
#def find(RA, DEC, filter_band='all', unit='hmsdms', frame='icrs',
#         give_obj_id=True, search_radius=0.0014, field_radius=2., outfname=None):
#    '''find the obj_id of a given RA and Dec with specio_find.py; see specio_find.py for docstring'''
#    
#    print('#RA\tDEC\tfieldname\tfilter_band\tobj_id')
#    specio_find.find(RA, DEC, filter_band=filter_band, unit=unit, frame=frame,  
#                     give_obj_id=give_obj_id, search_radius=search_radius, 
#                     field_radius=field_radius, outfname=outfname)
#    
#    
#    
#def find_list(fname, usecols=(0,1), filter_band='all', unit='hmsdms', frame='icrs',
#              give_obj_id=True, search_radius=0.014, field_radius=2., outfname=None):
#    '''find the obj_id of multiple given RAs and Decs with specio_find.py; see specio_find.py for docstring'''
#    
#    print('#RA\tDEC\tfieldname\tfilter_band\tobj_id')
#    RAs, DECs = np.genfromtxt(fname, usecols=usecols, delimiter='\t', dtype=None, unpack=True)
#    for i in range(len(RAs)):
#        specio_find.find(RAs[i], DECs[i], filter=filter_band, unit=unit, frame=frame, 
#                     give_obj_id=give_obj_id, search_radius=search_radius, 
#                     field_radius=field_radius, outfname=outfname)




###############################################################################
# Getter (Main Program)
###############################################################################

def get(telescope, field_name, filter_band, keys, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=False, set_nan=False):
    '''get data for a given object with specio_get.py; see specio_get.py for docstring'''
            
    dic = specio_get.get(telescope, field_name, filter_band, keys, obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
            
    return dic
    
    
    

###############################################################################
# Save to pickle
###############################################################################
    
def save(outfilename, fieldname, filter_band, keys, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=False, set_nan=False):
    '''save data for a given object to outfilename.pickle via specio_get.py; see specio_get.py for docstring'''
            
    dic = get(fieldname, filter_band, keys, obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
        
    pickle.dump( dic, open( outfilename+'.pickle', 'wb' ) )
    
    
 

###############################################################################
# Convenience functions
###############################################################################

def plot_lc(telescope, field_name, filter_band, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=True, set_nan=False, 
        normalized=True):
    
    dic = get(telescope, field_name, filter_band, ['JD','FLUX'], obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
    
    
    dic['FLUX'][ dic['FLUX']==0 ] = np.nan
    
    if normalized:
        dic['FLUX'] /= np.nanmedian(dic['FLUX'])
    
    t = dic['JD'] - 2450000
    fig, ax = plt.subplots()
    ax.plot(t, dic['FLUX'], 'k.', rasterized=True)
    ax.set(xlabel='JD (-2450000 d)', ylabel='FLUX', title=field_name + '_' + filter_band + ', ' + str(obj_id))
    
    return fig, ax



def plot_overview(telescope, field_name, filter_band, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=True, set_nan=False):
    '''
    FLUX     |  FWHM      |  SKYLEVEL  |  AIRMASS
    --------------------------------------------------
    RA_MOVE  |  DEC_MOVE  |  CCD-TEMP  |  POINTING ERR
    '''
    
    keys = ['FLUX', 'FWHM', 'SKYLEVEL', 'AIRMASS', 'RA_MOVE', 'DEC_MOVE', 'CCD-TEMP']
    dic = get(telescope, field_name, filter_band, keys+['JD'], obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
    
    try:
        dic_ACP = get_ACP_pointing(telescope,time_hjd=time_hjd)
    except:
        pass
    
    t = dic['JD']-2450000
    fig, axes = plt.subplots(2,4,figsize=(16,6),sharex=True)
    for i in range(len(keys)+1):
        ii,jj = np.unravel_index(i, (2,4))
        if i<7:
            axes[ii,jj].plot(t, dic[keys[i]], 'k.', rasterized=True)
            axes[ii,jj].set(ylabel=keys[i])
            xmin, xmax = axes[ii,jj].get_xlim()
        if i==7:
            try:
                axes[ii,jj].plot(dic_ACP['JD']-2450000, dic_ACP['POINTING_ERR'], 'k.', rasterized=True)
            except:
                pass
            axes[ii,jj].set(ylabel='POINTING_ERR', xlim=(xmin,xmax))
        if ii>0: 
            axes[ii,jj].set(xlabel='JD (-2450000 d)')
#    axes[-1,-1].axis('off')
    plt.suptitle = field_name + '_' + filter_band
    plt.tight_layout()
    
    return fig, axes
    
    

def plot_any(telescope, field_name, filter_band, key, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=True, set_nan=False):
    
    dic = get(telescope, field_name, filter_band, ['JD-OBS', key], obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
    
    t = dic['JD-OBS'] - 2450000
    fig, ax = plt.subplots()
    ax.plot(t, dic[key], 'k.', rasterized=True)
    ax.set(xlabel='JD-OBS (-2450000 d)', ylabel=key, title=field_name + '_' + filter_band)
    
    return fig, ax
    


def print_stats(telescope, field_name, filter_band, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=True, set_nan=False,
        sep='\t'):
    
    dic = get(telescope, field_name, filter_band, ['STATS'], obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
    
    print('#NUM_NIGHTS_TOTAL', sep, 'NUM_IMAGES_TOTAL')
    print(len(dic['STATS'][0]), sep, np.sum(dic['STATS'][1]))
    print('')
    
    print('#DATE', sep, 'NUM_IMAGES')
    for i in range(len(dic['STATS'][0])):
        print(dic['STATS'][0][i], sep, dic['STATS'][1][i])
        
        

###############################################################################
# For ACP pointing
###############################################################################
def get_ACP_pointing(telescope,time_hjd=None):
    from astropy.time import Time
    
    roots = specio_get.standard_roots(telescope, None, True)
    fname = os.path.join( roots['logs'], 'ACP_pointing.txt' )
    data = np.genfromtxt(fname,dtype=None,names=True,delimiter=',',encoding='utf-8')
    
    if time_hjd is not None:
        ind = np.where( data['DATE'] == time_hjd )[0]
        data = data[:][ind]
                
    dic = {}
    for key in data.dtype.names:
        dic[key] = data[key]
        
    times = [ str(date)+'T'+str(time) for i,(date,time) in enumerate(zip(dic['DATE'],dic['TIME']))]
    dic['JD'] = Time(times, format='isot', scale='utc').jd
    return dic
            
        
        
def plot_ACP_pointing(telescope,time_hjd=None):
    dic = get_ACP_pointing(telescope, time_hjd=time_hjd)
    t = dic['JD'] - 2450000
    fig, ax = plt.subplots()
    ax.plot(t, dic['POINTING_ERR'], 'k.', rasterized=True)
    ax.set(xlabel='JD (-2450000 d)', ylabel='Pointing error', title=telescope)
    return fig, ax



###############################################################################
# Needed for Jupyter Notebook
###############################################################################
def root(telescope):
    return specio_get.standard_roots(telescope, None, True)['nights']
    
    
    
#if __name__ == '__main__':
#     plot_ACP_pointing('Callisto')
#     plot_ACP_pointing('Callisto',time_hjd='2018-06-04')