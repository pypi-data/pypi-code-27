
class BaseAPIMethods(object):

    def __init__(self, client):
        if client is not None:
            self.client = client
        else:
            raise ValueError()