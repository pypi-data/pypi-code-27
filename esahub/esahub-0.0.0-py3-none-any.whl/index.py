# coding=utf-8
""" This module contains the functionality to extract the metadata
    from a Satellite archive, construct from that the relevant
    Solr index and post the index to a running Solr instance.
"""
from __future__ import print_function
import glob, sys, os, time, fnmatch, traceback, shutil
import re
import gc
import datetime as DT
import zipfile, tarfile
import multiprocessing
import subprocess
import lxml.etree as ET
import logginßg
import tempfile
from functools import partial
import pysolr
import json
from netCDF4 import Dataset
import numpy as np
from . import geo, helpers, tty, checksum
from .config import CONFIG

logger = logging.getLogger('evdc')
PY2 = sys.version_info < (3, 0)

if PY2:
    from StringIO import StringIO
else:
    from io import StringIO, BytesIO


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def exists(product, where='solr'):
    """Check if a product is already indexed.

    Parameters
    ----------
    product : str
        Filename of the product to be indexed.
    where : str, optional
        If 'solr', check if the product exists on the Solr index.
        If 'local', check if the extracted metadata exists in the local data
        directory. (default: 'solr')

    Returns
    -------
    bool
        True if the product is already indexed, False otherwise.
    """
    product = os.path.split(product)[1]
    if where == 'solr':
        return (count(q='product_name:{}*'.format(
                    os.path.splitext(product)[0])) > 0)
    elif where == 'local':
        stripped_product_path = os.path.join(CONFIG['GENERAL']['DATA_DIR'],
                                             product)
        if os.path.splitext(stripped_product_path)[1] != '.zip':
            stripped_product_path += '.zip'
        return os.path.isfile(stripped_product_path)


def index(product, is_data=True, store=False, queue=None):
    """Extract the metadata from a single satellite product.

    Parameters
    ----------
    product : str
        Filename of the product to be indexed.
    is_data : bool, optional
        If True, compute md5 sum and file size from the file. Ingestiondate is
        current timestamp. Otherwise, get info from S3 storage.
    store : bool, optional
        If True, store the stripped metadata in
        `config.CONFIG['GENERAL']['DATA_DIR']` (default: False).
    queue : multiprocessing.Manager.Queue, optional
        A multiprocessing queue to submit status messages.

    Returns
    -------
    dict
        If successful, returns a dictionary of the extracted metadata.
        Otherwise returns None.
    """
    product_path, product_file = os.path.split(product)
    identifier = os.path.splitext(product_file)[0]
    satellite = helpers.get_satellite(product)

    try:
        if satellite in ['S1A', 'S1B', 'S2A', 'S2B', 'S3A']:
            DATA = _index_S123(product)
        elif satellite == 'S5P':
            DATA = _index_S5(product)
        elif satellite == 'AE':
            DATA = _index_AE(product)
        else:
            return {}

    except Exception as e:
        msg = 'Could not extract metadata from {}: {}'.format(product, e)
        if queue is None:
            tty.update(product_file, msg)
        else:
            queue.put((product_file,msg))
        logging.info(msg)
        traceback.print_exc(file=sys.stderr)
        return {}

    #
    # Add a number of custom properties.
    #

    # Compute the area covered.
    if 'footprint' in DATA:
        # DATA['area_sqkm'] = '{:.2f}'.format(geo.polygon_area(DATA['footprint']))
        DATA['area_sqkm'] = geo.polygon_area(DATA['footprint'])

    if is_data:
        #
        # If the file is the actual product, compute additional metadata such
        # as the md5 sum and the file size from the file itself.
        #
        DATA['inventory_time'] = DT.datetime.strftime(DT.datetime.now(),
                                                      '%Y-%m-%dT%H:%M:%SZ')
        # DATA['inventory_time'] = DT.datetime.now()
        # Add the md5 checksum to metadata
        DATA['md5'] = checksum.md5(product)
        # Add the file size to metadata
        DATA['bytes'] = os.path.getsize(product)

    else:
        #
        # If the file is only the stripped metadata, obtain additional metadata
        # from other source.
        #
        pass
        # if not 'md5' in DATA or not 'bytes' in DATA or not 'inventory_time' in DATA:
        #     s3_info = storage.s3_ls(identifier)
        #     if len(s3_info) == 1:
        #         DATA['inventory_time'] = DT.datetime.strftime(s3_info[0]['time'],'%Y-%m-%dT%H:%M:%SZ')
        #         # DATA['inventory_time'] = s3_info[0]['time']
        #         DATA['md5'] = s3_info[0]['md5']
        #         DATA['bytes'] = s3_info[0]['size']

    # Store a stripped copy
    if store:
        evdc_meta = {_: DATA[_] for _ in ['md5', 'bytes', 'inventory_time']}
        strip(product, target=CONFIG['GENERAL']['DATA_DIR'], data=evdc_meta)

    return DATA


