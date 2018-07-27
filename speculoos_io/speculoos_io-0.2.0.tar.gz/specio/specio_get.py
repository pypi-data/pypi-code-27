# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:57:31 2017

@author:
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""

from __future__ import print_function

import warnings
import astropy.io.fits as pyfits
from astropy.time import Time
import fitsio
import os, sys, glob, socket, collections, datetime
import numpy as np



###############################################################################
# Helper function
###############################################################################
def warning_on_one_line(message, category, filename, lineno, file=None, line=''):
    return '\n%s: %s, line %s\n\t %s\n\n' % (category.__name__, filename, lineno, message)
warnings.formatwarning = warning_on_one_line

    

###############################################################################
# Getter (Main Program)
###############################################################################

def get(telescope, field_name, filter_band, keys, obj_id=None, obj_row=None, time_index=None, time_date=None, time_hjd=None, time_actionid=None, bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, fnames=None, root=None, roots=None, silent=False, set_nan=False):

    """
    Convenient wrapper for astropy and cfitsio readers for various SPECULOOS data files.
    Can handle either data formats as in prodstore/ or the MegaFile during pipeline runs.

    Parameters
    ----------
        
    field_name : str
        name of the SPECULOOS-field, e.g. 'Sp0544-2433'
    
    keys : str / array of str
        which parameters shall be read out from the fits files, e.g. ['RA','DEC','HJD','FLUX']. See below for other valid requests.
    
    obj_id, obj_row : int / str / textfilename / array of int / array of str
        identifier of the objects to be read out. If empty, all objects will be retrieved. Only either obj_id or obj_row can be chosen as input, not both. obj_id reads out objects by their object IDs. obj_row reads the requested rows from the fits file. Examples:    
            obj_id = 46,    obj_id = '046',    obj_id = '00046',    obj_id = [46,57,1337],    obj_id = range(1,100),    obj_id = 'object_ids.txt'
            obj_row = 1,    obj_row = [1,2,3,1337],     obj_row = range(1,100),     obj_row = 'object_rows.txt'
    
    time_index, time_date, time_hjd, time_actionid : int / str / textfilename / array of int / array of str
        identifier of the times/exposures to be read out. If empty, all times/exposures will be retrieved. Only either of these can be chosen as input, not more than one. time_index reads out the requested columns from the fits file, and hence allows to read out as little as one exposure. time_date reads all exposures per given calendar date(s). time_hjd reads all exposures per given HJD-date (only HJD values given as integers are accepted). time_actionid reads all exposures per given action ID. Examples:
            time_index = 1,    time_index = [1,2,3,1337],    time_index = range(1,100),    time_index = 'time_indices.txt'
            time_date = 20151104,    time_date = '20151104',    time_date = '2015-11-04',    time_date = '2015/11/04',    time_date = 'dates.txt'
            time_hjd = 674,    time_hjd = [674,675,680],    time_hjd = 'hjds.txt'
            time_actionid = 108583,    time_actionid = [108583,133749],    time_actionid = 'actionids.txt'      
    
    bls_rank : int
        which BLS RANK should be read out from the BLS fits files (e.g. when reading 'PERIOD')
        
    indexing : str
        following which format are the obj_rows and time_indices given (standard is 'fits')?
            'fits': indexing rows from 1
            'python': indexing rows from 0    
    
    fitsreader : str
        'pyfits' or 'astropy': use the astropy.io.fits module. 
        'fitsio' or 'cfitsio': use the fitsio module (standard) 
        fitsio seems to perform best, see below for performance tests.
     
    simplify : bool  
        if True and only one object is requested, it simplifies the dictionary entries into 1D nd.arrays (otherwise they will be 2D nd.arrays with an empty dimension). Standard is True.
   
    fnames : dict
        This allows to manually pass a dictionary of filenames. Leave blank if you want to run it on Warwick's or Cambridge's SPECULOOS cluster. Contains the following keys:
        a) if used in a pipeline run:
        fnames['BLSPipe_megafile']
        b) if used for final data prodcuts:
        fnames['nights']
        fnames['sysrem'] (optional)
        fnames['bls'] (optional)
        fnames['decorr'] (optional)
        fnames['canvas'] (optional)
        fnames['dilution'] (optional)
            
    
    root : str
        This allows to manually pass a single root directory. Leave blank if you want to run it on Warwick's or Cambridge's SPECULOOS cluster. The root directory structure has to contain all individual fits files.
    
    roots : dict
        This allows to manually pass different root directories, such as for prodstore/0*/[MergePipe*, BLSPipe*, SysremPipe*]. Leave blank if you want to run it on Warwick's or Cambridge's SPECULOOS cluster. Contains the following keys:
            roots['nights']
            roots['sysrem'] (optional)
            roots['bls'] (optional)
            roots['decorr'] (optional)
            roots['canvas'] (optional)
            roots['dilution'] (optional)
    
    silent : bool
        Whether a short report should be printed or not.
        
    ngtsversion : str
        From which directory shall the files be read? Standard is usually the latest release. Irrelevant if filenames are given manually via fnames=fnames.

    set_nan : bool
        Whether all flagged values in CCDX/Y, CENDTX/Y and FLUX should be replaced with NAN or not (if not, they might be zeros or any reasonable/unreasonable real numbers).


    Possible keys
    -------------

    a) Nightly Summary Fits file

        From 'CATALOGUE' (per object):
        ['OBJ_ID', 'RA', 'DEC', 'REF_FLUX', 'CLASS', 'CCD_X', 'CCD_Y', 'FLUX_MEAN', 'FLUX_RMS', 'MAG_MEAN', 'MAG_RMS', 'NPTS', 'NPTS_CLIPPED']
    
        From 'IMAGELIST' (per image):
        ['ACQUMODE', 'ACTIONID', 'ACTSTART', 'ADU_DEV', 'ADU_MAX', 'ADU_MEAN', 'ADU_MED', 'AFSTATUS', 'AGREFIMG', 'AGSTATUS', 'AG_APPLY', 'AG_CORRX', 'AG_CORRY', 'AG_DELTX', 'AG_DELTY', 'AG_ERRX', 'AG_ERRY', 'AIRMASS', 'BIASMEAN', 'BIASOVER', 'BIASPRE', 'BIAS_ID', 'BKG_MEAN', 'BKG_RMS', 'CAMERAID', 'CAMPAIGN', 'CCDTEMP', 'CCDTEMPX', 'CHSTEMP', 'CMD_DEC', 'CMD_DMS', 'CMD_HMS', 'CMD_RA', 'COOLSTAT', 'CROWDED', 'CTS_DEV', 'CTS_MAX', 'CTS_MEAN', 'CTS_MED', 'DARK_ID', 'DATE-OBS', 'DATE', 'DITHER', 'EXPOSURE', 'FCSR_ENC', 'FCSR_PHY', 'FCSR_TMP', 'FIELD', 'FILTFWHM', 'FLAT_ID', 'FLDNICK', 'GAIN', 'GAINFACT', 'HSS_MHZ', 'HTMEDXF', 'HTRMSXF', 'HTXFLAGD', 'HTXNFLAG', 'HTXRAD1', 'HTXSIG1', 'HTXTHTA1', 'HTXVAL1', 'IMAGE_ID', 'IMGCLASS', 'IMGTYPE', 'LST', 'MINPIX', 'MJD', 'MOONDIST', 'MOONFRAC', 'MOONPHSE', 'MOON_ALT', 'MOON_AZ', 'MOON_DEC', 'MOON_RA', 'NBSIZE', 'NIGHT', 'NUMBRMS', 'NXOUT', 'NYOUT', 'OBJECT', 'OBSSTART', 'PROD_ID', 'PSFSHAPE', 'RCORE', 'READMODE', 'READTIME', 'ROOFSTAT', 'SATN_ADU', 'SEEING', 'SKYLEVEL', 'SKYNOISE', 'STDCRMS', 'SUNDIST', 'SUN_ALT', 'SUN_AZ', 'SUN_DEC', 'SUN_RA', 'TC3_3', 'TC3_6', 'TC6_3', 'TC6_6', 'TCRPX2', 'TCRPX5', 'TCRVL2', 'TCRVL5', 'TEL_ALT', 'TEL_AZ', 'TEL_DEC', 'TEL_HA', 'TEL_POSA', 'TEL_RA', 'THRESHOL', 'TIME-OBS', 'TV6_1', 'TV6_3', 'TV6_5', 'TV6_7', 'VI_MINUS', 'VI_PLUS', 'VSS_USEC', 'WCSPASS', 'WCS_ID', 'WXDEWPNT', 'WXHUMID', 'WXPRES', 'WXTEMP', 'WXWNDDIR', 'WXWNDSPD', 'XENCPOS0', 'XENCPOS1', 'YENCPOS0', 'YENCPOS1', 'TMID']
    
        From image data (per object and per image):
        HJD
        FLUX
        FLUX_ERR
        FLAGS
        CCDX
        CCDY
        CENTDX_ERR
        CENTDX
        CENTDY_ERR
        CENTDY
        SKYBKG


    b) Sysrem Fits File

        Sysrem flux data (per object and per image):
        SYSREM_FLUX3


    c) BLS Fits File

        From 'CATALOGUE' (for all objects):
        ['OBJ_ID', 'BMAG', 'VMAG', 'RMAG', 'JMAG', 'HMAG', 'KMAG', 'MU_RA', 'MU_RA_ERR', 'MU_DEC', 'MU_DEC_ERR', 'DILUTION_V', 'DILUTION_R', 'MAG_MEAN', 'NUM_CANDS', 'NPTS_TOT', 'NPTS_USED', 'OBJ_FLAGS', 'SIGMA_XS', 'TEFF_VK', 'TEFF_JH', 'RSTAR_VK', 'RSTAR_JH', 'RPMJ', 'RPMJ_DIFF', 'GIANT_FLG', 'CAT_FLG']
    
        From 'CANDIDATE' data (only for candidates):
        ['OBJ_ID', 'RANK', 'FLAGS', 'PERIOD', 'WIDTH', 'DEPTH', 'EPOCH', 'DELTA_CHISQ', 'CHISQ', 'NPTS_TRANSIT', 'NUM_TRANSITS', 'NBOUND_IN_TRANS', 'AMP_ELLIPSE', 'SN_ELLIPSE', 'GAP_RATIO', 'SN_ANTI', 'SN_RED', 'SDE', 'MCMC_PERIOD', 'MCMC_EPOCH', 'MCMC_WIDTH', 'MCMC_DEPTH', 'MCMC_IMPACT', 'MCMC_RSTAR', 'MCMC_MSTAR', 'MCMC_RPLANET', 'MCMC_PRP', 'MCMC_PRS', 'MCMC_PRB', 'MCMC_CHISQ_CONS', 'MCMC_CHISQ_UNC', 'MCMC_DCHISQ_MR', 'MCMC_PERIOD_ERR', 'MCMC_EPOCH_ERR', 'MCMC_WIDTH_ERR', 'MCMC_DEPTH_ERR', 'MCMC_RPLANET_ERR', 'MCMC_RSTAR_ERR', 'MCMC_MSTAR_ERR', 'MCMC_CHSMIN', 'CLUMP_INDX', 'CAT_IDX', 'PG_IDX', 'LC_IDX']

    
    d) CANVAS Text File (if existant)
    
        ['CANVAS_PERIOD','CANVAS_EPOCH','CANVAS_WIDTH','CANVAS_DEPTH','CANVAS_Rp','CANVAS_Rs',...]
    
    
    e) DILUTION Fits File (if existant)
    
        'DILUTION'
        
    
    Returns
    -------
    dic : dict
        dictionary containing all the requested keys
        
        
    Note
    ----
    ngtsio can be used for either final products or within a pipeline run
    If used in pipeline run, fnames['BLSPipe_megafile'] is required
    If used for final products from prodstore/0* fnames['nights'], fnames['sysrem'] and fnames['bls'] may be required
    
    Naming conventions differ between pipeline and final prodcuts
    In pipeline: FLUX
    In final prodcuts: FLUX3, SYSREM_FLUX3, DECORR_FLUX3
    """


    if not silent: 
        print('Telescope:\t', telescope)
        print('Field name:\t', field_name)
        print('Filter band:\t', filter_band)

    if (roots is None) and (fnames is None):
        roots = standard_roots(telescope, root, silent)
    
    if fnames is None: 
        fnames = standard_fnames(telescope, field_name, filter_band, roots, silent)
    
    if fnames is not None:
        keys_0 = 1*keys #copy list
        keys_0.append('OBJ_ID')
        
        #::: append FLAGS for set_nan
        if set_nan and ('FLAGS' not in keys_0): 
            keys.append('FLAGS')
            
        #::: append JD-OBS for statistics
        if ('DATE-OBS' in keys) and ('JD-OBS' not in keys):
            keys.append('JD-OBS')
        if ('STATS' in keys) and ('JD-OBS' not in keys):
            keys.append('JD-OBS')
        
        #::: objects
        ind_objs, obj_ids = get_obj_inds(fnames, obj_id, obj_row, indexing, fitsreader, obj_sortby = 'obj_ids')
        if not silent: print('Object IDs (',len(obj_ids),'):', obj_ids)
        
        #::: only proceed if at least one of the requested objects exists
        if isinstance(ind_objs,slice) or len(ind_objs)>0:
            
            #::: time
            ind_time = get_time_inds(fnames, time_index, time_date, time_hjd, time_actionid, fitsreader, silent)
            
            #::: get dictionary
            dic, keys = get_data(fnames, obj_ids, ind_objs, keys, bls_rank, ind_time, fitsreader)
                
            #::: set flagged values and flux==0 values to nan
            if set_nan:
                dic = set_nan_dic(dic)
                
            #::: compute DATE-OBS if requested
            if 'DATE-OBS' in keys_0:
                dic['DATE-OBS'] = Time(dic['JD-OBS'] - 0.5, format='jd', scale='utc', out_subfmt='date').iso
            
            #::: compute STATS if requested
            if 'STATS' in keys_0:
                dic['STATS'] = np.unique(Time(dic['JD-OBS'] - 0.5, format='jd', scale='utc', out_subfmt='date').iso, return_counts=True)
            
            #::: remove entries that were only needed for readout / computing things
            if ('FLAGS' in dic.keys()) and ('FLAGS' not in keys_0): 
                del dic['FLAGS']
            if ('JD-OBS' in dic.keys()) and ('JD-OBS' not in keys_0): 
                del dic['JD-OBS']
            
            #::: simplify output if only for 1 object
            if simplify: 
                dic = simplify_dic(dic)
            
            #::: add field_name and filter_band
            dic['telescope'] = telescope
            dic['field_name'] = field_name
            dic['filter_band'] = filter_band
            
            #::: check if all keys were retrieved
            check_dic(dic, keys_0, silent)
            
        else:
            dic = None
 
    else: 
        dic = None
    
    return dic




