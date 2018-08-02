from directory_client_core.base import AbstractAPIClient

from directory_api_client.version import __version__


class BuyerAPIClient(AbstractAPIClient):

    endpoints = {
        'save': 'buyer/',
        'csv-dump': 'buyer/csv-dump/'
    }
    version = __version__

    def send_form(self, form_data):
        return self.post(
            self.endpoints['save'],
            data=form_data
        )

    def get_csv_dump(self, token):
        url = self.endpoints['csv-dump']
        return self.get(url, params={'token': token})