def _index_S123(product):
    """Extract the metadata from a Sentinel-1,2,3 product.

    Parameters
    ----------
    product : str
        The full file path of a Sentinel-1,2,3 product (zip-archive).

    Returns
    -------
    dict
        A dictionary of the extracted metadata.
    """
    product_path, product_file = os.path.split(product)
    DATA = {}
    #
    # Decide which satellite the zip belongs to:
    # S1, S2, S3
    #
    satellite = helpers.get_satellite(product_file)
    suffix = CONFIG['SATELLITES'][satellite]['suffix']
    identifier = os.path.splitext(product_file)[0]
    with zipfile.ZipFile(product, 'r') as zip_ref:
        for meta_data_file, meta in CONFIG['META'][CONFIG['SATELLITES'][satellite]['meta']].items():
            zpath = os.path.join(identifier+suffix, meta_data_file)
            # Treat the specified filename as a regular expression.
            zfiles = [zfile for zfile in zip_ref.namelist() if re.search(zpath,zfile)]
            for zfile in zfiles:
                root = ET.fromstring( zip_ref.read(zfile) )
                pre = CONFIG['META_NAMESPACES'].copy()
                pre.update(root.nsmap)

                #
                # Some satellite specific things
                #
                if satellite == 'S3A':
                    INSTR = root.find("./metadataSection/metadataObject[@ID='platform']//sentinel-safe:instrument/sentinel-safe:familyName", pre).attrib['abbreviation'].lower()
                else:
                    INSTR = ''

                #
                # Loop through the specified meta data entries for the given file.
                # Find the entry in the document and append the property to the
                # DATA dictionary.
                #
                for key,item in meta.items():
                    try:
                        xml_path = item[0].format(INSTR=INSTR)
                        if item[1] == 'text':
                            val = root.find(xml_path, pre).text
                        else:
                            val = root.find(xml_path, pre).attrib[item[1]]
                        if len(item) == 3:
                            conversion_fn = eval(item[2])
                            val = conversion_fn(val)
                    except Exception as e:
                        #
                        # This entry doesn't exist. Move on.
                        #
                        pass
                    else:
                        DATA[key] = val
        #
        # Extract additional metadata stored with the file
        # (e.g. during dat stripping).
        #
        root = os.path.commonprefix(zip_ref.namelist())
        evdc_meta_file = os.path.join(root, '.evdc_meta')
        if evdc_meta_file in zip_ref.namelist():
            json_str = zip_ref.read(evdc_meta_file)
            if not PY2:
                json_str = json_str.decode()
            evdc_meta = json.loads(json_str)
            DATA.update(evdc_meta)

    #
    # On Sentinel-2, the manifest.safe file specifies familyName as SENTINEL
    # Since we want to be able to query for mission, make this more specific.
    #
    if satellite.startswith('S1'):
        DATA['family_name'] = 'Sentinel-1'
    elif satellite.startswith('S2'):
        DATA['family_name'] = 'Sentinel-2'

    DATA['product_name'] = identifier + suffix

    return DATA