###############################################################################
# Fielnames Formatting
###############################################################################
def standard_roots(telescope, root, silent):
    
    try:
        if (root is None):
    
            #::: on laptop (OS X)
            if sys.platform == "darwin":
                roots = {}
                roots['nights'] = scalify(glob.glob('/Users/mx/Big_Data/BIG_DATA_SPECULOOS/'+telescope+'/callisto_pipeline_output/'))
                roots['logs'] = scalify(glob.glob('/Users/mx/Big_Data/BIG_DATA_SPECULOOS/'+telescope+'/processed_logs/'))
            #::: on Cambridge servers
            elif 'ra.phy.cam.ac.uk' in socket.gethostname():
                roots = {}
                roots['nights'] = scalify(glob.glob('/appcg/data2/SPECULOOSPipeline/'+telescope+'/output/'))
                roots['logs'] = scalify(glob.glob('/appcg/data2/SPECULOOS/'+telescope+'_Logs/'))

        #if a single root is given, it will overwrite individual roots
        elif root is not None:
            roots = {}
            roots['nights'] = root
        
        #otherwise roots has been given (try-except will catch the None or non-existing entries)
        else:
            pass   
        
    except:
#        raise ValueError('Requested files do not exist. Please check file directories.')
        warnings.warn('Requested roots do not exist. Please check file directories.')
        roots = None
        
    return roots
    
    
    
    
