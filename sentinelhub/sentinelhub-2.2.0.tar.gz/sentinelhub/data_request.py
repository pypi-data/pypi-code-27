"""
Main module for obtaining data.
"""

# pylint: disable=too-many-instance-attributes

import datetime
import os.path
import logging
import warnings
from abc import ABC, abstractmethod
from copy import deepcopy

from .ogc import OgcImageService
from .geopedia import GeopediaImageService
from .aws import AwsProduct, AwsTile
from .aws_safe import SafeProduct, SafeTile
from .download import download_data, ImageDecodingError, DownloadFailedException
from .io_utils import read_data
from .os_utils import make_folder
from .constants import DataSource, MimeType, CustomUrlParam, ServiceType, CRS
from .config import SHConfig

LOGGER = logging.getLogger(__name__)


class DataRequest(ABC):
    """ Abstract class for all Sentinel Hub data requests.

    Every data request type can write the fetched data to disk and then read it again (and hence avoid the need to
    download the same data again).

    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, *, data_folder=None):
        self.data_folder = data_folder.rstrip('/') if data_folder else None

        self.download_list = []
        self.folder_list = []
        self.create_request()

    @abstractmethod
    def create_request(self):
        raise NotImplementedError

    def get_download_list(self):
        """
        Returns a list of download requests for requested data.
        """
        return self.download_list

    def get_filename_list(self):
        """
        Returns a list of file names where the requested data will be saved or read from, if it
        was already downloaded and saved.
        """
        return [request.filename for request in self.download_list]

    def get_url_list(self):
        """
        Returns a list of urls for requested data.
        """
        return [request.url for request in self.download_list]

    def is_valid_request(self):
        return isinstance(self.download_list, list)

    def get_data(self, *, save_data=False, data_filter=None, redownload=False, max_threads=None,
                 raise_download_errors=True):
        """
        Get requested data either by downloading it or by reading it from the disk (if it
        was previously downloaded and saved).

        :param save_data: flag to turn on/off saving of data to disk. Default is ``False``.
        :type save_data: bool
        :param redownload: if ``True``, download again the requested data even though it's already saved to disk.
                            Default is ``False``, do not download if data is already available on disk.
        :type redownload: bool
        :param data_filter: Used to specify which items will be returned by the method and in which order. E.g. with
            ``data_filter=[0, 2, -1]`` the method will return only 1st, 3rd and last item. Default filter is ``None``.
        :type data_filter: list(int) or None
        :param max_threads: number of threads to use when downloading data; default is ``max_threads=None`` which uses
                            ``5*N`` workers where ``N`` is the number of processors on the system
        :type max_threads: int
        :param raise_download_errors: If ``True`` any error in download process should be raised as
            ``DownloadFailedException``. If ``False`` failed downloads will only raise warnings and the method will
            return list with ``None`` values in places where the results of failed download requests should be.
        :type raise_download_errors: bool
        :return: requested images as numpy arrays, where each array corresponds to a single acquisition and has
                    shape ``[height, width, channels]``.
        :rtype: list of numpy arrays
        """
        self._preprocess_request(save_data, True)
        data_list = self._execute_data_download(data_filter, redownload, max_threads, raise_download_errors)
        return self._add_saved_data(data_list, data_filter, raise_download_errors)

    def save_data(self, *, data_filter=None, redownload=False, max_threads=None, raise_download_errors=False):
        """
        Saves data to disk. If ``redownload=True`` then the data is redownloaded using ``max_threads`` workers.

        :param data_filter: Used to specify which items will be returned by the method and in which order. E.g. with
            `data_filter=[0, 2, -1]` the method will return only 1st, 3rd and last item. Default filter is ``None``.
        :type data_filter: list(int) or None
        :param redownload: data is redownloaded if ``redownload=True``. Default is ``False``
        :type redownload: bool
        :param max_threads: number of threads to use when downloading data; default is ``max_threads=None`` which uses
                            ``5*N`` workers where ``N`` is the number of processors on the system
        :type max_threads: int
        :param raise_download_errors: If ``True`` any error in download process should be raised as
            ``DownloadFailedException``. If ``False`` failed downloads will only raise warnings.
        :type raise_download_errors: bool
        """
        self._preprocess_request(True, False)
        self._execute_data_download(data_filter, redownload, max_threads, raise_download_errors)

    def _execute_data_download(self, data_filter, redownload, max_threads, raise_download_errors):
        """Calls download module and executes the download process

        :param data_filter: Used to specify which items will be returned by the method and in which order. E.g. with
            `data_filter=[0, 2, -1]` the method will return only 1st, 3rd and last item. Default filter is ``None``.
        :type data_filter: list(int) or None
        :param redownload: data is redownloaded if ``redownload=True``. Default is ``False``
        :type redownload: bool
        :param max_threads: the number of workers to use when downloading, default ``max_threads=None``
        :type max_threads: int
        :param raise_download_errors: If ``True`` any error in download process should be raised as
            ``DownloadFailedException``. If ``False`` failed downloads will only raise warnings.
        :type raise_download_errors: bool
        :return: List of data obtained from download
        :rtype: list
        """
        is_repeating_filter = False
        if data_filter is None:
            filtered_download_list = self.download_list
        elif isinstance(data_filter, (list, tuple)):
            try:
                filtered_download_list = [self.download_list[index] for index in data_filter]
            except IndexError:
                raise IndexError('Indices of data_filter are out of range')

            filtered_download_list, mapping_list = self._filter_repeating_items(filtered_download_list)
            is_repeating_filter = len(filtered_download_list) < len(mapping_list)
        else:
            raise ValueError('data_filter parameter must be a list of indices')

        data_list = []
        for future in download_data(filtered_download_list, redownload=redownload, max_threads=max_threads):
            try:
                data_list.append(future.result(timeout=SHConfig().download_timeout_seconds))
            except ImageDecodingError as err:
                data_list.append(None)
                LOGGER.debug('%s while downloading data; will try to load it from disk if it was saved', err)
            except DownloadFailedException as download_exception:
                if raise_download_errors:
                    raise download_exception
                warnings.warn(str(download_exception))
                data_list.append(None)

        if is_repeating_filter:
            data_list = [deepcopy(data_list[index]) for index in mapping_list]

        return data_list

    @staticmethod
    def _filter_repeating_items(download_list):
        """ Because of data_filter some requests in download list might be the same. In order not to download them again
        this method will reduce the list of requests. It will also return a mapping list which can be used to
        reconstruct the previous list of download requests.

        :param download_list: List of download requests
        :type download_list: list(sentinelhub.DownloadRequest)
        :return: reduced download list with unique requests and mapping list
        :rtype: (list(sentinelhub.DownloadRequest), list(int))
        """
        unique_requests_map = {}
        mapping_list = []
        unique_download_list = []
        for download_request in download_list:
            if download_request not in unique_requests_map:
                unique_requests_map[download_request] = len(unique_download_list)
                unique_download_list.append(download_request)
            mapping_list.append(unique_requests_map[download_request])
        return unique_download_list, mapping_list

    def _preprocess_request(self, save_data, return_data):
        """
        Prepares requests for download and creates empty folders

        :param save_data: Tells whether to save data or not
        :type: bool
        :param return_data: Tells whether to return data or not
        :type: bool
        """
        if not self.is_valid_request():
            raise ValueError('Cannot obtain data because request is invalid')

        if save_data and self.data_folder is None:
            raise ValueError('Request parameter `data_folder` is not specified. '
                             'In order to save data please set `data_folder` to location on your disk.')

        for download_request in self.download_list:
            download_request.set_save_response(save_data)
            download_request.set_return_data(return_data)
            download_request.set_data_folder(self.data_folder)

        if save_data:
            for folder in self.folder_list:
                make_folder(os.path.join(self.data_folder, folder))

    def _add_saved_data(self, data_list, data_filter, raise_download_errors):
        """
        Adds already saved data that was not redownloaded to the requested data list.
        """
        filtered_download_list = self.download_list if data_filter is None else \
            [self.download_list[index] for index in data_filter]
        for i, request in enumerate(filtered_download_list):
            if request.return_data and data_list[i] is None:
                if os.path.exists(request.get_file_path()):
                    data_list[i] = read_data(request.get_file_path())
                elif raise_download_errors:
                    raise DownloadFailedException('Failed to download data from {}.\n No previously downloaded data '
                                                  'exists in file {}.'.format(request.url, request.get_file_path()))
        return data_list


class OgcRequest(DataRequest):
    """ The base class for OGC-type requests (WMS and WCS) where all common parameters are
    defined.

    :param data_source: Source of requested satellite data. Default is Sentinel-2 L1C data.
    :type data_source: constants.DataSource
    :param service_type: type of OGC service (WMS or WCS)
    :type service_type: constants.ServiceType
    :param size_x: number of pixels in x or resolution in x (i.e. ``512`` or ``10m``)
    :type size_x: int or str
    :param size_y: number of pixels in x or resolution in y (i.e. ``512`` or ``10m``)
    :type size_y: int or str
    :param bbox: Bounding box of the requested image. Coordinates must be in the specified coordinate reference system.
    :type bbox: common.BBox
    :param time: time or time range for which to return the results, in ISO8601 format
                (year-month-date, for example: ``2016-01-01``, or year-month-dateThours:minuts:seconds format,
                i.e. ``2016-01-01T16:31:21``). When a single time is specified the request will return
                data for that specific date, if it exists. If a time range is specified the result is a list of all
                scenes between the specified dates conforming to the cloud coverage criteria. Most recent acquisition
                being first in the list. For the latest acquisition use ``latest``.
                Examples: ``latest``, ``'2016-01-01'``, or ``('2016-01-01', ' 2016-01-31')``
    :type time: str, or tuple of str
    :param layer: the preconfigured layer (image) to be returned as comma separated layer names. Required.
    :type layer: str
    :param maxcc: maximum accepted cloud coverage of an image. Float between 0.0 and 1.0. Default is ``1.0``.
    :type maxcc: float
    :param image_format: format of the returned image by the Sentinel Hub's WMS getMap service. Default is PNG, but
                        in some cases 32-bit TIFF is required, i.e. if requesting unprocessed raw bands.
                        Default is ``constants.MimeType.PNG``.
    :type image_format: constants.MimeType
    :param instance_id: user's instance id. If ``None`` the instance id is taken from the ``config.json``
                        configuration file.
    :type instance_id: str
    :param custom_url_params: dictionary of CustomUrlParameters and their values supported by Sentinel Hub's WMS and WCS
                              services. All available parameters are described at
                              http://www.sentinel-hub.com/develop/documentation/api/custom-url-parameters. Note: in
                              case of constants.CustomUrlParam.EVALSCRIPT the dictionary value must be a string
                              of Javascript code that is not encoded into base64.
    :type custom_url_params: dictionary of CustomUrlParameter enum and its value, i.e.
                              ``{constants.CustomUrlParam.ATMFILTER:'ATMCOR'}``
    :param time_difference: The time difference below which dates are deemed equal. That is, if for the given set of OGC
                            parameters the images are available at datestimes `d1<=d2<=...<=dn` then only those with
                            `dk-dj>time_difference` will be considered. The default time difference is negative (`-1s`),
                            meaning that all dates are considered by default.
    :type time_difference: datetime.timedelta
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, layer, bbox, *, time='latest', service_type=None, data_source=DataSource.SENTINEL2_L1C,
                 size_x=None, size_y=None, maxcc=1.0, image_format=MimeType.PNG, instance_id=None,
                 custom_url_params=None, time_difference=datetime.timedelta(seconds=-1), **kwargs):
        self.layer = layer
        self.bbox = bbox
        self.time = time
        self.data_source = data_source
        self.maxcc = maxcc
        self.image_format = MimeType(image_format)
        self.instance_id = instance_id
        self.service_type = service_type
        self.size_x = size_x
        self.size_y = size_y
        self.custom_url_params = custom_url_params
        self.time_difference = time_difference

        if self.custom_url_params is not None:
            self._check_custom_url_parameters()

        self.wfs_iterator = None

        super(OgcRequest, self).__init__(**kwargs)

    def _check_custom_url_parameters(self):
        """Checks if custom url parameters are valid parameters.

        Throws ValueError if the provided parameter is not a valid parameter.
        """
        for param in self.custom_url_params.keys():
            if param not in CustomUrlParam:
                raise ValueError('Parameter %s is not a valid custom url parameter. Please check and fix.' % param)

    def create_request(self):
        """Set download requests

        Create a list of DownloadRequests for all Sentinel-2 acquisitions within request's time interval and
        acceptable cloud coverage.
        """
        ogc_service = OgcImageService(instance_id=self.instance_id)
        self.download_list = ogc_service.get_request(self)
        self.wfs_iterator = ogc_service.get_wfs_iterator()

    def get_dates(self):
        """Get list of dates

        List of all available Sentinel-2 acquisitions for given bbox with max cloud coverage and the specified
        time interval. When a single time is specified the request will return that specific date, if it exists.
        If a time range is specified the result is a list of all scenes between the specified dates conforming to
        the cloud coverage criteria. Most recent acquisition being first in the list.

        :return: list of all available Sentinel-2 acquisitions within request's time interval and
                acceptable cloud coverage.
        :rtype: list of strings of form `YYYY:MM:DDThh:mm:ss` representing Sentinel-2 image acquisition time
        """
        return OgcImageService(instance_id=self.instance_id).get_dates(self)

    def get_tiles(self):
        """Returns iterator over info about all satellite tiles used for the OgcRequest

        :return: Iterator of dictionaries containing info about all satellite tiles used in the request. In case of
                 DataSource.DEM it returns None.
        :rtype: Iterator[dict] or None
        """
        return self.wfs_iterator