def _index_AE(product):
    """Extract the metadata from an ADM-AEOLUS product.

    Parameters
    ----------
    product : str
        The full file path of an ADM-AEOLUS product (tgz-archive).

    Returns
    -------
    dict
        A dictionary of the extracted metadata.
    """
    product_path, product_file = os.path.split(product)
    identifier = os.path.splitext(product_file)[0]
    satellite = 'AE'
    suffix = CONFIG['SATELLITES'][satellite]['suffix']
    DATA = {}
    with tarfile.open(product, 'r') as tar_ref:
        rootdir = os.path.commonprefix([os.path.split(_)[0] for _ in tar_ref.getnames()])
        for meta_data_file, meta in CONFIG['META'][CONFIG['SATELLITES'][satellite]['meta']].items():
            tpath = os.path.join(rootdir, meta_data_file)
            # Treat the specified filename as a regular expression.
            tfiles = [tfile for tfile in tar_ref.getnames() if re.search(tpath,tfile) and not os.path.split(tfile)[1].startswith('.')]
            for tfile in tfiles:
                tfile_object = tar_ref.extractfile(tfile)
                root = ET.fromstring( tfile_object.read() )
                tfile_object.close()
                pre = CONFIG['META_NAMESPACES'].copy()
                pre.update(root.nsmap)

                #
                # Loop through the specified meta data entries for the given file.
                # Find the entry in the document and append the property to the
                # DATA dictionary.
                #
                for key,item in meta.items():
                    try:
                        xml_path = item[0]
                        if item[1] == 'text':
                            val = root.find(xml_path, pre).text
                        else:
                            val = root.find(xml_path, pre).attrib[item[1]]
                        if len(item) == 3:
                            conversion_fn = eval(item[2])
                            val = conversion_fn(val)
                    except Exception as e:
                        #
                        # This entry doesn't exist. Move on.
                        #
                        pass
                    else:
                        DATA[key] = val
        #
        # Extract additional metadata stored with the file
        # (e.g. during data stripping).
        #
        evdc_meta_file = os.path.join(rootdir, '.evdc_meta')
        if evdc_meta_file in tar_ref.getnames():
            fobj = tar_ref.extractfile(evdc_meta_file)
            json_str = fobj.read()
            fobj.close()
            if not PY2:
                json_str = json_str.decode()
            evdc_meta = json.loads(json_str)
            DATA.update(evdc_meta)

    DATA['product_name'] = identifier + suffix

    if 'latstart' in DATA and 'lonstart' in DATA and 'latstop' in DATA and 'lonstop' in DATA:
        ymin=int(DATA['latstart'])/1.e6
        xmin=int(DATA['lonstart'])/1.e6
        ymax=int(DATA['latstop'])/1.e6
        xmax=int(DATA['lonstop'])/1.e6
        if xmax > 180: xmax -= 360
        if xmin > 180: xmin -= 360
        DATA['footprint'] = 'POLYGON(({xmin} {ymin},{xmin} {ymax},{xmax} {ymax},{xmax} {ymin},{xmin} {ymin}))'.format(
            ymin=ymin, xmin=xmin, ymax=ymax, xmax=xmax
        )
        del DATA['latstart'], DATA['lonstart'], DATA['latstop'], DATA['lonstop']

    return DATA


def ncget(nc_fid, path):
    """Return metadata attribute from netCDF file.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        An opened netCDF Dataset.
    path : str
        The path to the metadata attribute. Consists of nested groups and the attribute separated
        by slashes:
        `group/subgroup/.../[attribute]`

    Returns
    -------
    str
        The value of the requested attribute. If no attribute is specified (i.e. the path ends
        with a slash), the last subgroup is returned.
    """
    group = nc_fid
    path_elements = path.split('/')
    groups = path_elements[:-1]
    attr = path_elements[-1]
    for _ in groups: group = group.groups[_]
    if len(attr) == 0:
        return group
    else:
        value = group.getncattr(attr)
        if isinstance(value, np.integer):
            # There are problems with JSON-serializing numpy integers,
            # therefore convert to native int:
            value = int(value)
        return value


