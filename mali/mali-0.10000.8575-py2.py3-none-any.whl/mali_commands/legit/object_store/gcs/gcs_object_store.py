# -*- coding: utf8 -*-
import logging
from collections import OrderedDict

from ...gcs_utils import gcs_credentials, do_upload, do_delete_all, do_download, s3_moniker
from ...connection_mixin import ConnectionMixin
from ...dulwich.object_store import BaseObjectStore
from ...dulwich.objects import hex_to_filename, Blob


def return_request_result(response, content):
    return response, content


class GCSObjectStore(ConnectionMixin, BaseObjectStore):
    def __init__(self, connection):
        super(GCSObjectStore, self).__init__(connection)
        self.__upload_pool = None
        self._object_store_auth = connection.data_volume_config.object_store_config.get('auth')
        self.__bucket_name = connection.data_volume_config.object_store_config.get('bucket_name')
        self.__embedded = connection.data_volume_config.embedded
        self.__volume_id = self._connection.data_volume_config.volume_id
        self._signed_url_service = None
        self.__multi_process_control = None

    def delete_all(self, max_files=None):
        return do_delete_all(self.__bucket_name, self.__volume_id, max_files)

    def set_multi_process_control(self, multi_process_control):
        self.__multi_process_control = multi_process_control

    @classmethod
    def get_content_headers(cls, content_type=None):

        headers = OrderedDict()
        if content_type:
            headers['Content-Type'] = content_type

        headers['x-goog-acl'] = 'public-read'
        headers['x-goog-if-generation-match'] = '0'

        return headers

    @classmethod
    def _get_shafile_path(cls, sha):
        # Check from object dir
        return hex_to_filename('objects', sha)

    @classmethod
    def on_upload_error(cls, ex):
        raise ex

    def upload(self, obj, head_url=None, put_url=None, callback=None):
        object_name = self._get_shafile_path(obj.sha)

        if self.__bucket_name and not self.__bucket_name.startswith(s3_moniker) or self._object_store_auth == 'gcloud':
            credentials = gcs_credentials()
        else:
            credentials = None

        content_type = obj.content_type
        headers = GCSObjectStore.get_content_headers(content_type)

        object_name = '%s/%s' % (self.__volume_id, object_name)

        args = (
            self._object_store_auth,
            self.__bucket_name, object_name, obj.full_path, headers, head_url, put_url, credentials)

        self.__multi_process_control.execute(do_upload, args=args, callback=callback)

    def add_object(self, obj):
        """Add a single object to this object store.

        :param obj: Object to add
        """
        self.upload(obj)

    def _get_loose_object(self, metadata):
        logging.debug('get object %s', metadata)

        sha = metadata['@id']

        if self.__embedded or self.__bucket_name is not None:
            object_name = '%s/%s' % (self.__volume_id, self._get_shafile_path(sha))
        else:
            object_name = metadata['@url']

        data = do_download(
            self._object_store_auth, self.__bucket_name, object_name, signed_url_service=self._signed_url_service)

        blob = Blob()
        blob.set_raw_chunks([data], sha)
        return blob

    def get_raw(self, metadata):
        """Obtain the raw text for an object.

        :param metadata: metadata for the object.
        :return: tuple with numeric type and object contents.
        """
        ret = self._get_loose_object(metadata)
        if ret is not None:
            return ret.type_num, ret.as_raw_string()

        raise KeyError(metadata)

    @property
    def packs(self):
        raise NotImplementedError(self.packs)

    def __iter__(self):
        raise NotImplementedError(self.__iter__)

    def add_objects(self, objects, callback=None):
        for obj in objects:
            self.upload(obj, callback=callback)

    def contains_packed(self, sha):
        raise NotImplementedError(self.contains_packed)

    def contains_loose(self, sha):
        raise NotImplementedError(self.contains_loose)