class WmsRequest(OgcRequest):
    """ Web Map Service request class

    Creates an instance of Sentinel Hub WMS (Web Map Service) GetMap request,
    which provides access to Sentinel-2's unprocessed bands (B01, B02, ..., B08, B8A, ..., B12)
    or processed products such as true color imagery, NDVI, etc. The only difference is that in
    the case od WMS request the user specifies the desired image size instead of its resolution.

    It is required to specify at least one of `width` and `height` parameters. If only one of them is specified the
    the other one will be calculated to best fit the bounding box ratio. If both of them are specified they will be used
    no matter the bounding box ratio.

    :param width: width (number of columns) of the returned image (array)
    :type width: int or None
    :param height: height (number of rows) of the returned image (array)
    :type height: int or None
    :param data_source: Source of requested satellite data. Default is Sentinel-2 L1C data.
    :type data_source: constants.DataSource
    :param bbox: Bounding box of the requested image. Coordinates must be in the specified coordinate reference system.
    :type bbox: common.BBox
    :param time: time or time range for which to return the results, in ISO8601 format
                (year-month-date, for example: ``2016-01-01``, or year-month-dateThours:minuts:seconds format,
                i.e. ``2016-01-01T16:31:21``). When a single time is specified the request will return
                data for that specific date, if it exists. If a time range is specified the result is a list of all
                scenes between the specified dates conforming to the cloud coverage criteria. Most recent acquisition
                being first in the list. For the latest acquisition use ``latest``.
                Examples: ``latest``, ``'2016-01-01'``, or ``('2016-01-01', ' 2016-01-31')``
    :type time: str, or tuple of str
    :param layer: the preconfigured layer (image) to be returned as comma separated layer names. Required.
    :type layer: str
    :param maxcc: maximum accepted cloud coverage of an image. Float between 0.0 and 1.0. Default is ``1.0``.
    :type maxcc: float
    :param image_format: format of the returned image by the Sentinel Hub's WMS getMap service. Default is PNG, but
                        in some cases 32-bit TIFF is required, i.e. if requesting unprocessed raw bands.
                        Default is ``constants.MimeType.PNG``.
    :type image_format: constants.MimeType
    :param instance_id: User's Sentinel Hub instance id. If ``None`` the instance id is taken from the ``config.json``
                        configuration file.
    :type instance_id: str
    :param custom_url_params: dictionary of CustomUrlParameters and their values supported by Sentinel Hub's WMS and WCS
                              services. All available parameters are described at
                              http://www.sentinel-hub.com/develop/documentation/api/custom-url-parameters. Note: in
                              case of constants.CustomUrlParam.EVALSCRIPT the dictionary value must be a string
                              of Javascript code that is not encoded into base64.
    :type custom_url_params: dictionary of CustomUrlParameter enum and its value, i.e.
                              ``{constants.CustomUrlParam.ATMFILTER:'ATMCOR'}``
    :param time_difference: The time difference below which dates are deemed equal. That is, if for the given set of OGC
                            parameters the images are available at datestimes `d1<=d2<=...<=dn` then only those with
                            `dk-dj>time_difference` will be considered. The default time difference is negative (`-1s`),
                            meaning that all dates are considered by default.
    :type time_difference: datetime.timedelta
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str

    More info available at:
    https://www.sentinel-hub.com/develop/documentation/api/ogc_api/wms-parameters
    """
    def __init__(self, *, width=None, height=None, **kwargs):
        super(WmsRequest, self).__init__(service_type=ServiceType.WMS, size_x=width, size_y=height, **kwargs)