def _index_S5(product):
    """Extract the metadata from a Sentinel-5P product.

    Parameters
    ----------
    product : str
        The full file path of a Sentinel-5P product (netCDF file).

    Returns
    -------
    dict
        A dictionary of the extracted metadata.
    """
    product_path, product_file = os.path.split(product)
    DATA = {}
    satellite = product_file[:3]

    # If the product is a zip archive, extract to temporary directory
    if os.path.splitext(product_file)[1] == '.zip':
        compressed = True
        tmpdir = tempfile.mkdtemp()
        z = zipfile.ZipFile(product,'r')
        product = z.extract(z.namelist()[0], tmpdir)
    else:
        compressed = False

    nc_fid = Dataset(product, 'r')

    for key,item in CONFIG['META'][CONFIG['SATELLITES'][satellite]['meta']].items():
        try:
            if len(item)==1:
                DATA[key] = ncget(nc_fid, item[0])
            elif len(item)==2:
                conversion_fn = eval(item[1])
                DATA[key] = conversion_fn(ncget(nc_fid, item[0]))
        except Exception as e:
            pass

    #
    # Extract additional metadata stored with the file
    # (e.g. during dat stripping).
    #
    if 'EVDC_META' in nc_fid.groups:
        meta_group = nc_fid.groups['EVDC_META']
        evdc_meta = {_ : ncget(meta_group,_) for _ in meta_group.ncattrs()}
        DATA.update(evdc_meta)

    nc_fid.close()
    gc.collect()

    if compressed: shutil.rmtree(tmpdir)

    return DATA


def strip(product, target, compress=True, data=None):
    """Create a stripped down copy of the satellite product that only contains the metadata.

    Parameters
    ----------
    product : str
        The full file path of a Sentinel product.
    target : str, optional
        The directory to store the stripped down product.
    compress : bool, optional
        If True, compress bare netCDF files in a zip archive (default: True)
    data : dict, optional
        Additional metadata to be stored. This will typically be the md5 checksum and filesize.

    Returns
    -------
    str
        If successful, the file path of the stripped copy. False otherwise.
    """
    satellite = helpers.get_satellite(product)
    if satellite in ['S1A', 'S1B', 'S2A', 'S2B', 'S3A']:
        return _strip_S123(product, target, data=data)
    elif satellite == 'S5P':
        return _strip_S5(product, target, compress, data=data)
    elif satellite == 'AE':
        return _strip_AE(product, target, data=data)
    else:
        return False


