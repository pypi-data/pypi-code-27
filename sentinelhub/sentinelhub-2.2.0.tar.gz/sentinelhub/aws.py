"""
Module for obtaining data from Amazon Web Service
"""

from abc import ABC, abstractmethod
import logging
import os.path

from .download import DownloadRequest, get_json, AwsDownloadFailedException
from .opensearch import get_tile_info, get_tile_info_id
from .time_utils import parse_time
from .config import SHConfig
from .constants import AwsConstants, EsaSafeType, MimeType, DataSource


LOGGER = logging.getLogger(__name__)


class AwsService(ABC):
    """ Amazon Web Service (AWS) base class

    :param parent_folder: Folder where the fetched data will be saved.
    :type parent_folder: str
    :param bands: List of Sentinel-2 bands for request. If parameter is set to ``None`` all bands will be used.
    :type bands: list(str) or None
    :param metafiles: List of additional metafiles available on AWS
                      (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``).
                      If parameter is set to ``None`` the list will be set automatically.
    :type metafiles: list(str) or None
    """
    def __init__(self, parent_folder='', bands=None, metafiles=None):
        self.parent_folder = parent_folder
        self.bands = self._parse_bands(bands)
        self.metafiles = self._parse_metafiles(metafiles)

        self.download_list = []
        self.folder_list = []

        self.base_url = self.get_base_url()
        self.base_http_url = self.get_base_url(force_http=True)

    @abstractmethod
    def get_requests(self):
        raise NotImplementedError

    def _parse_bands(self, band_input):
        """
        Parses class input and verifies band names.

        :param band_input: input parameter `bands`
        :type band_input: str or list(str) or None
        :return: verified list of bands
        :rtype: list(str)
        """
        all_bands = AwsConstants.S2_L1C_BANDS if self.data_source is DataSource.SENTINEL2_L1C else \
            AwsConstants.S2_L2A_BANDS

        if band_input is None:
            return all_bands
        if isinstance(band_input, str):
            band_list = band_input.split(',')
        elif isinstance(band_input, list):
            band_list = band_input.copy()
        else:
            raise ValueError('bands parameter must be a list or a string')
        band_list = [band.strip().split('.')[0] for band in band_list]
        band_list = [band for band in band_list if band != '']
        if not set(band_list) <= set(all_bands):
            raise ValueError('bands {} must be a subset of {}'.format(band_list, all_bands))
        return band_list

    def _parse_metafiles(self, metafile_input):
        """
        Parses class input and verifies metadata file names.

        :param metafile_input: class input parameter `metafiles`
        :type metafile_input: str or list(str) or None
        :return: verified list of metadata files
        :rtype: list(str)
        """
        all_metafiles = AwsConstants.S2_L1C_METAFILES if self.data_source is DataSource.SENTINEL2_L1C else \
            AwsConstants.S2_L2A_METAFILES

        if metafile_input is None:
            if self.__class__.__name__ == 'SafeProduct':
                return all_metafiles
            elif self.__class__.__name__ == 'SafeTile':
                return [metafile for metafile in all_metafiles if metafile in AwsConstants.TILE_FILES]
            return []
        if isinstance(metafile_input, str):
            metafile_list = metafile_input.split(',')
        elif isinstance(metafile_input, list):
            metafile_list = metafile_input.copy()
        else:
            raise ValueError('metafiles parameter must be a list or a string')
        metafile_list = [metafile.strip().split('.')[0] for metafile in metafile_list]
        metafile_list = [metafile for metafile in metafile_list if metafile != '']
        if not set(metafile_list) <= set(all_metafiles):
            raise ValueError('metadata files {} must be a subset of {}'.format(metafile_list, all_metafiles))
        return metafile_list

    def get_base_url(self, force_http=False):
        """ Creates base URL path

        :param force_http: True if HTTP base URL for Sentinel-2 L1C should be used and False otherwise
        :type force_http: str
        :return: base url string
        :rtype: str
        """
        if self.data_source is DataSource.SENTINEL2_L1C:
            if SHConfig().use_s3_l1c_bucket and not force_http:
                return 's3://{}/'.format(SHConfig().aws_s3_l1c_bucket)
            return SHConfig().aws_base_url
        return 's3://{}/'.format(SHConfig().aws_s3_l2a_bucket)

    def get_safe_type(self):
        """Determines the type of ESA product.

        In 2016 ESA changed structure and naming of data. Therefore the class must
        distinguish between old product type and compact (new) product type.

        :return: type of ESA product
        :rtype: constants.EsaSafeType
        :raises: ValueError
        """
        product_type = self.product_id.split('_')[1]
        if product_type.startswith('MSI'):
            return EsaSafeType.COMPACT_TYPE
        if product_type in ['OPER', 'USER']:
            return EsaSafeType.OLD_TYPE
        raise ValueError('Unrecognized product type of product id {}'.format(self.product_id))

    def get_baseline(self):
        """ Determines the baseline number (i.e. version) of ESA .SAFE product

        :return: baseline number
        :rtype: str
        :raises: ValueError
        """
        if self.safe_type is EsaSafeType.COMPACT_TYPE:
            baseline = self.product_id.split('_')[3].lstrip('N')
            if len(baseline) != 4:
                raise ValueError('Unable to recognize baseline number from the product id {}'.format(self.product_id))
            return '{}.{}'.format(baseline[:2], baseline[2:])
        return self._read_baseline_from_info()

    def _read_baseline_from_info(self):
        """Tries to find and return baseline number from either tileInfo or productInfo file.

        :return: Baseline ID
        :rtype: str
        :raises: ValueError
        """
        if hasattr(self, 'tile_info'):
            return self.tile_info['datastrip']['id'][-5:]
        if hasattr(self, 'product_info'):
            return self.product_info['datastrips'][0]['id'][-5:]
        raise ValueError('No info file has been obtained yet.')

    @staticmethod
    def url_to_tile(url):
        """
        Extracts tile name, date and AWS index from tile url on AWS.

        :param url: class input parameter 'metafiles'
        :type url: str
        :return: Name of tile, date and AWS index which uniquely identifies tile on AWS
        :rtype: (str, str, int)
        """
        info = url.strip('/').split('/')
        name = ''.join(info[-7: -4])
        date = '-'.join(info[-4: -1])
        return name, date, int(info[-1])

    def sort_download_list(self):
        """
        Method for sorting the list of download requests. Band images have priority before metadata files. If bands
        images or metadata files are specified with a list they will be sorted in the same order as in the list.
        Otherwise they will be sorted alphabetically (band B8A will be between B08 and B09).
        """
        def aws_sort_function(download_request):
            data_name = download_request.properties['data_name']
            url_part = download_request.url[len(self.base_url):].strip('/')
            url_part = ''.join(url_part.split('/', 4)[:-1])
            if data_name in self.bands:
                return 0, url_part, self.bands.index(data_name)
            return 1, url_part, self.metafiles.index(data_name)
        self.download_list.sort(key=aws_sort_function)

    def structure_recursion(self, struct, folder):
        """
        From nested dictionaries representing .SAFE structure it recursively extracts all the files that need to be
        downloaded and stores them into class attribute `download_list`.

        :param struct: nested dictionaries representing a part of .SAFE structure
        :type struct: dict
        :param folder: name of folder where this structure will be saved
        :type folder: str
        """
        has_subfolder = False
        for name, substruct in struct.items():
            subfolder = os.path.join(folder, name)
            if not isinstance(substruct, dict):
                if substruct.split('/')[3] == 'products':
                    data_name = substruct.split('/', 8)[-1]
                    if data_name.startswith('datastrip'):
                        items = data_name.split('/', 2)
                        data_name = '/'.join([items[0], '*', items[2]])
                else:
                    data_name = substruct.split('/', 11)[-1]
                if '.' in data_name:
                    data_type = MimeType(substruct.split('.')[-1])
                    data_name = data_name.rsplit('.', 1)[0]
                else:
                    data_type = MimeType.RAW
                if data_name in self.bands + self.metafiles:
                    self.download_list.append(DownloadRequest(url=substruct, filename=subfolder, data_type=data_type,
                                                              data_name=data_name))
            else:
                has_subfolder = True
                self.structure_recursion(substruct, subfolder)
        if not has_subfolder:
            self.folder_list.append(folder)

    @staticmethod
    def add_file_extension(filename, data_format=None, remove_path=False):
        """Joins filename and corresponding file extension if it has one.

        :param filename: Name of the file without extension
        :type filename: str
        :param data_format: format of file, if None it will be set automatically
        :type data_format: constants.MimeType or None
        :param remove_path: True if the path in filename string should be removed
        :type remove_path: bool
        :return: Name of the file with extension
        :rtype: str
        """
        if data_format is None:
            data_format = AwsConstants.AWS_FILES[filename]
        if remove_path:
            filename = filename.split('/')[-1]
        if filename.startswith('datastrip'):
            filename = filename.replace('*', '0')
        if data_format is MimeType.RAW:
            return filename
        return '{}.{}'.format(filename.replace('*', ''), data_format.value)

    def has_reports(self):
        """Products created with baseline 2.06 and greater (and some products with baseline 2.05) should have quality
        report files

        :return: True if the product has report xml files and False otherwise
        :rtype: bool
        """
        return self.baseline > '02.05' or (self.baseline == '02.05' and self.date >= '2017-10-12')  # Not sure

    def is_early_compact_l2a(self):
        """Check if product is early version of compact L2A product

        :return: True if product is early version of compact L2A product and False otherwise
        :rtype: bool
        """
        return self.data_source is DataSource.SENTINEL2_L2A and self.safe_type is EsaSafeType.COMPACT_TYPE and \
            self.baseline <= '02.06'


