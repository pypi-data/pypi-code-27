# -*- coding: utf8 -*-
import logging
import requests
import six
from requests import HTTPError
from requests.exceptions import MissingSchema, InvalidSchema

from .exceptions import NonRetryException, NotFound, AccessDenied
from .path_utils import remove_moniker
import warnings


class GooglePackagesMissing(NonRetryException):
    pass


__gcs_service = None
__gcs_credentials = None


warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")


class closing_with_condition(object):
    def __init__(self, thing, should_close):
        self.thing = thing
        self.should_close = should_close

    def __enter__(self):
        return self.thing

    def __exit__(self, *exc_info):
        if self.should_close:
            self.thing.close()


def gcs_credentials():
    try:
        import google.auth.exceptions
    except ImportError:
        raise GooglePackagesMissing()

    global __gcs_credentials

    if __gcs_credentials is None:
        try:
            __gcs_credentials, _ = google.auth.default()
        except google.auth.exceptions.DefaultCredentialsError:
            pass

    return __gcs_credentials


def gcs_service(credentials=None):
    try:
        from google.cloud import storage
    except ImportError:
        raise GooglePackagesMissing()

    global __gcs_service

    if __gcs_service is None:
        __gcs_service = storage.Client(credentials=credentials)

    return __gcs_service


class GCSService(object):
    RETRYABLE_ERRORS = (IOError, )
    DEFAULT_MIMETYPE = 'application/octet-stream'
    NUM_RETRIES = 5

    def __init__(self, signed_url_service):
        self.signed_url_service = signed_url_service


class GCSDownload(GCSService):
    def __init__(self, auth_method, signed_url_service):
        super(GCSDownload, self).__init__(signed_url_service)
        self._auth_method = auth_method

    def download(self, object_name):
        import requests

        signed_urls = self.signed_url_service.get_signed_urls(['GET'], [object_name])
        url = signed_urls['GET'][0]

        r = requests.get(url)  # allowed to use requests
        r.raise_for_status()
        data = r.content

        logging.debug('downloaded  %s(%s)', object_name, len(data))

        return data


class GCSDownloadDirectDownload(GCSService):
    def __init__(self):
        super(GCSDownloadDirectDownload, self).__init__(None)

    @classmethod
    def download(cls, bucket_name, object_name):
        if bucket_name:
            bucket_name = remove_moniker(bucket_name)

            gcs = gcs_service()

            blob = gcs.bucket(bucket_name).blob(object_name)
            return blob.download_as_string()

        auth_session = _get_auth_session('gcloud')

        r = auth_session.get(object_name)
        r.raise_for_status()

        return r.content


def _wrap_s3_call(callback, bucket_name, key):
    from botocore.exceptions import ClientError
    import boto3

    bucket_name = remove_moniker(bucket_name)

    s3_client = boto3.client('s3')

    try:
        return callback(s3_client, bucket_name, key)
    except s3_client.exceptions.NoSuchBucket:
        raise NotFound('No such S3 Bucket %s' % bucket_name)
    except ClientError as ex:
        if ex.response.get('Error', {}).get('Code') == 'RequestTimeout':
            raise

        if ex.response.get('Error', {}).get('Code') == 'AccessDenied':
            raise AccessDenied('Access Denied s3://%s/%s' % (bucket_name, key))

        if ex.response.get('Error', {}).get('Code') == 'NoSuchKey':
            raise NotFound('Object not found s3://%s/%s' % (bucket_name, key))

        raise NonRetryException('%s (s3://%s/%s)' % (ex, bucket_name, key))


class S3DownloadDirectDownload(GCSService):
    def __init__(self):
        super(S3DownloadDirectDownload, self).__init__(None)

    @classmethod
    def download(cls, bucket_name, object_name):
        def s3_call(_s3_client, s3_bucket_name, s3_object_name):
            import boto3

            s3_resource = boto3.resource('s3')

            obj = s3_resource.Object(s3_bucket_name, s3_object_name)
            return obj.get()['Body'].read()

        return _wrap_s3_call(s3_call, bucket_name, object_name)


class GCSUploadDirect(GCSService):
    def __init__(self):
        super(GCSUploadDirect, self).__init__(None)

    @classmethod
    def upload(cls, bucket_name, object_name, file_obj, headers, credentials=None):
        logging.info('gcs upload (direct) bucket: %s %s', bucket_name, object_name)

        try:
            import google.api_core.exceptions as google_exceptions
        except ImportError:
            raise GooglePackagesMissing()

        gcs = gcs_service(credentials=credentials)

        blob = gcs.bucket(bucket_name).blob(object_name)

        content_type = headers.get('Content-Type')

        try:
            blob.upload_from_file(file_obj, content_type)
        except google_exceptions.NotFound:
            raise NotFound('bucket %s not found' % bucket_name)
        except google_exceptions.PermissionDenied:
            raise AccessDenied('access denied to bucket %s' % bucket_name)


