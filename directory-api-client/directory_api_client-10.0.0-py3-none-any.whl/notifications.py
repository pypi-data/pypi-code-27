from directory_client_core.base import AbstractAPIClient

from directory_api_client.version import __version__


class NotificationsAPIClient(AbstractAPIClient):

    endpoints = {
        'anonymous-unsubscribe': '/notifications/anonymous-unsubscribe/',
    }
    version = __version__

    def anonymous_unsubscribe(self, signed_email_address):
        url = self.endpoints['anonymous-unsubscribe']
        return self.post(url, {'email': signed_email_address})