class WcsRequest(OgcRequest):
    """ Web Coverage Service request class

    Creates an instance of Sentinel Hub WCS (Web Coverage Service) GetCoverage request,
    which provides access to Sentinel-2's unprocessed bands (B01, B02, ..., B08, B8A, ..., B12)
    or processed products such as true color imagery, NDVI, etc., as the WMS service. The
    only difference is that in the case od WCS request the user specifies the desired
    resolution of the image instead of its size.

    More info available at:
    https://www.sentinel-hub.com/develop/documentation/api/ogc_api/wcs-request

    :param resx: resolution in x (resolution of a column) given in meters in the format (examples ``10m``,
                 ``20m``, ...). Default is ``10m``, which is the best native resolution of some Sentinel-2 bands.
    :type resx: str
    :param resy: resolution in y (resolution of a row) given in meters in the format (examples ``10m``, ``20m``, ...).
                Default is ``10m``, which is the best native resolution of some Sentinel-2 bands.
    :type resy: str
    :param data_source: Source of requested satellite data. Default is Sentinel-2 L1C data.
    :type data_source: constants.DataSource
    :param bbox: Bounding box of the requested image. Coordinates must be in the specified coordinate reference system.
    :type bbox: common.BBox
    :param time: time or time range for which to return the results, in ISO8601 format
                (year-month-date, for example: ``2016-01-01``, or year-month-dateThours:minuts:seconds format,
                i.e. ``2016-01-01T16:31:21``). When a single time is specified the request will return
                data for that specific date, if it exists. If a time range is specified the result is a list of all
                scenes between the specified dates conforming to the cloud coverage criteria. Most recent acquisition
                being first in the list. For the latest acquisition use ``latest``.
                Examples: ``latest``, ``'2016-01-01'``, or ``('2016-01-01', ' 2016-01-31')``
    :type time: str, or tuple of str
    :param layer: the preconfigured layer (image) to be returned as comma separated layer names. Required.
    :type layer: str
    :param maxcc: maximum accepted cloud coverage of an image. Float between 0.0 and 1.0. Default is ``1.0``.
    :type maxcc: float
    :param image_format: format of the returned image by the Sentinel Hub's WMS getMap service. Default is PNG, but
                        in some cases 32-bit TIFF is required, i.e. if requesting unprocessed raw bands.
                        Default is ``constants.MimeType.PNG``.
    :type image_format: constants.MimeType
    :param instance_id: user's instance id. If ``None`` the instance id is taken from the ``config.json``
                        configuration file.
    :type instance_id: str
    :param custom_url_params: dictionary of CustomUrlParameters and their values supported by Sentinel Hub's WMS and WCS
                              services. All available parameters are described at
                              http://www.sentinel-hub.com/develop/documentation/api/custom-url-parameters. Note: in
                              case of constants.CustomUrlParam.EVALSCRIPT the dictionary value must be a string
                              of Javascript code that is not encoded into base64.
    :type custom_url_params: dictionary of CustomUrlParameter enum and its value, i.e.
                              ``{constants.CustomUrlParam.ATMFILTER:'ATMCOR'}``
    :param time_difference: The time difference below which dates are deemed equal. That is, if for the given set of OGC
                            parameters the images are available at datestimes `d1<=d2<=...<=dn` then only those with
                            `dk-dj>time_difference` will be considered. The default time difference is negative (`-1s`),
                            meaning that all dates are considered by default.
    :type time_difference: datetime.timedelta
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, *, resx='10m', resy='10m', **kwargs):
        super(WcsRequest, self).__init__(service_type=ServiceType.WCS, size_x=resx, size_y=resy, **kwargs)


class GeopediaRequest(DataRequest):
    """ The base class for Geopedia's OGC-type requests (WMS and WCS) where all common parameters are
    defined.

    :param service_type: type of OGC service (WMS or WCS)
    :type service_type: constants.ServiceType
    :param size_x: number of pixels in x or resolution in x (i.e. ``512`` or ``10m``)
    :type size_x: int or str
    :param size_y: number of pixels in x or resolution in y (i.e. ``512`` or ``10m``)
    :type size_y: int or str
    :param bbox: Bounding box of the requested image. Coordinates must be in the specified coordinate reference system.
    :type bbox: common.BBox
    :param layer: the preconfigured layer (image) to be returned as comma separated layer names. Required.
    :type layer: str
    :param theme: Geopedia's theme for which the layer is defined.
    :type theme: str
    :param custom_url_params: dictionary of CustomUrlParameters and their values supported by Geopedia's WMS services.
                              At the moment only the transparancy is supported (CustomUrlParam.TRANSPARENT).
    :type custom_url_params: dictionary of CustomUrlParameter enum and its value, i.e.
                              ``{constants.CustomUrlParam.TRANSPARENT:True}``
    :param image_format: format of the returned image by the Sentinel Hub's WMS getMap service. Default is PNG, but
                        in some cases 32-bit TIFF is required, i.e. if requesting unprocessed raw bands.
                        Default is ``constants.MimeType.PNG``.
    :type image_format: constants.MimeType
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, layer, bbox, theme, *, service_type=None, size_x=None, size_y=None, custom_url_params=None,
                 image_format=MimeType.PNG, **kwargs):
        self.layer = layer
        self.theme = theme
        self.bbox = bbox
        self.image_format = MimeType(image_format)
        self.service_type = service_type
        self.size_x = size_x
        self.size_y = size_y

        self.custom_url_params = custom_url_params

        if self.custom_url_params is not None:
            self._check_custom_url_parameters()

        if bbox.crs is not CRS.POP_WEB:
            raise ValueError('Geopedia Request at the moment supports only CRS = {}'.format(CRS.POP_WEB))

        super(GeopediaRequest, self).__init__(**kwargs)

    def _check_custom_url_parameters(self):
        """Checks if custom url parameters are valid parameters.

        Throws ValueError if the provided parameter is not a valid parameter.
        """
        for param in self.custom_url_params.keys():
            if param not in [CustomUrlParam.TRANSPARENT]:
                raise ValueError('Parameter %s is not a valid custom url parameter. Please check and fix.' % param)

    def create_request(self):
        """Set download requests

        Create a list of DownloadRequests for all Sentinel-2 acquisitions within request's time interval and
        acceptable cloud coverage.
        """
        gpd_service = GeopediaImageService()
        self.download_list = gpd_service.get_request(self)