class S3UploadDirect(GCSService):
    def __init__(self):
        super(S3UploadDirect, self).__init__(None)

    # noinspection PyUnusedLocal
    @classmethod
    def upload(cls, bucket_name, object_name, file_obj, headers, credentials=None):
        logging.info('s3 upload %s %s', bucket_name, object_name)

        def s3_call(s3_client, s3_bucket_name, s3_object_name):
            s3_client.upload_fileobj(file_obj, s3_bucket_name, s3_object_name)

        return _wrap_s3_call(s3_call, bucket_name, object_name)

    @classmethod
    def copy(cls, src, dest):
        logging.info('s3 copy %s => %s', src, dest)

        bucket_name, key = dest.split('/', 1)

        def s3_call(s3_client, s3_bucket_name, s3_key):
            s3_client.copy_object(Bucket=s3_bucket_name, CopySource=src, Key=s3_key)

        return _wrap_s3_call(s3_call, bucket_name, key)


class FileWithCallback(object):
    def __init__(self, file_obj, callback):
        file_obj.seek(0, 2)
        self._total = file_obj.tell()
        file_obj.seek(0)

        self._callback = callback
        self._file_obj = file_obj

    def __len__(self):
        return self._total

    def read(self, size):
        data = self._file_obj.read(size)
        if not six.PY2 and isinstance(data, six.string_types):
            data = data.encode()

        if six.PY3 and isinstance(data, six.string_types):
            data = data.encode()

        if self._callback is not None:
            self._callback(len(data))

        return data


class GCSUpload(GCSService):
    def __init__(self, auth_method, head_url, put_url):
        super(GCSUpload, self).__init__(None)
        self._head_url = head_url
        self._put_url = put_url
        self._auth_method = auth_method

    def upload(self, file_obj, headers, progress_callback=None):
        logging.info('gcs upload head: %s put: %s', self._head_url, self._put_url)

        auth_session = _get_auth_session(self._auth_method)

        resp = None

        if self._head_url:
            logging.info('try head url')
            resp = auth_session.head(self._head_url)

            logging.info('try head resp %s', resp)

            if resp.status_code in (204, 404):
                logging.debug('file not found, uploading')
                resp = None

        if resp is None:
            file_obj_with_callback = FileWithCallback(file_obj, progress_callback)

            logging.info('put url')
            resp = auth_session.put(self._put_url, data=file_obj_with_callback, headers=headers)
            logging.info('put url done %s', resp)

        if resp.status_code in (401, 403):
            raise NonRetryException()

        resp.raise_for_status()


class GCSDeleteAll(GCSService):
    @classmethod
    def delete_all(cls, bucket_name, volume_id, max_files=None):
        try:
            import google.api_core.exceptions as google_exceptions
        except ImportError:
            raise GooglePackagesMissing()

        logging.info('delete all at %s/%s', bucket_name, volume_id)
        gcs = gcs_service()

        try:
            list_iter = gcs.bucket(bucket_name).list_blobs(prefix=volume_id)
        except google_exceptions.NotFound:
            logging.warning('bucket %s was not found', bucket_name)
            return

        total_deleted = 0
        for blob in list_iter:
            try:
                gcs.bucket(bucket_name).delete_blob(blob.name)
            except google_exceptions.NotFound:
                pass

            total_deleted += 1

            if max_files is not None and max_files == total_deleted:
                break

        logging .info('total deleted %s', total_deleted)

        return total_deleted


def _get_auth_session(auth_method):
    if auth_method == 'gcloud':
        try:
            import google.auth.transport.requests
        except ImportError:
            raise GooglePackagesMissing()

        credentials = gcs_credentials()

        return google.auth.transport.requests.AuthorizedSession(credentials)

    return requests


s3_moniker = 's3://'


def __retry_if_retry_possible_error(exception):
    logging.debug('got retry exception (upload/download) %s', exception)

    return not isinstance(exception, NonRetryException)


def _default_retry():
    from retrying import retry

    def decor(f):
        return retry(retry_on_exception=__retry_if_retry_possible_error, wait_exponential_multiplier=50, wait_exponential_max=5000)(f)

    return decor


