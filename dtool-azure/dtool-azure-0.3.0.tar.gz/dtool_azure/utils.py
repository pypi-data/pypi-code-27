"""Dtool Azure helper functions."""

import base64
import binascii

from azure.storage.blob import BlockBlobService

from dtoolcore.utils import get_config_value


def get_azure_account_key(account_name, config_path):
    """Return the Azure account key associated with the account name."""

    account_key = get_config_value(
        "DTOOL_AZURE_ACCOUNT_KEY_" + account_name,
        config_path=config_path
    )
    return account_key


def base64_to_hex(input_string):
    """Return the hex encoded version of the base64 encoded input string."""

    return binascii.hexlify(base64.b64decode(input_string)).decode()


def get_blob_service(storage_account_name, config_path):
    account_key = get_azure_account_key(
        storage_account_name,
        config_path=config_path
    )
    if account_key is None:
        message = [
            "Cannot find key for '{}' azure account".format(
                storage_account_name
            ),
            "Hint: export DTOOL_AZURE_ACCOUNT_KEY_{}=azure_key".format(
                storage_account_name
            ),
        ]

        raise(KeyError(". ".join(message)))

    return BlockBlobService(
        account_name=storage_account_name,
        account_key=account_key
    )