class GeopediaWmsRequest(GeopediaRequest):
    """ Web Map Service request class for Geopedia

    Creates an instance of Geopedia's WMS (Web Map Service) GetMap request,
    which provides access to various layers in Geopedia.

    :param width: width (number of columns) of the returned image (array)
    :type width: int or None
    :param height: height (number of rows) of the returned image (array)
    :type height: int or None
    :param data_source: Source of requested satellite data. Default is Sentinel-2 L1C data.
    :type data_source: constants.DataSource
    :param bbox: Bounding box of the requested image. Coordinates must be in the specified coordinate reference system.
    :type bbox: common.BBox
    :param layer: the preconfigured layer (image) to be returned. Required.
    :type layer: str
    :param theme: Geopedia's theme for which the layer is defined.
    :type theme: str
    :param image_format: format of the returned image by the Geopedia WMS getMap service. Default is PNG.
    :type image_format: constants.MimeType
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, *, width=None, height=None, **kwargs):
        super(GeopediaWmsRequest, self).__init__(service_type=ServiceType.WMS, size_x=width, size_y=height, **kwargs)


class AwsRequest(DataRequest):
    """ The base class for Amazon Web Service request classes. Common parameters are defined here.

    Collects and provides data from AWS.

    AWS database is available at:
    http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/

    :param bands: List of Sentinel-2 bands for request. If `None` all bands will be obtained
    :type bands: list(str) or None
    :param metafiles: list of additional metafiles available on AWS
                      (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``)
    :type metafiles: list(str)
    :param safe_format: flag that determines the structure of saved data. If ``True`` it will be saved in .SAFE format
                        defined by ESA. If ``False`` it will be saved in the same structure as the stucture at AWS.
    :type safe_format: bool
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, *, bands=None, metafiles=None, safe_format=False, **kwargs):
        self.bands = bands
        self.metafiles = metafiles
        self.safe_format = safe_format

        self.aws_service = None
        super(AwsRequest, self).__init__(**kwargs)

    @abstractmethod
    def create_request(self):
        raise NotImplementedError

    def get_aws_service(self):
        """
        :return: initialized AWS service class
        :rtype: aws.AwsProduct or aws.AwsTile or aws_safe.SafeProduct or aws_safe.SafeTile
        """
        return self.aws_service