class _CloudUploader(object):
    @classmethod
    def _handle_file_object(cls, full_path_to_data):
        if hasattr(full_path_to_data, 'read'):
            full_path_to_data.seek(0)
            return full_path_to_data

        try:
            return open(full_path_to_data, 'rb')
        except IOError:
            raise NonRetryException('failed to open %s' % full_path_to_data)

    @classmethod
    @_default_retry()
    def with_retry_to_s3(cls, bucket_name, object_name, full_path_to_data, headers):
        file_obj = cls._handle_file_object(full_path_to_data)

        S3UploadDirect().upload(bucket_name, object_name, file_obj, headers)

    @classmethod
    @_default_retry()
    def with_retry_transfer_s3(cls, bucket_name, object_name, full_path_to_data):
        full_s3_path = remove_moniker(full_path_to_data)
        object_name_with_bucket = remove_moniker(bucket_name) + '/' + object_name
        S3UploadDirect().copy(full_s3_path, object_name_with_bucket)

    @classmethod
    @_default_retry()
    def with_retry_to_gcs(cls, auth, put_url, head_url, headers, callback, full_path_to_data):
        file_obj = cls._handle_file_object(full_path_to_data)

        try:
            GCSUpload(auth, head_url, put_url).upload(file_obj, headers, callback)
        except (MissingSchema, InvalidSchema, MissingSchema):
            logging.exception('Invalid request')
            raise NonRetryException('Invalid request')
        except HTTPError as e:
            if e.response.status_code != 412:  # precondition
                return

            raise

    @classmethod
    @_default_retry()
    def with_retry_to_gcs_direct(cls, bucket_name, object_name, headers, full_path_to_data):
        file_obj = cls._handle_file_object(full_path_to_data)

        try:
            GCSUploadDirect().upload(remove_moniker(bucket_name), object_name, file_obj, headers)
        except HTTPError as e:
            if e.response.status_code != 412:  # precondition
                return

            raise


class _S3Upload(object):
    def __init__(self, full_path_to_data, headers):
        self._full_path_to_data = full_path_to_data
        self._headers = headers

    def upload(self, bucket_name, object_name):
        if self._full_path_to_data.startswith(s3_moniker):
            _CloudUploader.with_retry_transfer_s3(bucket_name, object_name, self._full_path_to_data)
            return

        _CloudUploader.with_retry_to_s3(bucket_name, object_name, self._full_path_to_data, self._headers)


class _GCSUpload(object):
    def __init__(self, full_path_to_data, headers):
        self._full_path_to_data = full_path_to_data
        self._headers = headers

    def upload(self, auth, bucket_name, object_name, head_url, put_url, callback):
        if put_url:
            _CloudUploader.with_retry_to_gcs(auth, put_url, head_url, self._headers, callback, self._full_path_to_data)
            return

        _CloudUploader.with_retry_to_gcs_direct(bucket_name, object_name, self._headers, self._full_path_to_data)


def do_upload(auth, bucket_name, object_name, full_path_to_data, headers, head_url, put_url, credentials=None, callback=None):
    global __gcs_credentials

    __gcs_credentials = credentials or __gcs_credentials

    if bucket_name is not None and bucket_name.startswith(s3_moniker):
        _S3Upload(full_path_to_data, headers).upload(bucket_name, object_name)
        return

    _GCSUpload(full_path_to_data, headers).upload(auth, bucket_name, object_name, head_url, put_url, callback)


def __handle_s3_download_if_needed(bucket_name, object_name):
    @_default_retry()
    def with_retry_s3():
        return S3DownloadDirectDownload().download(bucket_name, object_name)

    if object_name.startswith(s3_moniker):
        object_name = remove_moniker(object_name)
        bucket_name, object_name = object_name.split('/', 1)
        return with_retry_s3(), True
    elif bucket_name is not None and bucket_name.startswith(s3_moniker):
        return with_retry_s3(), True

    return None, False


def do_download(auth, bucket_name, object_name, signed_url_service=None):
    data, handled = __handle_s3_download_if_needed(bucket_name, object_name)

    if handled:
        return data

    @_default_retry()
    def with_retry():
        if signed_url_service:
            return GCSDownload(auth, signed_url_service).download(object_name)

        return GCSDownloadDirectDownload().download(bucket_name, object_name)

    return with_retry()


def do_delete_all(bucket_name, volume_id, max_files):
    return GCSDeleteAll(signed_url_service=None).delete_all(bucket_name, volume_id, max_files)
