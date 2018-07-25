# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_service_bus_queue.py
@time: 2016/12/14 16:25
"""
from azure.mgmt.servicebus.service_bus_management_client import ServiceBusManagementClient
from azure.mgmt.servicebus.models.sb_queue import SBQueue
from azure.mgmt.servicebus.models.error_response import ErrorResponseException
from azure.common.credentials import UserPassCredentials
from msrestazure.azure_exceptions import CloudError

from .op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
from .op_func import param_is_null


class OPServiceBusQueue(object):
    """azure service bus sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password, verify=False)
        self.sb_client = ServiceBusManagementClient(credentials, subscription_id)
        self.sb_queue_client = self.sb_client.queues
        self.sb_np_client = self.sb_client.namespaces

    def list_name_space_by_rg(self, resource_group_name):
        """list all name space"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_np_client.list_by_resource_group(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_namespace(self, resource_group_name, namespace_name):
        """list all service bus"""
        if param_is_null([resource_group_name, namespace_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_queue_client.list_by_namespace(resource_group_name, namespace_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def create_or_update(self, resource_group_name, namespace_name, queue_name, parameters):
        """create or update service bus"""
        if param_is_null([resource_group_name, namespace_name, queue_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.get(resource_group_name, namespace_name, queue_name)
        if status_code != AZURE_STATUS_OK and "Not Found" in result:
            pass
        else:
            return status_code, result

        enable_partitioning = parameters.get("enable_partitioning", None)
        duplicate_detection_history_time_window = parameters.get("duplicate_detection_history_time_window", None)
        default_message_time_to_live = parameters.get("default_message_time_to_live", None)
        requires_duplicate_detection = parameters.get("requires_duplicate_detection", None)
        lock_duration = parameters.get("lock_duration", None)
        max_delivery_count = parameters.get("max_delivery_count", None)
        max_size_in_megabytes = parameters.get("max_size_in_megabytes", None)
        if param_is_null([enable_partitioning, duplicate_detection_history_time_window, default_message_time_to_live,
                          requires_duplicate_detection, lock_duration, max_delivery_count, max_size_in_megabytes]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        sb_queue = SBQueue(lock_duration=lock_duration,
                           max_size_in_megabytes=max_size_in_megabytes,
                           requires_duplicate_detection=requires_duplicate_detection,
                           requires_session=False,
                           default_message_time_to_live=default_message_time_to_live,
                           dead_lettering_on_message_expiration=True,
                           duplicate_detection_history_time_window=duplicate_detection_history_time_window,
                           max_delivery_count=max_delivery_count,
                           status=None,
                           auto_delete_on_idle=None,
                           enable_partitioning=enable_partitioning,
                           enable_express=False)

        try:
            result = self.sb_queue_client.create_or_update(resource_group_name, namespace_name, queue_name, sb_queue)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def delete(self, resource_group_name, namespace_name, queue_name):
        """delete service bus queue"""
        if param_is_null([resource_group_name, namespace_name, queue_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_queue_client.delete(resource_group_name, namespace_name, queue_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get(self, resource_group_name, namespace_name, queue_name):
        """get a service bus queue object"""
        if param_is_null([resource_group_name, namespace_name, queue_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_queue_client.get(resource_group_name, namespace_name, queue_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        except ErrorResponseException as response_err:
            return AZURE_STATUS_CLOUD_ERROR, response_err.message
        return AZURE_STATUS_OK, result

    def get_message_count_detail(self, resource_group_name, namespace_name, queue_name):
        """get service bus queue message detail info"""
        if param_is_null([resource_group_name, namespace_name, queue_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            queue_resource = self.sb_queue_client.get(resource_group_name, namespace_name, queue_name)
            message_count_detail = queue_resource.count_details
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, message_count_detail