class AwsProductRequest(AwsRequest):
    """ AWS Service request class for an ESA product

    List of available products:
    http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/#products/

    :param product_id: original ESA product identification string
                       (e.g. ``'S2A_MSIL1C_20170414T003551_N0204_R016_T54HVH_20170414T003551'``)
    :type product_id: str
    :param tile_list: list of tiles inside the product to be downloaded. If parameter is set to ``None`` all
                      tiles inside the product will be downloaded.
    :type tile_list: list(str) or None
    :param bands: List of Sentinel-2 bands for request. If `None` all bands will be obtained
    :type bands: list(str) or None
    :param metafiles: list of additional metafiles available on AWS
                      (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``)
    :type metafiles: list(str)
    :param safe_format: flag that determines the structure of saved data. If ``True`` it will be saved in .SAFE format
                        defined by ESA. If ``False`` it will be saved in the same structure as the stucture at AWS.
    :type safe_format: bool
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, product_id, *, tile_list=None, **kwargs):
        self.product_id = product_id
        self.tile_list = tile_list

        super(AwsProductRequest, self).__init__(**kwargs)

    def create_request(self):
        if self.safe_format:
            self.aws_service = SafeProduct(self.product_id, tile_list=self.tile_list, bands=self.bands,
                                           metafiles=self.metafiles)
        else:
            self.aws_service = AwsProduct(self.product_id, tile_list=self.tile_list, bands=self.bands,
                                          metafiles=self.metafiles)

        self.download_list, self.folder_list = self.aws_service.get_requests()


class AwsTileRequest(AwsRequest):
    """ AWS Service request class for an ESA tile

    List of available products:
    http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/#tiles/

    :param tile: tile name (e.g. ``'T10UEV'``)
    :type tile: str
    :param time: tile sensing time in ISO8601 format
    :type time: str
    :param aws_index: there exist Sentinel-2 tiles with the same tile and time parameter. Therefore each tile on AWS
                      also has an index which is visible in their url path. If aws_index is set to ``None`` the class
                      will try to find the index automatically. If there will be multiple choices it will choose the
                      lowest index and inform the user.
    :type aws_index: int or None
    :param data_source: Source of requested AWS data. Supported sources are Sentinel-2 L1C and Sentinel-2 L2A, default
                        is Sentinel-2 L1C data.
    :type data_source: constants.DataSource
    :param bands: List of Sentinel-2 bands for request. If `None` all bands will be obtained
    :type bands: list(str) or None
    :param metafiles: list of additional metafiles available on AWS
                      (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``)
    :type metafiles: list(str)
    :param safe_format: flag that determines the structure of saved data. If ``True`` it will be saved in .SAFE format
                        defined by ESA. If ``False`` it will be saved in the same structure as the stucture at AWS.
    :type safe_format: bool
    :param data_folder: location of the directory where the fetched data will be saved.
    :type data_folder: str
    """
    def __init__(self, *, tile=None, time=None, aws_index=None, data_source=DataSource.SENTINEL2_L1C, **kwargs):
        self.tile = tile
        self.time = time
        self.aws_index = aws_index
        self.data_source = data_source

        super(AwsTileRequest, self).__init__(**kwargs)

    def create_request(self):
        if self.safe_format:
            self.aws_service = SafeTile(self.tile, self.time, self.aws_index, bands=self.bands,
                                        metafiles=self.metafiles, data_source=self.data_source)
        else:
            self.aws_service = AwsTile(self.tile, self.time, self.aws_index, bands=self.bands,
                                       metafiles=self.metafiles, data_source=self.data_source)

        self.download_list, self.folder_list = self.aws_service.get_requests()


def get_safe_format(product_id=None, tile=None, entire_product=False, bands=None, data_source=DataSource.SENTINEL2_L1C):
    """
    Returns .SAFE format structure in form of nested dictionaries. Either ``product_id`` or ``tile`` must be specified.

    :param product_id: original ESA product identification string. Default is ``None``
    :type product_id: str
    :param tile: tuple containing tile name and sensing time/date. Default is ``None``
    :type tile: (str, str)
    :param entire_product: in case tile is specified this flag determines if it will be place inside a .SAFE structure
                           of the product. Default is ``False``
    :type entire_product: bool
    :param bands: list of bands to download. If ``None`` all bands will be downloaded. Default is ``None``
    :type bands: list(str) or None
    :param data_source: In case of tile request the source of satellite data has to be specified. Default is Sentinel-2
                        L1C data.
    :type data_source: constants.DataSource
    :return: Nested dictionaries representing .SAFE structure.
    :rtype: dict
    """
    entire_product = entire_product and product_id is None
    if tile is not None:
        safe_tile = SafeTile(tile_name=tile[0], time=tile[1], bands=bands, data_source=data_source)
        if not entire_product:
            return safe_tile.get_safe_struct()
        product_id = safe_tile.get_product_id()
    if product_id is None:
        raise ValueError('Either product_id or tile must be specified')
    safe_product = SafeProduct(product_id, tile_list=[tile[0]], bands=bands) if entire_product else \
        SafeProduct(product_id, bands=bands)
    return safe_product.get_safe_struct()


def download_safe_format(product_id=None, tile=None, folder='.', redownload=False, entire_product=False, bands=None,
                         data_source=DataSource.SENTINEL2_L1C):
    """
    Downloads .SAFE format structure in form of nested dictionaries. Either ``product_id`` or ``tile`` must
    be specified.

    :param product_id: original ESA product identification string. Default is ``None``
    :type product_id: str
    :param tile: tuple containing tile name and sensing time/date. Default is ``None``
    :type tile: (str, str)
    :param folder: location of the directory where the fetched data will be saved. Default is ``'.'``
    :type folder: str
    :param redownload: if ``True``, download again the requested data even though it's already saved to disk. If
                       ``False``, do not download if data is already available on disk. Default is ``False``
    :type redownload: bool
    :param entire_product: in case tile is specified this flag determines if it will be place inside a .SAFE structure
                           of the product. Default is ``False``
    :type entire_product: bool
    :param bands: list of bands to download. If ``None`` all bands will be downloaded. Default is ``None``
    :type bands: list(str) or None
    :param data_source: In case of tile request the source of satellite data has to be specified. Default is Sentinel-2
                        L1C data.
    :type data_source: constants.DataSource
    :return: Nested dictionaries representing .SAFE structure.
    :rtype: dict
    """
    entire_product = entire_product and product_id is None
    if tile is not None:
        safe_request = AwsTileRequest(tile=tile[0], time=tile[1], data_folder=folder, bands=bands,
                                      safe_format=True, data_source=data_source)
        if entire_product:
            safe_tile = safe_request.get_aws_service()
            product_id = safe_tile.get_product_id()
    if product_id is not None:
        safe_request = AwsProductRequest(product_id, tile_list=[tile[0]], data_folder=folder, bands=bands,
                                         safe_format=True) if entire_product else \
            AwsProductRequest(product_id, data_folder=folder, bands=bands, safe_format=True)

    safe_request.save_data(redownload=redownload)