class AwsProduct(AwsService):
    """ Service class for Sentinel-2 product on AWS

    :param product_id: ESA ID of the product
    :type product_id: str
    :param tile_list: list of tile names
    :type tile_list: list(str) or None
    :param parent_folder: location of the directory where the fetched data will be saved.
    :type parent_folder: str
    :param bands: List of Sentinel-2 bands for request. If parameter is set to ``None`` all bands will be used.
    :type bands: list(str) or None
    :param metafiles: List of additional metafiles available on AWS
                      (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``).
                      If parameter is set to ``None`` the list will be set automatically.
    :type metafiles: list(str) or None
    """
    def __init__(self, product_id, tile_list=None, **kwargs):
        self.product_id = product_id.split('.')[0]
        self.tile_list = self.parse_tile_list(tile_list)

        self.data_source = self.get_data_source()
        self.safe_type = self.get_safe_type()

        super(AwsProduct, self).__init__(**kwargs)

        self.date = self.get_date()
        self.product_url = self.get_product_url()
        self.product_info = get_json(self.get_url(AwsConstants.PRODUCT_INFO))

        self.baseline = self.get_baseline()

    @staticmethod
    def parse_tile_list(tile_input):
        """
        Parses class input and verifies band names.

        :param tile_input: class input parameter `tile_list`
        :type tile_input: str or list(str)
        :return: parsed list of tiles
        :rtype: list(str) or None
        """
        if tile_input is None:
            return None
        if isinstance(tile_input, str):
            tile_list = tile_input.split(',')
        elif isinstance(tile_input, list):
            tile_list = tile_input.copy()
        else:
            raise ValueError('tile_list parameter must be a list of tile names')
        tile_list = [AwsTile.parse_tile_name(tile_name) for tile_name in tile_list]
        return tile_list

    def get_requests(self):
        """
        Creates product structure and returns list of files for download.

        :return: List of download requests and list of empty folders that need to be created
        :rtype: (list(download.DownloadRequest), list(str))
        """
        self.download_list = [DownloadRequest(url=self.get_url(metafile), filename=self.get_filepath(metafile),
                                              data_type=AwsConstants.AWS_FILES[metafile], data_name=metafile) for
                              metafile in self.metafiles if metafile in AwsConstants.PRODUCT_FILES]

        tile_parent_folder = os.path.join(self.parent_folder, self.product_id)
        for tile_info in self.product_info['tiles']:
            tile_name, date, aws_index = self.url_to_tile(self.get_tile_url(tile_info))
            if self.tile_list is None or AwsTile.parse_tile_name(tile_name) in self.tile_list:
                tile_downloads, tile_folders = AwsTile(tile_name, date, aws_index, parent_folder=tile_parent_folder,
                                                       bands=self.bands, metafiles=self.metafiles,
                                                       data_source=self.data_source).get_requests()
                self.download_list.extend(tile_downloads)
                self.folder_list.extend(tile_folders)
        self.sort_download_list()
        return self.download_list, self.folder_list

    def get_data_source(self):
        """The method determines data source from product ID.

        :return: Data source of the product
        :rtype: DataSource
        :raises: ValueError
        """
        product_type = self.product_id.split('_')[1]
        if product_type.endswith('L1C') or product_type == 'OPER':
            return DataSource.SENTINEL2_L1C
        if product_type.endswith('L2A') or product_type == 'USER':
            return DataSource.SENTINEL2_L2A
        raise ValueError('Unknown data source of product {}'.format(self.product_id))

    def get_date(self):
        """ Collects sensing date of the product.

        :return: Sensing date
        :rtype: str
        """
        if self.safe_type == EsaSafeType.OLD_TYPE:
            name = self.product_id.split('_')[-2]
            date = [name[1:5], name[5:7], name[7:9]]
        else:
            name = self.product_id.split('_')[2]
            date = [name[:4], name[4:6], name[6:8]]
        return '-'.join(date_part.lstrip('0') for date_part in date)

    def get_url(self, filename, data_format=None):
        """
        Creates url of file location on AWS.

        :param filename: name of file
        :type filename: str
        :param data_format: format of file, if None it will be set automatically
        :type data_format: constants.MimeType or None
        :return: url of file location
        :rtype: str
        """
        product_url = self.product_url
        force_http = self.data_source is DataSource.SENTINEL2_L1C and \
            filename in [AwsConstants.PRODUCT_INFO, AwsConstants.METADATA]
        if product_url is None or force_http:
            product_url = self.get_product_url(force_http=force_http)
        return '{}/{}'.format(product_url, self.add_file_extension(filename, data_format))

    def get_product_url(self, force_http=False):
        """
        Creates base url of product location on AWS.

        :param force_http: True if HTTP base URL should be used and False otherwise
        :type force_http: str
        :return: url of product location
        :rtype: str
        """
        base_url = self.base_http_url if force_http else self.base_url
        return '{}products/{}/{}'.format(base_url, self.date.replace('-', '/'), self.product_id)

    def get_tile_url(self, tile_info):
        """
        Collects tile url from productInfo.json file.

        :param tile_info: information about tile from productInfo.json
        :type tile_info: dict
        :return: url of tile location
        :rtype: str
        """
        return '{}/{}'.format(self.base_url, tile_info['path'])

    def get_filepath(self, filename):
        """
        Creates file path for the file.

        :param filename: name of the file
        :type filename: str
        :return: filename with path on disk
        :rtype: str
        """
        return os.path.join(self.parent_folder, self.product_id, self.add_file_extension(filename)).replace(':', '.')