def standard_fnames(telescope, field_name, filter_band, roots, silent):
    
    try: 
        fnames = {}
        
        #Nights
        #a list of all single files (e.g. FLAGS, FLUX3, FLUX3_ERR, CCDX etc.)
        try:
            f_nights = os.path.join( roots['nights'], field_name+'_' + filter_band + '*.fts' )
            fnames['nights'] = glob.glob( f_nights )[0]
        except:
            fnames['nights'] = None        

    except:
        warnings.warn('Requested files do not exist. Please check file directories.')   
        fnames = None

    return fnames




def get_name(fnames, keys):
    for key in keys:
        fnames[key] = scalify([x for x in fnames['nights'] if key+'.fits' in x])
    return fnames

    


def scalify(l, out='first'):
    if len(l) == 0: 
        return None
    else:
        if out=='first': 
            return l[0]
        elif out=='last': 
            return l[-1]
        elif out=='all': 
            return l




###############################################################################
# Object Input Formatting
###############################################################################

def get_obj_inds(fnames, obj_ids, obj_rows, indexing,fitsreader, obj_sortby = 'obj_ids'):

    inputtype = None


    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::: if no input is given, use all objects
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    if obj_ids is None and obj_rows is None:

        inputtype = None
        ind_objs = slice(None)
        obj_ids = get_objids_from_indobjs(fnames, ind_objs, fitsreader)


    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::: if obj_id is given
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    elif obj_ids is not None and obj_rows is None:

        inputtype = 'obj_ids'

        # b) test if non-empty list
        if isinstance(obj_ids, (collections.Sequence, np.ndarray)) and not isinstance(obj_ids, (str, unicode)) and len(np.atleast_1d(obj_ids)) > 0:
            #make sure its not a 0-dimensional ndarray
            obj_ids = np.atleast_1d(obj_ids)
            # if list of integer or float -> convert to list of str
            if not isinstance(obj_ids[0], str):
                obj_ids = map(int, obj_ids)
                if not all(x>0 for x in obj_ids):
                    error = '"obj_id" data type not understood.'
                    sys.exit(error)
                obj_ids = map(str, obj_ids)
            # give all strings 6 digits
            obj_ids = objid_6digit(obj_ids)
            # connect obj_ids to ind_objs
            ind_objs, obj_ids = get_indobjs_from_objids(fnames, obj_ids, fitsreader)


        #c) test if file
        elif isinstance(obj_ids, str) and os.path.isfile(obj_ids):
            # load the file
            obj_ids = np.loadtxt(obj_ids, dtype='S6').tolist()
            # cast to list
            if isinstance(obj_ids, str):
                obj_ids = [obj_ids]
            # give all strings 6 digits
            obj_ids = objid_6digit(obj_ids)
            # connect obj_ids to ind_objs
            ind_objs, obj_ids = get_indobjs_from_objids(fnames, obj_ids, fitsreader)


        # d) test if str
        elif isinstance(obj_ids, str) and not os.path.isfile(obj_ids):
            # cast to list
            obj_ids = [obj_ids]
            # give all strings 6 digits
            obj_ids = objid_6digit(obj_ids)
            # connect obj_ids to ind_objs
            ind_objs, obj_ids = get_indobjs_from_objids(fnames, obj_ids, fitsreader)


        # e) test if int/float
        elif isinstance(obj_ids, (int, float)) and obj_ids>=0:
            # cast to list of type str
            obj_ids = [ str(int(obj_ids)) ]
            # give all strings 6 digits
            obj_ids = objid_6digit(obj_ids)
            # connect obj_ids to ind_objs
            ind_objs, obj_ids = get_indobjs_from_objids(fnames, obj_ids, fitsreader)


        # problems:
        else:
            error = '"obj_id" data type not understood.'
            sys.exit(error)


    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::: if obj_row is given
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    elif obj_ids is None and obj_rows is not None:

        inputtype = 'ind_objs'

        ind_objs = obj_rows

        # a) test if non-empty list
        if isinstance(ind_objs, (collections.Sequence, np.ndarray)) and not isinstance(ind_objs, (str, unicode)) and len(ind_objs) > 0:
            # if list of str or float -> convert to list of int
            if isinstance(ind_objs[0], (str,float)):
                ind_objs = map(int, ind_objs)
            # count from 0 (python) or from 1 (fits)?
            if (indexing=='fits'):
                if 0 in ind_objs:
                    warnings.warn('"indexing" was set to "fits" (starts counting from 1) but "obj_rows" contained 0. "indexing" is now automatically set to "python" to avoid errors.')
                    indexing = 'python'
                else:
                    ind_objs = [x-1 for x in ind_objs]
            # connect obj_ids to ind_objs
            obj_ids = get_objids_from_indobjs(fnames, ind_objs, fitsreader)

        # b) test if file
        elif isinstance(ind_objs, str) and os.path.isfile(ind_objs):
            # load the file
            ind_objs = np.loadtxt(obj_rows, dtype='int').tolist()
            # count from 0 (python) or from 1 (fits)?
            if (indexing=='fits'):
                ind_objs = [x-1 for x in ind_objs]
            # connect obj_ids to ind_objs
            obj_ids = get_objids_from_indobjs(fnames, ind_objs, fitsreader)

        # c) test if str
        elif isinstance(ind_objs, str) and not os.path.isfile(ind_objs):
            # cast to list of type int
            ind_objs = [ int(ind_objs) ]
            # count from 0 (python) or from 1 (fits)?
            if (indexing=='fits'):
                if 0 in ind_objs:
                    warnings.warn('"indexing" was set to "fits" (starts counting from 1) but "obj_rows" contained 0. "indexing" is now automatically set to "python" to avoid errors.')
                    indexing = 'python'
                else:
                    ind_objs = [x-1 for x in ind_objs]
            # connect obj_ids to ind_objs
            obj_ids = get_objids_from_indobjs(fnames, ind_objs, fitsreader)

        # d) test if int/float
        elif isinstance(ind_objs, (int, float)):
            # cast to list of type int
            ind_objs = [ int(ind_objs) ]
            # count from 0 (python) or from 1 (fits)?
            if (indexing=='fits'):
                if 0 in ind_objs:
                    warnings.warn('"indexing" was set to "fits" (starts counting from 1) but "obj_rows" contained 0. "indexing" is now automatically set to "python" to avoid errors.')
                    indexing = 'python'
                else:
                    ind_objs = [x-1 for x in ind_objs]
            # connect obj_ids to ind_objs
            obj_ids = get_objids_from_indobjs(fnames, ind_objs, fitsreader)


        # problems:
        else:
#            print '--- Warning: "obj_row" data type not understood. ---'
            error = '"obj_row" data type not understood.'
            sys.exit(error)



    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::: if obj_id and obj_row are both given
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    else:
        error = 'Only use either "obj_id" or "obj_row".'
        sys.exit(error)



    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #:::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    if inputtype is not None:

        #::: typecast to numpy arrays
        obj_ids = np.array(obj_ids)
        ind_objs = np.array(ind_objs)
        
        ind_objs = np.sort(ind_objs)
        obj_ids = np.sort(obj_ids)

    #::: return
    return ind_objs, obj_ids



def get_indobjs_from_objids(fnames, obj_list, fitsreader):

    if fitsreader=='astropy' or fitsreader=='pyfits':
        with pyfits.open(fnames['nights'], mode='denywrite') as hdulist:
            obj_ids_all = hdulist['CATALOGUE'].data['OBJ_ID'].strip()
            del hdulist['CATALOGUE'].data

    elif fitsreader=='fitsio' or fitsreader=='cfitsio':
        with fitsio.FITS(fnames['nights'], vstorage='object') as hdulist:
            obj_ids_all = np.char.strip( hdulist['CATALOGUE'].read(columns='OBJ_ID') )#indices of the candidates

    else: sys.exit('"fitsreader" can only be "astropy"/"pyfits" or "fitsio"/"cfitsio".')

    ind_objs = np.in1d(obj_ids_all, obj_list, assume_unique=True).nonzero()[0]

    #::: check if all obj_ids were read out
    for obj_id in obj_list:
        if obj_id not in obj_ids_all[ind_objs]:
            warnings.warn('obj_id '+str(obj_id)+' not found in fits file.')

    #::: truncate the list of obj_ids, remove obj_ids that are not in fits files
    obj_ids = obj_ids_all[ind_objs]
    del obj_ids_all

    return ind_objs, obj_ids



def get_objids_from_indobjs(fnames, ind_objs, fitsreader):

    if fitsreader=='astropy' or fitsreader=='pyfits':
        with pyfits.open(fnames['nights'], mode='denywrite') as hdulist:
            obj_ids = hdulist['CATALOGUE'].data['OBJ_ID'][ind_objs].strip() #copy.deepcopy( hdulist['CATALOGUE'].data['OBJ_ID'][ind_objs].strip() )
            del hdulist['CATALOGUE'].data

    elif fitsreader=='fitsio' or fitsreader=='cfitsio':
        with fitsio.FITS(fnames['nights'], vstorage='object') as hdulist:
            if isinstance(ind_objs, slice): obj_ids = np.char.strip( hdulist['CATALOGUE'].read(columns='OBJ_ID') ) #copy.deepcopy( hdulist['CATALOGUE'].data['OBJ_ID'][ind_objs].strip() )
            else: obj_ids = np.char.strip( hdulist['CATALOGUE'].read(columns='OBJ_ID', rows=ind_objs) ) #copy.deepcopy( hdulist['CATALOGUE'].data['OBJ_ID'][ind_objs].strip() )

    else: sys.exit('"fitsreader" can only be "astropy"/"pyfits" or "fitsio"/"cfitsio".')

    obj_ids = objid_6digit(obj_ids)


    return obj_ids



