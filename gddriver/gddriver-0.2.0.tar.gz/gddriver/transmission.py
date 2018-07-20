# -*- coding: utf-8 -*-

import os

import gddriver.errors as errors
import gddriver.models as models
import gddriver.utils.io as ioutil

logger = models.DRIVER_LOGGER_CONFIG.logger
DEFAULT_MULTIPART_TRANSFER_THRESHOLD = 1 << 25  # 32 MB


class _CommonStreamUploadRequest(models.StreamTransferRequest):
    def __init__(self, container_name, stream, object_name):
        super(_CommonStreamUploadRequest, self).__init__(container_name, stream, object_name)
        self._multi = None

    @property
    def multi(self):
        """是否分片上传 bool"""
        return self._multi

    @multi.setter
    def multi(self, v):
        self._multi = v


def upload_object_from_file(connection, request, driver, multipart_transfer_threshold):
    """
    通过路径上传文件，当文件大小超过阈值时，使用分片上传的形式

    文件超过阈值时，由于分片并发上传，校验码的计算可能需要另启一个线程，
    但使用OSS上传并且要求crc64校验码时就不会有此情况，oss会在上传完成时，将crc64返回

    :param driver:  存储服务驱动
    :type  driver: `gddriver.base.StorageDriver`

    :param connection: 连接信息
    :type  connection: `gddriver.base.Connection`

    :param request: 传输请求
    :type  request: `gddriver.models.FileTransferRequest`

    :param multipart_transfer_threshold: 分片传输阈值
    :type  multipart_transfer_threshold: int

    :return:
    """

    final_multipart_threshold = multipart_transfer_threshold or DEFAULT_MULTIPART_TRANSFER_THRESHOLD
    file_path = request.file_path
    object_name = request.object_name

    file_size = os.path.getsize(file_path)
    if file_size < final_multipart_threshold:
        logger.debug("upload %s to %s via stream, data-size=%s", file_path, object_name, file_size)
        with open(file_path, 'rb') as f:
            # 流式上传时，data_size需要用户自定义或者用户的progress_callback有能力处理data_size为空的情况
            stream_request = _CommonStreamUploadRequest(
                container_name=request.container_name,
                stream=f,
                object_name=object_name
            )

            stream_request.checksum_type = request.checksum_type
            stream_request.progress_callback = request.progress_callback
            stream_request.data_size = file_size

            res = driver.upload_object_via_stream(
                request=stream_request,
                connection=connection
            )
            logger.debug("upload %s to %s via stream, data-size=%s, upload successfully",
                         file_path, object_name, file_size)
            return res

    else:
        logger.debug("upload %s to %s by file path, data-size=%s, threads_count=%s",
                     file_path, object_name, file_size, request.threads_count)
        res = driver.upload_file(
            connection=connection,
            request=request
        )
        logger.debug("finished upload %s to %s by file path, data-size=%s, "
                     "threads_count=%s, upload successfully",
                     file_path, object_name, file_size, request.threads_count)
        return res


def download_object_to_file(connection, request, driver,
                            multipart_transfer_threshold, overwrite_existing, delete_on_failure):
    """
        当文件大小超过阈值(threshold)时，会启用多分片并发下载，如果要求计算校验码，则需要额外的时间同步等待校验码计算完成。
    文件未超过阈值时，校验码可以在传输时一并完成计算。

    :param driver:  存储服务驱动
    :type  driver: `gddriver.base.StorageDriver`

    :param connection: 连接信息
    :type  connection: `gddriver.base.Connection`

    :param request: 传输请求
    :type  request: `gddriver.models.FileTransferRequest`

    :param multipart_transfer_threshold: 分片并发下载的阈值（字节）
    :type  multipart_transfer_threshold: ``int``

    :param overwrite_existing: 本地存在时覆盖
    :type  overwrite_existing: ``bool``

    :param delete_on_failure:  下载失败时删除
    :type  delete_on_failure: ``bool``

    :rtype: :class:`gddriver.models.DownloadResult`
    """
    file_path = request.file_path
    object_name = request.object_name
    final_threshold = multipart_transfer_threshold or DEFAULT_MULTIPART_TRANSFER_THRESHOLD
    checksum_type = request.checksum_type

    info = "Download {object_name} to {file_path}, container {container_name}".format(
        object_name=object_name,
        file_path=file_path,
        container_name=request.container_name
    )

    if os.path.isdir(file_path):
        raise errors.PathTypeConflict("%s, local path is a directory".format(info))

    if os.path.exists(file_path) and not overwrite_existing:
        raise errors.FileAlreadyExists("%s, file already exists".format(info))

    object_meta = driver.get_object_meta(
        connection=connection,
        object_name=object_name,
        container_name=request.container_name
    )
    logger.debug("download %s to %s, data-size-threshold: %s, object info: %s",
                 object_name, file_path, final_threshold, object_meta)

    if object_meta.size < final_threshold:
        stream_download_request = models.StreamDownloadRequest(
            container_name=request.container_name,
            object_name=object_name)

        readable_stream = driver.download_object_as_stream(
            request=stream_download_request,
            connection=connection
        )
        stream_adapter = ioutil.make_checksum_adapter(readable_stream, checksum_type)

        with open(file_path, 'wb') as file_:
            size = ioutil.copy_file(stream_adapter, file_)
            if size != object_meta.size and delete_on_failure:
                os.remove(file_path)
                raise errors.UnexpectedDownloadedSize(object_meta.size, size)

        # 部分服务可能会提供server_checksum (比如OSS提供crc_checksum)
        result = models.DownloadResult(
            server_checksum=readable_stream.server_checksum,
            client_checksum=stream_adapter.checksum,
            checksum_type=stream_adapter.checksum_type
        )
    else:
        driver.download_file(
            request=request,
            connection=connection
        )

        checksum_gen = ioutil.create_checksum_yield(
            file_path=file_path,
            checksum_type=checksum_type,
            logger=logger
        )
        checksum = next(checksum_gen)
        result = models.DownloadResult(
            client_checksum=checksum,
            checksum_type=checksum_type
        )
    logger.info("download %s to %s, container %s, download successfully.",
                object_name, file_path, request.container_name)
    return result


def get_object_append_position(connection, driver, object_name, container_name):
    """
    获取对象当前的长度，可用于append_object的position

    :param connection:
    :type  connection: ``gddriver.base.Connection``
    :param driver:
    :type  driver:  ``gddriver.base.StorageDriver``
    :param container_name:
    :type  container_name: ``str``
    :param object_name: Object name.
    :type object_name: ``str``

    :return: 对象长度/坐标
    :rtype: ``int``
    """
    try:
        object_meta = driver.get_object_meta(
            connection=connection,
            object_name=object_name,
            container_name=container_name
        )
        return object_meta.size
    except errors.NoSuchObject:
        return 0