class AwsTile(AwsService):
    """ Service class for Sentinel-2 product on AWS

    :param tile: Tile name (e.g. 'T10UEV')
    :type tile: str
    :param time: Tile sensing time in ISO8601 format
    :type time: str
    :param aws_index: There exist Sentinel-2 tiles with the same tile and time parameter. Therefore each tile on AWS
                      also has an index which is visible in their url path. If ``aws_index`` is set to ``None`` the
                      class will try to find the index automatically. If there will be multiple choices it will choose
                      the lowest index and inform the user.
    :type aws_index: int or None
    :param data_source: Source of requested AWS data. Supported sources are Sentinel-2 L1C and Sentinel-2 L2A, default
                        is Sentinel-2 L1C data.
    :type data_source: constants.DataSource
    :param parent_folder: folder where the fetched data will be saved.
    :type parent_folder: str
    :param bands: List of Sentinel-2 bands for request. If parameter is set to ``None`` all bands will be used.
    :type bands: list(str) or None
    :param metafiles: List of additional metafiles available on AWS
                      (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``).
                      If parameter is set to ``None`` the list will be set automatically.
    :type metafiles: list(str) or None
    """
    def __init__(self, tile_name, time, aws_index=None, data_source=DataSource.SENTINEL2_L1C, **kwargs):
        self.tile_name = self.parse_tile_name(tile_name)
        self.datetime = self.parse_datetime(time)
        self.date = self.datetime.split('T')[0]
        self.aws_index = aws_index
        self.data_source = data_source

        super(AwsTile, self).__init__(**kwargs)
        self.tile_url = None

        self.aws_index = self.get_aws_index()
        self.tile_url = self.get_tile_url()
        self.tile_info = self.get_tile_info()
        if not self.tile_is_valid():
            raise ValueError('Cannot find data on AWS for specified tile, time and aws_index')

        self.product_id = self.get_product_id()
        self.safe_type = self.get_safe_type()
        self.baseline = self.get_baseline()

    @staticmethod
    def parse_tile_name(name):
        """
        Parses and verifies tile name.

        :param name: class input parameter `tile_name`
        :type name: str
        :return: parsed tile name
        :rtype: str
        """
        tile_name = name.lstrip('T0')
        if len(tile_name) == 4:
            tile_name = '0' + tile_name
        if len(tile_name) != 5:
            raise ValueError('Invalid tile name {}'.format(name))
        return tile_name

    @staticmethod
    def parse_datetime(time):
        """
        Parses and verifies tile sensing time.

        :param time: tile sensing time
        :type time: str
        :return: tile sensing time in ISO8601 format
        :rtype: str
        """
        try:
            return parse_time(time)
        except Exception:
            raise ValueError('Time must be in format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS')

    def get_requests(self):
        """
        Creates tile structure and returns list of files for download.

        :return: List of download requests and list of empty folders that need to be created
        :rtype: (list(download.DownloadRequest), list(str))
        """
        self.download_list = []
        for data_name in [band for band in self.bands if self._band_exists(band)] + self.metafiles:
            if data_name in AwsConstants.TILE_FILES:
                url = self.get_url(data_name)
                filename = self.get_filepath(data_name)
                self.download_list.append(DownloadRequest(url=url, filename=filename,
                                                          data_type=AwsConstants.AWS_FILES[data_name],
                                                          data_name=data_name))
        self.sort_download_list()
        return self.download_list, self.folder_list

    def get_aws_index(self):
        """
        Returns tile index on AWS. If `tile_index` was not set during class initialization it will be determined
        according to existing tiles on AWS.

        :return: Index of tile on AWS
        :rtype: int
        """
        if self.aws_index is not None:
            return self.aws_index
        tile_info_list = get_tile_info(self.tile_name, self.datetime, all_tiles=True)
        if not tile_info_list:
            raise ValueError('Cannot find aws_index for specified tile and time')

        if self.data_source is DataSource.SENTINEL2_L2A:
            for tile_info in sorted(tile_info_list, key=self._parse_aws_index):
                try:
                    self.aws_index = self._parse_aws_index(tile_info)
                    self.get_tile_info()
                    return self.aws_index
                except AwsDownloadFailedException:
                    pass

        return self._parse_aws_index(tile_info_list[0])

    @staticmethod
    def _parse_aws_index(tile_info):
        """Parses AWS index from tile info

        :param tile_info: dictionary with information about tile
        :type tile_info: dict
        :return: Index of tile on AWS
        :rtype: int
        """
        return int(tile_info['properties']['s3Path'].split('/')[-1])

    def tile_is_valid(self):
        return self.tile_info is not None \
               and (self.datetime == self.date or self.datetime == self.parse_datetime(self.tile_info['timestamp']))

    def get_tile_info(self):
        """
        Collects basic info about tile from tileInfo.json.

        :return: dictionary with tile information
        :rtype: dict
        """
        return get_json(self.get_url(AwsConstants.TILE_INFO))

    def get_url(self, filename):
        """
        Creates url of file location on AWS.

        :param filename: name of file
        :type filename: str
        :return: url of file location
        :rtype: str
        """
        tile_url = self.tile_url
        force_http = self.data_source is DataSource.SENTINEL2_L1C and \
            filename in [AwsConstants.TILE_INFO, AwsConstants.PRODUCT_INFO, AwsConstants.METADATA]
        if tile_url is None or force_http:
            tile_url = self.get_tile_url(force_http=force_http)
        return '{}/{}'.format(tile_url, self.add_file_extension(filename))

    def get_tile_url(self, force_http=False):
        """
        Creates base url of tile location on AWS.

        :param force_http: True if HTTP base URL should be used and False otherwise
        :type force_http: str
        :return: url of tile location
        :rtype: str
        """
        base_url = self.base_http_url if force_http else self.base_url
        url = '{}tiles/{}/{}/{}/'.format(base_url, self.tile_name[0:2].lstrip('0'), self.tile_name[2],
                                         self.tile_name[3:5])
        date_params = self.date.split('-')
        for param in date_params:
            url += param.lstrip('0') + '/'
        return url + str(self.aws_index)

    def get_qi_url(self, metafile):
        """Returns url of tile metadata products

        :param metafile: Name of metadata product at AWS
        :type metafile: str
        :return: url location of metadata product at AWS
        :rtype: str
        """
        return '{}/qi/{}'.format(self.tile_url, metafile)

    def get_gml_url(self, qi_type, band='B00'):
        """
        :param qi_type: type of quality indicator
        :type qi_type: str
        :param band: band name
        :type band: str
        :return: location of gml file on AWS
        :rtype: str
        """
        band = band.split('/')[-1]
        return self.get_qi_url('MSK_{}_{}.gml'.format(qi_type, band))

    def get_preview_url(self, data_type='L1C'):
        """Returns url location of full resolution L1C preview
        :return:
        """
        if self.data_source is DataSource.SENTINEL2_L1C or self.safe_type is EsaSafeType.OLD_TYPE:
            return self.get_url(AwsConstants.PREVIEW_JP2)
        return self.get_qi_url('{}_PVI.jp2'.format(data_type))

    def get_filepath(self, filename):
        """
        Creates file path for the file.

        :param filename: name of the file
        :type filename: str
        :return: filename with path on disk
        :rtype: str
        """
        return os.path.join(self.parent_folder, '{},{},{}'.format(self.tile_name, self.date, self.aws_index),
                            self.add_file_extension(filename)).replace(':', '.')

    def get_product_id(self):
        """
        Obtains ESA ID of product which contains the tile.

        :return: ESA ID of the product
        :rtype: str
        """
        return self.tile_info['productName']

    def _band_exists(self, band_name):
        if self.data_source is DataSource.SENTINEL2_L1C:
            return True
        resolution, band = band_name.split('/')
        if self.safe_type is EsaSafeType.COMPACT_TYPE:
            return not (self.baseline >= '02.07' and band.endswith(AwsConstants.VIS))
        return band != AwsConstants.TCI and not (band == AwsConstants.SCL and resolution == AwsConstants.R60m)

    @staticmethod
    def tile_id_to_tile(tile_id):
        """
        :param tile_id: original tile identification string provided by ESA (e.g.
                        'S2A_OPER_MSI_L1C_TL_SGS__20160109T230542_A002870_T10UEV_N02.01')
        :type: str
        :return: tile name, sensing date and AWS index
        :rtype: (str, str, int)
        """
        if tile_id.split('_')[0] not in ['S2A', 'L1C']:
            raise ValueError('Transformation from tile_id to tile works currently only for Sentinel-2 L1C products')

        tile_info = get_tile_info_id(tile_id)
        return AwsService.url_to_tile(tile_info['properties']['s3Path'])
