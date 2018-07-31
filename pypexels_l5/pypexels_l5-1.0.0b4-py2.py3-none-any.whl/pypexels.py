from builtins import object

from .src import API_VERSION, LIB_NAME, Curated, Popular, Search


class PyPexels(object):
    logger_name = LIB_NAME

    def __init__(self, api_key, api_version=API_VERSION):
        self.api_key = api_key
        self.api_version = api_version

    def curated(self, **kwargs):
        return Curated(api_key=self.api_key, api_version=self.api_version, **kwargs)

    def popular(self, **kwargs):
        return Popular(api_key=self.api_key, api_version=self.api_version, **kwargs)

    def search(self, **kwargs):
        return Search(api_key=self.api_key, api_version=self.api_version, **kwargs)
