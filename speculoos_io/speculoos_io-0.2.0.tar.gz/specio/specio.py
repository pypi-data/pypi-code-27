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
import specio_find
import pickle
import os, sys, socket, glob
import astropy.io.fits as pyfits
import astropy.visualization as pyvis




###############################################################################
# Define version
###############################################################################
__version__ = '0.2.0'

    
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
# Get keys
###############################################################################

def get_available_keys(telescope, field_name, filter_band, root=None, roots=None, fnames=None, silent=True):
    return specio_get.get_available_keys(telescope, field_name, filter_band, root=None, roots=None, fnames=None, silent=True)               

    

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



def plot_overview(telescope, field_name, filter_band, extra_keys=[], obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=True, set_nan=False, 
        normalized=True, color='lightgrey', figsize='normal'):
    '''
    FLUX     |  FWHM      |  SKYLEVEL  |  AIRMASS
    --------------------------------------------------
    RA_MOVE  |  DEC_MOVE  |  CCD-TEMP  |  POINTING ERR
    --------------------------------------------------
    EXTRA_1  |  EXTRA_2   | ...
    '''
    
    keys = ['FLUX', 'FWHM', 'SKYLEVEL', 'AIRMASS', 'RA_MOVE', 'DEC_MOVE', 'CCD-TEMP'] \
            + extra_keys
    dic = get(telescope, field_name, filter_band, keys+['JD'], obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
    
#    try:
#        dic_ACP = get_ACP_pointing(telescope,time_hjd=time_hjd)
#    except:
#        pass
    
    dic['FLUX'][ dic['FLUX']==0 ] = np.nan
    dic['FLUX_MEAN'] = np.nanmean(dic['FLUX'])
    dic['FLUX_MEDIAN'] = np.nanmedian(dic['FLUX'])
    if normalized:
        dic['FLUX'] /= dic['FLUX_MEDIAN']
        
    N_panels = len(keys)
    N_rows = int( np.ceil(N_panels/4.) )
        
    t = dic['JD']-2450000
    if figsize=='normal':
        fig, axes = plt.subplots(N_rows,4,figsize=(16,N_rows*3),sharex=True)
    elif figsize=='small':
        fig, axes = plt.subplots(N_rows,4,figsize=(11,N_rows*2.5),sharex=True)
    for i in range(N_rows*4):
        ii,jj = np.unravel_index(i, (N_rows,4))
        if i < len(keys):
            axes[ii,jj].plot(t, dic[keys[i]], 'k.', color=color, rasterized=True)
            axes[ii,jj].set(ylabel=keys[i])
            xmin, xmax = axes[ii,jj].get_xlim()
    #        if i==7:
    #            try:
    #                axes[ii,jj].plot(dic_ACP['JD']-2450000, dic_ACP['POINTING_ERR'], 'k.', rasterized=True)
    #            except:
    #                pass
    #            axes[ii,jj].set(ylabel='POINTING_ERR', xlim=(xmin,xmax))
        if i >= len(keys)-4: 
            axes[ii,jj].set(xlabel='JD (-2450000 d)')
            axes[ii,jj].tick_params(labelbottom=True)
        if i >= len(keys):
            axes[ii,jj].axis('off')
#    axes[-1,-1].axis('off')
    plt.suptitle = field_name + '_' + filter_band + ', Mean flux:' + str(dic['FLUX_MEAN'])
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
        
        
        


def print_infos(telescope, field_name, filter_band, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=True, set_nan=False,
        sep='\t'):
    
    dic = get(telescope, field_name, filter_band, ['STATS', 'EXPOSURE', 'FLUX', 'GAIA_ID', 'GMAG'], obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, set_nan=set_nan)
    
    dic['FLUX'][ dic['FLUX']==0 ] = np.nan
    dic['FLUX_MEAN'] = np.nanmean(dic['FLUX'])
    
    print(telescope, field_name, filter_band, obj_id)
    print('Gaia ID:', dic['GAIA_ID'])
    print('Nights:', len(dic['STATS'][0]))
    print('Images:', np.sum(dic['STATS'][1]))
    print('Mean exposure:', "{0:.0f}".format( np.nanmean(dic['EXPOSURE']) ), 's')
    print('Hours observed:', "{0:.1f}".format( np.sum(dic['STATS'][1]) * np.nanmean(dic['EXPOSURE']) / 3600. ), 'h')
    print('Date range:', 'from', dic['STATS'][0][0], 'to', dic['STATS'][0][-1])
    print('Mean flux:', "{0:.0f}".format( np.nanmean(dic['FLUX_MEAN']) ))
    print('G-mag:', "{0:.1f}".format( dic['GMAG'] ))
    
    

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
# Check on which nights which targets were observed
###############################################################################
def get_observing_log():   
    return specio_get.get_observing_log()
    


def save_observing_log():   
    
    #::: on laptop (OS X)m
    if sys.platform == "darwin":
        dirname = '/Users/mx/Big_Data/BIG_DATA_SPECULOOS/Observing_log/'    
    
    #::: on Cambridge servers
    elif 'ra.phy.cam.ac.uk' in socket.gethostname():
        dirname = '/appcg/data2/SPECULOOS/Observing_log/'    
        
    if not os.path.exists(dirname): os.makedirs(dirname)
    df = get_observing_log()
    pickle.dump(df, open(dirname+'Observing_log.pickle','wb'))
    df.to_html(dirname+'Observing_log.html')
    df.to_csv(dirname+'Observing_log.csv')
    
    
    
    
def load_observing_log(telescope=None, field_name=None, filter_band=None, date=None):   
    
    #::: on laptop (OS X)
    if sys.platform == "darwin":
        dirname = '/Users/mx/Big_Data/BIG_DATA_SPECULOOS/Observing_log/'    
    
    #::: on Cambridge servers
    elif 'ra.phy.cam.ac.uk' in socket.gethostname():
        dirname = '/appcg/data2/SPECULOOS/Observing_log/'  
        
    df = pickle.load(open(dirname+'Observing_log.pickle','rb'))
    if telescope is not None: df = df[ df.telescope==telescope ]
    if field_name is not None: df = df[ df.field_name==field_name ]
    if filter_band is not None: df = df[ df.filter_band==filter_band ]
    if date is not None: df = df[ df.date==date ]
    
    return df
    
    
    
###############################################################################
# Plot stacked image
###############################################################################
def plot_stackimage(telescope, field_name, filter_band, obj_id=None, apt=True, apt_radius=5, fnames=None, root=None, roots=None, silent=True):
    '''
    Note:
        the aperture positions of the stacked images DO NOT match the CCDX/Y values in the pipeline fits files
        they lie off from each other by a few pixels (up to tens of pixels)
        this is because the images are slightly rotated and stretched
        hence, need to take the sequence number from stacked_catalogue, which should always be obj_id+1
    '''
    roots = specio_get.standard_roots(telescope, root, silent)
    dirname = os.path.join( roots['nights'], 'StackImages', '' )

    imagename = glob.glob( os.path.join( dirname, field_name+'_outstack_'+filter_band+'.fts' ) )[0]
    image_data = pyfits.getdata(imagename)
    norm = pyvis.ImageNormalize(image_data, interval=pyvis.ZScaleInterval(), stretch=pyvis.SqrtStretch())
        
    if apt:
        posname = glob.glob( os.path.join( dirname, field_name+'_stack_catalogue_'+filter_band+'.fts' ) )[0]
        pos = {}
        with pyfits.open(posname) as hdulist:
            pos['OBJ_ID'] = np.array([ 'SP'+str(int(sn) - 1).zfill(6) for sn in hdulist[1].data['Sequence_number'] ]) #assume seq number is always obj_id+1...
            pos['X'] = hdulist[1].data['X_coordinate']
            pos['Y'] = hdulist[1].data['Y_coordinate']
    
    fig, ax = plt.subplots()    
    im = ax.imshow(image_data, cmap='gray', norm=norm, origin='lower')
    apt_artist = []
    if apt:
        #all
        for (x,y) in zip(pos['X'],pos['Y']):
            circle = plt.Circle((x, y), apt_radius, color='r', lw=2, fill=False)
            ln = ax.add_artist(circle)
            apt_artist.append(ln)
        #target
        if obj_id is not None:
            ind_target = np.where( pos['OBJ_ID']==obj_id )[0]
            circle = plt.Circle((pos['X'][ind_target], pos['Y'][ind_target]), apt_radius, color='lightblue', lw=2, fill=False)
            ln = ax.add_artist(circle)
            apt_artist.append(ln)
        
    plt.colorbar(im)
    
    return fig, ax, apt_artist
    




###############################################################################
# Find by CCDX CCDY coords
###############################################################################
def find_ccdx_ccdy(x, y, telescope, field_name, filter_band, fnames=None, root=None, roots=None, silent=True):
    return specio_find.find_ccdx_ccdy(x, y, telescope, field_name, filter_band, fnames=fnames, root=root, roots=roots, silent=silent)
    


def find_ccdx_ccdy_from_stacked_image(x, y, telescope, field_name, filter_band, fnames=None, root=None, roots=None, silent=True):
    return specio_find.find_ccdx_ccdy_from_stacked_image(x, y, telescope, field_name, filter_band, fnames=fnames, root=root, roots=roots, silent=silent)
    
    
        
    


###############################################################################
# Needed for Jupyter Notebook
###############################################################################
def root(telescope):
    return specio_get.standard_roots(telescope, None, True)['nights']
    

