import os


def credential(instance):
    alias = "AZURE_" + instance
    connection_kwargs = {
        'database': os.environ[alias + "_DATABASE"],
        'username': os.environ[alias + "_USERNAME"],
        'server': os.environ[alias + "_HOST"],
        'port': os.environ[alias + "_PORT"],
        'password': os.environ[alias + "_PASSWORD"],
        'driver': os.environ[alias + "_DRIVER"],
    }
    return connection_kwargs
