# -*- coding:utf-8 -*-

"""
@author: sam
@file: op_keyvault.py
@version: 1.0
@time: 2018/6/5
"""
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault import KeyVaultClient
from azure.common.credentials import UserPassCredentials
from msrestazure.azure_exceptions import CloudError
from azure.keyvault.models.key_vault_error import KeyVaultErrorException

from .op_status_code import AZURE_STATUS_OK, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, AZURE_STATUS_CLOUD_ERROR
from .op_func import param_is_null


class OPKeyvault(object):
    """azure key vault sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.kv_manage_client = KeyVaultManagementClient(credentials, subscription_id).vaults
        self.kv_client = KeyVaultClient(credentials)

    def get(self, resource_group_name, vault_name):
        """get a vault object"""
        if param_is_null([resource_group_name, vault_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.kv_manage_client.get(resource_group_name, vault_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get_secret_value(self, vault_base_url, secret_name, secret_version):
        """get a vault key value"""
        if param_is_null([vault_base_url, secret_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.kv_client.get_secret(vault_base_url=vault_base_url,
                                               secret_name=secret_name,
                                               secret_version=secret_version)
        except KeyVaultErrorException as key_vault_error:
            return AZURE_STATUS_CLOUD_ERROR, key_vault_error.message
        return AZURE_STATUS_OK, result.value
