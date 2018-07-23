from typing import List
from googleapiclient import http
from toto9.gcp_api import GenericGcpApi
from toto9.errors import GcpApiExecutionError
from io import BytesIO


class CloudStorage(GenericGcpApi):
    def __init__(self, credentials_path: str=None, scopes: List=None) -> None:
        self.service_module = 'storage'
        self.service_version = 'v1'
        super(CloudStorage, self).__init__(
            self.service_module,
            self.service_version,
            credentials_path=credentials_path,
            scopes=scopes
        )
        self.storage_service = self.initialized_gcp_service()
        self.page_size = 100

    def objects_list(self, bucket: str, opt: dict={}) -> list:
        """List all objects in a given bucket
        """
        request: googleapiclient.discovery.Request = self.storage_service.objects().list(bucket=bucket, **opt)
        obj_list = []

        self.logger.debug(f'listing objects for bucket {bucket}')

        while request is not None:
            objects: dict = self._execute(request)
            obj_list += objects.get('items', [])
            request = self.storage_service.objects().list_next(request, objects)

        return obj_list

    def objects_insert(self, bucket: str, name: str, filename: str) -> list:
        """Add/Insert storage objects
            when name has training '/', it'll create folder
        """
        body = {
            'name': name
        }
        params = {
            'bucket': bucket,
            'body': body,
            'media_body': filename 
        }
        request: googleapiclient.discovery.Request = self.storage_service.objects().insert(**params)
        # note:unable to use _execute since bytes object in this request is not json serializable
        res = request.execute()

        return res
        
    def objects_delete(self, bucket: str, object: str) -> list:
        """Delete storage object
        """
        request: googleapiclient.discovery.Request = self.storage_service.objects().delete(bucket=bucket, object=object)
        res = self._execute(request)

        return res
       
    def buckets_get(self, bucket: str) -> list:
        """Get bucket
        """
        request: googleapiclient.discovery.Request = self.storage_service.buckets().get(bucket=bucket)
        res = self._execute(request)

        return res