def objid_6digit(obj_list):
    for i, obj_id in enumerate(obj_list):
        while len(obj_id)<6:
            obj_id = '0'+obj_id
        obj_list[i] = obj_id

#    formatter = "{:06d}".format
#    map(formatter, obj_list)

    return obj_list




###############################################################################
# Time Input Formatting
###############################################################################

def get_time_inds(fnames, time_index, time_date, time_hjd, time_actionid, fitsreader, silent):

    if time_index is None and time_date is None and time_hjd is None and time_actionid is None:
        ind_time = slice(None)



    elif time_index is not None and time_date is None and time_hjd is None and time_actionid is None:
        # A) test if file
        if isinstance(time_index, str) and os.path.isfile(time_index):
            # load the file
            time_index = np.loadtxt(time_index, dtype='int').tolist()
            # cast to list
            if isinstance(time_index, str):
                time_index = [time_index]

        # B) work with the data

        # if not list, make list
        if not isinstance(time_index, (tuple, list, np.ndarray)):
            ind_time = [time_index]
        else:
            ind_time = time_index



    elif time_index is None and time_date is not None and time_hjd is None and time_actionid is None:

        # A) test if file
        if isinstance(time_date, str) and os.path.isfile(time_date):
            # load the file
            time_date = np.loadtxt(time_date, dtype='S22').tolist()
            # cast to list
            if isinstance(time_date, str):
                time_date = [time_date]

        # B) work with the data
        # a) test if non-empty list
        if isinstance(time_date, (collections.Sequence, np.ndarray)) and not isinstance(time_date, (str, unicode)) and len(time_date) > 0:
            # if list of int or float -> convert to list of str
            if isinstance(time_date[0], (int,float)):
                time_date = map(str, time_date)
            # format if necessary
            if len(time_date[0]) == 8:
                time_date = [ x[0:4]+'-'+x[4:6]+'-'+x[6:] for x in time_date ]
            elif len(time_date[0]) == 10:
                time_date = [ x.replace('/','-') for x in time_date ]
            elif len(time_date[0]) > 10:
                error = '"time_date" format not understood.'
                sys.exit(error)
            # connect to ind_time
            ind_time = get_indtime_from_timedate(fnames, time_date, fitsreader, silent)

        # c) test if int/float
        elif isinstance(time_date, (int, float)):
            # convert to str
            time_date = str(time_date)
            # format
            time_date = time_date[0:4]+'-'+time_date[4:6]+'-'+time_date[6:]
            # connect to ind_time
            ind_time = get_indtime_from_timedate(fnames, time_date, fitsreader, silent)

        # d) test if str
        elif isinstance(time_date, str):

            # if single date, format if necessary
            if len(time_date) == 8:
                time_date = time_date[0:4]+'-'+time_date[4:6]+'-'+time_date[6:]

            # if single date, format if necessary
            elif len(time_date) == 10:
                time_date = time_date.replace('/','-')

            # if dates are given in a range ('20151104:20160101' or '2015-11-04:2016-01-01')
            elif len(time_date) > 10:
                time_date = get_time_date_from_range(time_date)

            else:
                sys.exit('Invalid format of value "time_date". Use e.g. 20151104, "20151104", "2015-11-04" or a textfile name like "dates.txt".')

            # connect to ind_time
            ind_time = get_indtime_from_timedate(fnames, time_date, fitsreader, silent)



    elif time_index is None and time_date is None and time_hjd is not None and time_actionid is None:

        # A) test if file
        if isinstance(time_hjd, str) and os.path.isfile(time_hjd):
            # load the file
            time_hjd = np.loadtxt(time_hjd, dtype='int').tolist()
            # cast to list
            if isinstance(time_hjd, str):
                time_hjd = [time_hjd]

        # B) work with the data
        # a) test if non-empty list
        if isinstance(time_hjd, (collections.Sequence, np.ndarray)) and not isinstance(time_hjd, (str, unicode)) and len(time_hjd) > 0:
            # if list of str or float -> convert to list of int
            if isinstance(time_hjd[0], (str,float)):
                time_hjd = map(int, time_hjd)
            # connect obj_ids to ind_objs
            ind_time = get_indtime_from_timehjd(fnames, time_hjd, fitsreader, silent)

       # b) test if str/int/float
        if isinstance(time_hjd, (str, int, float)):
            time_hjd = int(time_hjd)
            ind_time = get_indtime_from_timehjd(fnames, time_hjd, fitsreader, silent)



    elif time_index is None and time_date is None and time_hjd is None and time_actionid is not None:

       # A) test if file
        if isinstance(time_actionid, str) and os.path.isfile(time_actionid):
            # load the file
            time_actionid = np.loadtxt(time_actionid, dtype='S13').tolist()

        # B) work with the data
        # a) test if non-empty list
        if isinstance(time_actionid, (collections.Sequence, np.ndarray)) and not isinstance(time_actionid, (str, unicode)) and len(time_actionid) > 0:
            # if list of str or float -> convert to list of int
            if isinstance(time_actionid[0], (str,float)):
                time_actionid = map(int, time_actionid)
            # connect to ind_time
            ind_time = get_indtime_from_timeactionid(fnames, time_actionid, fitsreader)

        # c) test if int/float
        elif isinstance(time_actionid, (int, float)):
            # convert to int
            time_actionid = int(time_actionid)
            # connect to ind_time
            ind_time = get_indtime_from_timeactionid(fnames, time_actionid, fitsreader)

        # d) test if str
        elif isinstance(time_actionid, str):

            # if single actioniod, convert to int
            if len(time_actionid) == 6:
                time_actionid = int(time_actionid)

            # if actionids are given in a range ('108583:108600')
            elif len(time_actionid) > 6:
                time_actionid = get_time_actionid_from_range(time_actionid)

            # connect to ind_time
            ind_time = get_indtime_from_timeactionid(fnames, time_actionid, fitsreader)

    else:
        error = 'Only use either "time_index" or "time_date" or "time_hjd" or "time_actionid".'
        sys.exit(error)

    return ind_time



