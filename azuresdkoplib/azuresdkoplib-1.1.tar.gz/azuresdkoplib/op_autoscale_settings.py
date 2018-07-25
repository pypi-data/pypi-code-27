# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_autoscale_settings.py
@time: 2016/12/14 16:25
"""

from azure.mgmt.monitor.monitor_management_client import MonitorManagementClient
from azure.common.credentials import UserPassCredentials
from msrestazure.azure_exceptions import CloudError
from .op_status_code import AZURE_STATUS_OK, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, AZURE_STATUS_CLOUD_ERROR, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST, AZURE_STATUS_RES_EXIST, AZURE_INFO_AUTOSCALE_SETTINGS_EXIST, \
    AZURE_INFO_AUTOSCALE_SETTINGS_NOT_EXIST
from .op_func import param_is_null
from .op_resource_group import OPResourceGroup


class OPAutoscaleSettings(object):
    """azure autoscale settings sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.monitor_management_client = MonitorManagementClient(credentials, subscription_id)
        self.autoscale_settings_client = self.monitor_management_client.autoscale_settings

    def list_by_resource_group(self, resource_group_name):
        """list the autoscale settings for a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.autoscale_settings_client.list_by_resource_group(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, autoscale_setting_name):
        """check a autoscale settings if exists"""
        if param_is_null([resource_group_name, autoscale_setting_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == autoscale_setting_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, autoscale_setting_name):
        """get a autoscale settings"""
        if param_is_null([resource_group_name, autoscale_setting_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, autoscale_setting_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_AUTOSCALE_SETTINGS_NOT_EXIST

        try:
            result = self.autoscale_settings_client.get(resource_group_name, autoscale_setting_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def create(self, resource_group_name, autoscale_setting_name, parameters):
        """create a autoscale setting"""
        if param_is_null([resource_group_name, autoscale_setting_name, parameters]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return status_code, result

        status_code, result = self.check_existence(resource_group_name, autoscale_setting_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_AUTOSCALE_SETTINGS_EXIST

        try:
            result = self.autoscale_settings_client.create_or_update(resource_group_name, autoscale_setting_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def update(self, resource_group_name, autoscale_setting_name, parameters):
        """update a autoscale setting"""
        if param_is_null([resource_group_name, autoscale_setting_name, parameters]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return status_code, result

        status_code, result = self.check_existence(resource_group_name, autoscale_setting_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return status_code, result

        try:
            result = self.autoscale_settings_client.create_or_update(resource_group_name, autoscale_setting_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def delete(self, resource_group_name, autoscale_setting_name):
        """delete a autoscale setting"""
        if param_is_null([resource_group_name, autoscale_setting_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, autoscale_setting_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_AUTOSCALE_SETTINGS_NOT_EXIST

        try:
            result = self.autoscale_settings_client.delete(resource_group_name, autoscale_setting_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def enable(self, resource_group_name, autoscale_setting_name):
        if param_is_null([resource_group_name, autoscale_setting_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.get(resource_group_name, autoscale_setting_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        result.enabled = True

        status_code, result = self.update(resource_group_name, autoscale_setting_name, result)
        return status_code, result

    def disable(self, resource_group_name, autoscale_setting_name):
        if param_is_null([resource_group_name, autoscale_setting_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.get(resource_group_name, autoscale_setting_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        result.enabled = False

        status_code, result = self.update(resource_group_name, autoscale_setting_name, result)
        return status_code, result
