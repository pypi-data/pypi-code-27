import json


class Data(object):
    """
    Class tha holds all response data etc
    """

    def __init__(self, **kwargs):
        self.status_code = kwargs.get('status_code')
        self.response = kwargs.get('response')

    def cache_query(self):
        pass

    def meta(self):
        pass

    def data(self):
        pass

    @property
    def raw_data(self) -> json:
        """Returns the raw json"""
        return self.response

    def links(self):
        pass