def _strip_S123(product, target, data):
    """Create a stripped down copy of the Sentinel-1,2,3 product that only contains the metadata.

    Parameters
    ----------
    product : str
        The full file path of a Sentinel-1,2,3 product.
    target : str, optional
        The directory to store the stripped down product.
    data : dict, optional
        Additional metadata to be stored. This will typically be the md5 checksum and filesize.

    Returns
    -------
    str
        If successful, the file path of the stripped copy. False otherwise.
    """

    product_path, product_file = os.path.split(product)
    satellite = helpers.get_satellite(product)
    stripped_product_path = os.path.join( target, product_file )

    with zipfile.ZipFile(stripped_product_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_stripped:
        with zipfile.ZipFile(product, 'r') as zip_original:
            root = os.path.commonprefix(zip_original.namelist())
            for meta_data_file in CONFIG['META'][CONFIG['SATELLITES'][satellite]['meta']]:
                zpath = os.path.join(root, meta_data_file)
                # Treat the specified filename as a regular expression.
                zfiles = [zfile for zfile in zip_original.namelist() if re.search(zpath,zfile)]
                for zfile in zfiles:
                    # Add file to new zip archive
                    zip_stripped.writestr(zfile, zip_original.read(zfile))

            #
            # Add additional metadata to zip archive
            #
            if data is not None:
                jsondata = json.dumps(data)
                zip_stripped.writestr(os.path.join(root, '.evdc_meta'), jsondata)

    return stripped_product_path


def _strip_AE(product, target, data):
    """Create a stripped down copy of the ADM-AEOLUS product that only contains the metadata.

    Parameters
    ----------
    product : str
        The full file path of an ADM-AEOLUS product.
    target : str, optional
        The directory to store the stripped down product.
    data : dict, optional
        Additional metadata to be stored. This will typically be the md5 checksum and filesize.

    Returns
    -------
    str
        If successful, the file path of the stripped copy. False otherwise.
    """

    product_path, product_file = os.path.split(product)
    satellite = helpers.get_satellite(product)
    stripped_product_path = os.path.join( target, product_file )

    with tarfile.open(stripped_product_path, 'w') as tar_stripped:
        with tarfile.open(product, 'r') as tar_original:
            root = os.path.commonprefix(tar_original.getnames())
            for meta_data_file in CONFIG['META'][CONFIG['SATELLITES'][satellite]['meta']]:
                tpath = os.path.join(root, meta_data_file)
                # Treat the specified filename as a regular expression.
                tfiles = [tfile for tfile in tar_original.getnames() if re.search(tpath,tfile) and not os.path.split(tfile)[1].startswith('.')]
                for tfile in tfiles:
                    # Add file to new tar archive
                    fobj = tar_original.extractfile(tfile)
                    tar_stripped.addfile(tar_original.getmember(tfile), fobj)
                    fobj.close()

            #
            # Add additional metadata to tar archive
            #
            if data is not None:
                jsondata = json.dumps(data).encode('utf-8')
                tfile = os.path.join(root, '.evdc_meta')
                tinfo = tarfile.TarInfo(tfile)
                fobj = BytesIO(jsondata)
                tinfo.size = len(jsondata)
                tar_stripped.addfile(tinfo, fobj)

    return stripped_product_path


def _strip_S5(product, target, compress, data=None):
    """Create a stripped down copy of the Sentinel-5 product that only contains the metadata.

    Parameters
    ----------
    product : str
        The full file path of a Sentinel-5 product.
    target : str
        The directory to store the stripped down product.
    compress : bool
        If True, compress the stripped product in a zip archive.
    data : dict, optional
        Additional metadata to be stored. This will typically be the md5 checksum and filesize.

    Returns
    -------
    str
        If successful, the file path of the (compressed) stripped copy. False otherwise.
    """
    product_path, product_file = os.path.split(product)

    if compress:
        stripped_product_path = tempfile.mkstemp()[1]
    else:
        stripped_product_path = os.path.join( target, product_file )

    try:
        nc_fid = Dataset(product, 'r')
        nc_stripped = Dataset(stripped_product_path, 'w')
    except:
        print(product)
        traceback.print_exc(file=sys.stderr)
        return False

    def _copy(src,tgt):
        # Set attributes
        tgt.setncatts({_:src.getncattr(_) for _ in src.ncattrs()})
        # Recursively go through groups
        for src_group_name,src_group in src.groups.items():
            tgt_group = tgt.createGroup(src_group_name)
            _copy(src_group, tgt_group)

    _copy(nc_fid, nc_stripped)

    #
    # Add additional metadata to zip archive
    #
    if data is not None:
        meta_group = nc_stripped.createGroup('EVDC_META')
        meta_group.setncatts(data)

    nc_stripped.close()

    if compress:
        zipped_stripped_product_path = os.path.join( target, product_file + '.zip' )
        with zipfile.ZipFile(zipped_stripped_product_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_stripped:
            zip_stripped.write(stripped_product_path)
        os.remove(stripped_product_path)
        return zipped_stripped_product_path
    else:
        return stripped_product_path


COUNT = 0
def _count(boolean,total=None):
    global COUNT
    if boolean: COUNT += 1
    if total is not None: tty.set_progress(COUNT,total)

COLLECT = []


def _init_collect():
    global COLLECT, COUNT
    COLLECT = []
    COUNT = 0


def _collect(result,total=None):
    global COLLECT, COUNT
    COLLECT.append(result)
    COUNT += 1
    if total is not None: tty.set_progress(COUNT,total)


def index_all(directory, is_data=True, store=False, daily=False, subset=None):
    """Generate the index for all satellite products in the data directory.

    Parameters
    ----------
    directory : str
        The directory containing the products to be indexed.
    is_data : bool, optional
        If True, compute md5 sum and file size from the file. Otherwise, get info from S3 storage.
    store : bool, optional
        If True, store the stripped metadata in `config.CONFIG['GENERAL']['DATA_DIR']`
        (default: False).
    daily : bool, optional
        Whether to only index products that were added since yesterday.
    subset : list of str, optional
        A list of filenames to be indexed.

    Returns
    -------
    list of dict
        A list of the metadata dictonary of each satellite product in the directory.
    """
    start_time = time.time()

    #
    # Get a list of all products in directory.
    #
    products = helpers.ls(directory, subset=subset)

    if daily:
        # Only index products that were modified after yesterday midnight.
        yesterday = DT.datetime.combine(DT.date.today() - DT.timedelta(1), DT.datetime.min.time())
        products = [_ for _ in products if DT.datetime.fromtimestamp(os.path.getmtime(_)) > yesterday]

    #
    # Index all products found (multiprocessing).
    #
    msg = 'Indexing {:d} products... '.format(len(products))
    tty.status(msg)

    q = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(processes=CONFIG['GENERAL']['N_PROC'])

    _init_collect()
    _collect_metadata = partial(_collect, total=len(products))
    _index_fn = partial(index, is_data=is_data, store=store)

    for product in products:
        pool.apply_async(_index_fn, (product,), callback=_collect_metadata)

    pool.close()
    pool.join()

    stop_time = time.time()

    msg = 'Indexing {:d} products... ({:.1f}s)'.format(len(products), stop_time-start_time)
    logging.info(msg)
    tty.status(msg)

    return COLLECT


def commit(data, quiet=False):
    """Feeds data into the running Solr instance.

    Parameters
    ----------
    data : dict or list of dict
        The data is directly piped into Solr.
    quiet : bool, optional
        Whether to suppress output.

    Returns
    -------
    str
        The Solr output.
    """
    solr = pysolr.Solr( os.path.join(CONFIG['GENERAL']['SOLR_URL'], CONFIG['GENERAL']['SOLR_CORE']) )

    if type(data) is dict: data = [data]

    if not quiet:
        msg = 'Posting {} documents to Solr core {}...'.format(len(data), CONFIG['GENERAL']['SOLR_CORE'])
        tty.status(msg)
    start_time = time.time()
    try:
        result = None
        for chunk in helpers.chunks(data, 1000):
            result = solr.add(chunk)
    except Exception as e:
        logging.error('Could not add documents to Solr: {}'.format(e))
        return e
    else:
        stop_time = time.time()
        if not quiet:
            msg = 'Posting {} documents to Solr core {}... done. ({:.1f}s)'.format(len(data), CONFIG['GENERAL']['SOLR_CORE'], stop_time-start_time)
            logging.info(msg)
            tty.status(msg)
    finally:
        solr.get_session().close()

    return result


def _wipe():
    """Wipes the entire index. Use with caution."""
    solr = pysolr.Solr( os.path.join(CONFIG['GENERAL']['SOLR_URL'], CONFIG['GENERAL']['SOLR_CORE']), timeout=10 )
    solr.delete(q='*:*')
    solr.get_session().close()


def count(q='*:*'):
    """Returns the number of documents in the Solr index matching a query.

    Parameters
    ----------
    q : str, optional
        Solr query string (default: '*:*').

    Returns
    -------
    int
        The number of documents found.
    """
    solr = pysolr.Solr( os.path.join(CONFIG['GENERAL']['SOLR_URL'], CONFIG['GENERAL']['SOLR_CORE']), timeout=10 )
    result = solr.search(q)
    solr.get_session().close()
    return result.hits


def search(*args, **kwargs):
    """Returns documents from the Solr index. Follows the Syntax of pysolr.Solr.search()."""
    solr = pysolr.Solr( os.path.join(CONFIG['GENERAL']['SOLR_URL'], CONFIG['GENERAL']['SOLR_CORE']), timeout=10 )
    result = solr.search(*args, **kwargs)
    solr.get_session().close()
    return result