def get_indtime_from_timedate(fnames, time_date, fitsreader, silent):
    

    # if not list, make list
    if not isinstance(time_date, (tuple, list, np.ndarray)):
        time_date = [time_date]


    if fitsreader=='astropy' or fitsreader=='pyfits':
        with pyfits.open(fnames['nights'], mode='denywrite') as hdulist:
            
            #::: SPECULOOS has no DATE-OBS key (=starting date of observations; unlike NGTS), so first need to calculate DATE-OBS
            time_date_all = hdulist['IMAGELIST'].data['JD-OBS']
            time_date_all = Time(time_date_all - 0.5, format='jd', scale='utc', out_subfmt='date').iso
            del hdulist['IMAGELIST'].data

    elif fitsreader=='fitsio' or fitsreader=='cfitsio':
        with fitsio.FITS(fnames['nights'], vstorage='object') as hdulist:
            time_date_all = hdulist['IMAGELIST'].read(columns='JD-OBS')
#            print('****')
#            print(time_date_all)
            time_date_all = Time(time_date_all - 0.5, format='jd', scale='utc', out_subfmt='date').iso

    else: sys.exit('"fitsreader" can only be "astropy"/"pyfits" or "fitsio"/"cfitsio".')

    ind_time = np.in1d(time_date_all, time_date).nonzero()[0]


    #::: check if all dates were found in fits file
    for date in time_date:
        if date not in time_date_all[ind_time]:
            warnings.warn('Date '+ date +' not found in fits file.')

    #::: clean up
    del time_date_all


    return ind_time



def get_indtime_from_timehjd(fnames, time_hjd, fitsreader, silent):
    
    # if not list, make list
    if not isinstance(time_hjd, (tuple, list, np.ndarray)):
        time_hjd = [time_hjd]


    if fitsreader=='astropy' or fitsreader=='pyfits':
        with pyfits.open(fnames['IMAGELIST'], mode='denywrite') as hdulist:
            time_hjd_all = np.int64( hdulist['HJD'].data[0]/3600./24. )
            del hdulist['IMAGELIST'].data

    elif fitsreader=='fitsio' or fitsreader=='cfitsio':
        with fitsio.FITS(fnames['IMAGELIST'], vstorage='object') as hdulist:
            time_hjd_all = np.int64( hdulist['HJD'][0,:]/3600./24. )[0]

    else: sys.exit('"fitsreader" can only be "astropy"/"pyfits" or "fitsio"/"cfitsio".')

    ind_time = np.in1d(time_hjd_all, time_hjd).nonzero()[0]


    #::: check if all dates were found in fits file
    for hjd in time_hjd:
        if hjd not in time_hjd_all[ind_time]:
            if silent is False:
                warnings.warn('Date-HJD '+ str(hjd) +' not found in fits file.')
            else:
                warnings.warn('One ore more Date-HJDs not found in fits file.')
                break

    #::: clean up
    del time_hjd_all


    return ind_time



def get_indtime_from_timeactionid(fnames, time_actionid, fitsreader):

    # if not list, make list
    if not isinstance(time_actionid, (tuple, list, np.ndarray)):
        time_actionid = [time_actionid]


    if fitsreader=='astropy' or fitsreader=='pyfits':
        with pyfits.open(fnames['IMAGELIST'], mode='denywrite') as hdulist:
            time_actionid_all = hdulist['IMAGELIST'].data['ACTIONID']
            del hdulist['IMAGELIST'].data

    elif fitsreader=='fitsio' or fitsreader=='cfitsio':
        with fitsio.FITS(fnames['IMAGELIST'], vstorage='object') as hdulist:
            time_actionid_all = hdulist['IMAGELIST'].read(columns='ACTIONID')

    else: sys.exit('"fitsreader" can only be "astropy"/"pyfits" or "fitsio"/"cfitsio".')

    ind_time = np.in1d(time_actionid_all, time_actionid).nonzero()[0]


    for actionid in time_actionid:
        if actionid not in time_actionid_all[ind_time]:
            warnings.warn('Action-ID '+ str(actionid) +' not found in fits file.')

    del time_actionid_all

    return ind_time



# mother
def get_time_date_from_range(date_range):
    start_date, end_date = solve_range(date_range)

    time_date = []
    start_date, end_date = format_date(start_date, end_date)
    for bufdate in perdelta(start_date, end_date, datetime.timedelta(days=1)):
        time_date.append(bufdate.strftime("%Y-%m-%d"))

    return time_date



# daughter of get_time_date_from_range(date_range)
def format_date(start_date, end_date):
    if isinstance(start_date, int):
        start_date = str(start_date)

    if isinstance(start_date, str):
        if len(start_date) == 8:
            start_date = datetime.datetime.strptime(str(start_date), '%Y%m%d')
        elif len(start_date) == 10:
            start_date.replace('/','-')
            start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')

    if isinstance(end_date, int):
        end_date = str(end_date)

    if isinstance(end_date, str):
        if len(end_date) == 8:
            end_date = datetime.datetime.strptime(str(end_date), '%Y%m%d')
        elif len(end_date) == 10:
            end_date = end_date.replace('/','-')
            end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')

    return start_date, end_date



# daughter of get_time_date_from_range(date_range)
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta



# daughter of
# 1) get_time_date_from_range(date_range)
# 2) get_time_actionid_from_range(actionid_range)
def solve_range(date_range):
    # input:
    # 1) '20151104:20160101' or '2015-11-04:2016-01-01'
    # 2) '108583:108600'
    try:
        start_date, end_date = date_range.split(':')
    except:
        sys.exit('"time_date" data type not understood.')
    return start_date, end_date



# mother
def get_time_actionid_from_range(actionid_range):
    start_actionid, end_actionid = solve_range(actionid_range)
    start_actionid = int(start_actionid)
    end_actionid = int(end_actionid)

    time_actionid = range(start_actionid, end_actionid+1)

    return time_actionid



###############################################################################
# get dictionary with fitsio/pyfits getters
###############################################################################
def get_data(fnames, obj_ids, ind_objs, keys, bls_rank, ind_time, fitsreader):

    #::: check keys
    if isinstance (keys, str): keys = [keys]

    #::: check ind_objs
    if not isinstance(ind_objs, slice) and len(ind_objs) == 0:
        warnings.warn('None of the given objects found in the fits files. Return empty dictionary.')
        dic = {}

    elif not isinstance(ind_time, slice) and len(ind_time) == 0:
        warnings.warn('None of the given objects found in the fits files. Return empty dictionary.')
        dic = {}

    else:

        # in case OBJ_IDs was not part of the keys, add it to have array sizes/indices that are always confirm with the nightly fits files
#        dont_save_obj_id = False
        if 'OBJ_ID' not in keys:
#            dont_save_obj_id = True
            keys.append('OBJ_ID')

        if fitsreader=='astropy' or fitsreader=='pyfits': dic = pyfits_get_data(fnames, obj_ids, ind_objs, keys, bls_rank, ind_time=ind_time)
        elif fitsreader=='fitsio' or fitsreader=='cfitsio': dic = fitsio_get_data(fnames, obj_ids, ind_objs, keys, bls_rank, ind_time=ind_time)
        else: sys.exit('"fitsreader" can only be "astropy"/"pyfits" or "fitsio"/"cfitsio".')


        #TODO: make clear that from now on OBJ_IDs is always part of the dictionary!
        # in case OBJ_IDs was not part of the keys, remove it again
#        if dont_save_obj_id == True:
#            del dic['OBJ_ID']
#            keys.remove('OBJ_ID')


        #TODO: read out dimensions
#        if not isinstance(ind_objs, slice):
#            dic['N_objects'] = np.array( [len(ind_objs)] )
#        else:
#            dic['N_objects'] = np.array( [np.nan] )
#
#        if not isinstance(ind_time, slice):
#            dic['N_times'] = np.array( [len(ind_time)] )
#        else:
#            dic['N_times'] = np.array( [np.nan] )


    return dic, keys



###############################################################################
# pyfits getter
###############################################################################


def pyfits_get_data(fnames, obj_ids, ind_objs, keys, bls_rank, ind_time=slice(None), CCD_bzero=0., CCD_precision=32., CENTD_bzero=0., CENTD_precision=1024.):

    dic = {}
        
    with pyfits.open(fnames['nights'], mode='denywrite') as hdulist:

        #::: CATALOGUE
        hdukey = 'CATALOGUE'
        hdu = hdulist[hdukey].data
        for key in np.intersect1d(hdu.names, keys):
            dic[key] = hdu[key][ind_objs] #copy.deepcopy( hdu[key][ind_objs] )
        del hdu, hdulist[hdukey].data

        #::: IMAGELIST
        hdukey = 'IMAGELIST'
        hdu = hdulist[hdukey].data
        for key in np.intersect1d(hdu.names, keys):
            dic[key] = hdu[key][ind_time] #copy.deepcopy( hdu[key][ind_time] )
        del hdu, hdulist[hdukey].data

        #::: DATA HDUs
        for _, hdukeyinfo in enumerate(hdulist.info(output=False)):
            hdukey = hdukeyinfo[1]
            if hdukey in keys:
                key = hdukey
                dic[key] = hdulist[key].data[ind_objs][:,ind_time] #copy.deepcopy( hdulist[key].data[ind_objs][:,ind_time] )
#                if key in ['CCDX','CCDY']:
#                    dic[key] = (dic[key] + CCD_bzero) / CCD_precision
#                if key in ['CENTDX','CENTDX_ERR','CENTDY','CENTDY_ERR']:
#                    dic[key] = (dic[key] + CENTD_bzero) / CENTD_precision
                del hdulist[key].data

        del hdulist
        

    #::: output as numpy ndarrays
    for key, value in dic.iteritems():
        dic[key] = np.array(value)


    return dic




###############################################################################
# fitsio getter
###############################################################################
def fitsio_get_data(fnames, obj_ids, ind_objs, keys, bls_rank, ind_time=slice(None), CCD_bzero=0., CCD_precision=32., CENTD_bzero=0., CENTD_precision=1024.):

    dic = {}
    
    with fitsio.FITS(fnames['nights'], vstorage='object') as hdulist:

        #::: fitsio does not work with slice arguments, convert to list
        allobjects = False
        if isinstance (ind_objs, slice):
            N_objs = int( hdulist['CATALOGUE'].get_nrows() )
            ind_objs = range(N_objs)
            allobjects = True

        if isinstance (ind_time, slice):
            N_time = int( hdulist['IMAGELIST'].get_nrows() )
            ind_time = range(N_time)


        #::: CATALOGUE
        hdukey = 'CATALOGUE'
        hdunames = hdulist[hdukey].get_colnames()
        subkeys = np.intersect1d(hdunames, keys)
        if subkeys.size!=0:
            data = hdulist[hdukey].read(columns=subkeys, rows=ind_objs)
            if isinstance(subkeys, str): subkeys = [subkeys]
            for key in subkeys:
                dic[key] = data[key] #copy.deepcopy( data[key] )
            del data

        #::: IMAGELIST
        hdukey = 'IMAGELIST'
        hdunames = hdulist[hdukey].get_colnames()
        subkeys = np.intersect1d(hdunames, keys)
        if subkeys.size!=0:
            data = hdulist[hdukey].read(columns=subkeys, rows=ind_time)
            if isinstance(subkeys, str): subkeys = [subkeys]
            for key in subkeys:
                dic[key] = data[key] #copy.deepcopy( data[key] )
            del data

        # TODO: very inefficient - reads out entire image first, then cuts
        # TODO: can only give ind_time in a slice, not just respective dates
        #::: DATA HDUs
        j = 0
        while j!=-1:
            try:
                hdukey = hdulist[j].get_extname()
                if hdukey in keys:
                    key = hdukey

                    #::: read out individual objects (more memory efficient)
                    if allobjects == False:
                        dic[key] = np.zeros(( len(ind_objs), len(ind_time) ))
                        for i, ind_singleobj in enumerate(ind_objs):
                            buf = hdulist[hdukey][slice(ind_singleobj,ind_singleobj+1), slice( ind_time[0], ind_time[-1]+1)]
                            #::: select the wished times only (if some times within the slice are not wished for)
                            if buf.shape[1] != len(ind_time):
                                ind_timeX = [x - ind_time[0] for x in ind_time]
                                buf = buf[:,ind_timeX]
                            dic[key][i,:] = buf
                        del buf

                    #::: read out all objects at once
                    else:
                        buf = hdulist[hdukey][:, slice( ind_time[0], ind_time[-1]+1)]
                        if buf.shape[1] != len(ind_time):
                            ind_timeX = [x - ind_time[0] for x in ind_time]
                            buf = buf[:,ind_timeX]
                        dic[key] = buf
                        del buf

#                    if key in ['CCDX','CCDY']:
#                        dic[key] = (dic[key] + CCD_bzero) / CCD_precision
#                    if key in ['CENTDX','CENTDX_ERR','CENTDY','CENTDY_ERR']:
#                        dic[key] = (dic[key] + CENTD_bzero) / CENTD_precision
                j += 1
            except:
                break

    return dic



###############################################################################
# Simplify output if only one object is retrieved
###############################################################################
def simplify_dic(dic):

    for key, value in dic.iteritems():
        try:
            if value.shape[0] == 1:
                dic[key] = value[0]
            elif (len(value.shape) > 1) and (value.shape[1] == 1):
                dic[key] = value[:,0]
        except AttributeError:
            pass
    return dic



###############################################################################
# Set flagged values to nan
###############################################################################
def set_nan_dic(dic):
    if len(dic['OBJ_ID']) == 1:
        dic = set_nan_single(dic)
    elif len(dic['OBJ_ID']) > 1:
        dic = set_nan_multi(dic)
    return dic


#::: if only 1 object is contained in dic
def set_nan_single(dic):
    ###### REMOVE BROKEN ITEMS #######
    #::: nan
    ind_broken = np.where( dic['FLAGS'] > 0 ) #(dic[key] == 0.) | 
#    if key in dic: dic[key][ind_broken] = np.nan
#    dic['HJD'][ind_broken] = np.nan #this is not allowed to be set to nan!!! Otherwise the binning will be messed up!!!
    for key in ['FLUX','FLUX_ERR','FLUX3','FLUX3_ERR', 
                'FLUX4','FLUX4_ERR','FLUX5','FLUX5_ERR',
                'SYSREM_FLUX3','SYSREM_FLUX3_ERR',
                'DECORR_FLUX3','DECORR_FLUX3_ERR',
                'CCDX','CCDX_ERR','CCDY','CCDY_ERR',
                'CENTDX','CENTDX_ERR','CENTDY','CENTDY_ERR']:
        if key in dic: 
            dic[key][ind_broken] = np.nan
    return dic


#::: if multiple objects are contained in dic
def set_nan_multi(dic):
    ###### REMOVE BROKEN ITEMS #######
    #::: nan
    N_obj = dic['FLAGS'].shape[0]
    for obj_nr in range(N_obj):
        ind_broken = np.where( dic['FLAGS'][obj_nr] > 0 )
#        if key in dic: dic[key][obj_nr,ind_broken] = np.nan
#    #    dic['HJD'][ind_broken] = np.nan #this is not allowed to be set to nan!!! Otherwise the binning will be messed up!!!
#        if 'CCDX' in dic: dic['CCDX'][obj_nr,ind_broken] = np.nan
#        if 'CCDY' in dic: dic['CCDY'][obj_nr,ind_broken] = np.nan
#        if 'CENTDX' in dic: dic['CENTDX'][obj_nr,ind_broken] = np.nan
#        if 'CENTDY' in dic: dic['CENTDY'][obj_nr,ind_broken] = np.nan    
        for key in ['FLUX','FLUX_ERR','FLUX3','FLUX3_ERR', 
                'FLUX4','FLUX4_ERR','FLUX5','FLUX5_ERR',
                'SYSREM_FLUX3','SYSREM_FLUX3_ERR',
                'DECORR_FLUX3','DECORR_FLUX3_ERR',
                'CCDX','CCDX_ERR','CCDY','CCDY_ERR',
                'CENTDX','CENTDX_ERR','CENTDY','CENTDY_ERR']:
            if key in dic: 
                dic[key][obj_nr,ind_broken] = np.nan
    return dic





###############################################################################
# Check if all keys are retrieved
###############################################################################
def check_dic(dic, keys, silent):

    if not silent: print('###############################################################################')

    fail = False

    for key in keys:
        if key not in dic:
            print('Failure: key',key,'not read into dictionary.')
            fail = True

    if fail == False:
        if not silent: print('Success: All keys successfully read into dictionary.')

    if not silent: print('###############################################################################')

    return




###############################################################################
# Check which keys are available
###############################################################################
def get_available_keys(telescope, field_name, filter_band, root=None, roots=None, fnames=None, silent=True):    
    
    if (roots is None) and (fnames is None):
        roots = standard_roots(telescope, root, silent)
    
    if fnames is None: 
        fnames = standard_fnames(telescope, field_name, filter_band, roots, silent)
    
    if fnames is not None:
        with pyfits.open(fnames['nights'], mode='denywrite') as hdulist:                
            hdukeys = [ hdukeyinfo[1] for _, hdukeyinfo in enumerate(hdulist.info(output=False)) ]
            keys_imagelist = hdulist['IMAGELIST'].data.names
            keys_catalogue = hdulist['CATALOGUE'].data.names
    
    return hdukeys + keys_imagelist + keys_catalogue
    
    



###############################################################################
# Check on which nights which targets were observed
###############################################################################
def get_observing_log(): 
    import pandas as pd
    from tqdm import tqdm
    
    #::: on laptop (OS X)
    if sys.platform == "darwin":
        files = [ f for tel in ['Io','Europe','Callisto','Ganymede'] for f in glob.glob('/Users/mx/Big_Data/BIG_DATA_SPECULOOS/{tel}/callisto_pipeline_output/20*/*/*_output.fts'.format(tel=tel)) ]    
    
    #::: on Cambridge servers
    elif 'ra.phy.cam.ac.uk' in socket.gethostname():
        files = [ f for tel in ['Io','Europe','Callisto','Ganymede'] for f in glob.glob('/appcg/data2/SPECULOOSPipeline/{tel}/output/20*/*/*_output.fts'.format(tel=tel)) ]    
    
    dic = {}
    dic['telescope'] = [ f.split('/')[-5] for f in files ]
    dic['date'] = [ os.path.basename(f).split('_')[0] for f in files ]
    dic['field_name'] = [ os.path.basename(f).split('_')[1] for f in files ]
    dic['filter_band'] = [ os.path.basename(f).split('_')[2] for f in files ]
    dic['N_images'] = np.zeros(len(files))
    dic['exposure'] = np.zeros(len(files))
    dic['N_hours'] = np.zeros(len(files))
    
    for i,f in tqdm( enumerate(files), total=len(files) ):
        try:
            with pyfits.open(f, mode='denywrite') as hdulist:
                dic['N_images'][i] = len( hdulist['IMAGELIST'].data )
                dic['exposure'][i] = np.round( 100*np.nanmean( hdulist['IMAGELIST'].data['EXPOSURE'] ) )/100.
                dic['N_hours'][i] = np.round( 100*dic['N_images'][i] * dic['exposure'][i] / 3600. ) /100.
        except:
            pass
    
    df = pd.DataFrame(dic)
    df = df[ ['date', 'telescope', 'field_name', 'filter_band', 'exposure', 'N_images', 'N_hours'] ]
    df['date']=pd.to_datetime(df.date)
    df = df.sort_values(by='date') 
    df = df.reset_index(drop=True)
    
    return df