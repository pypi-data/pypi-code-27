import json
from requests import Session


class Client(object):

    def __init__(self):
        self.base_url = 'https://polisen.se/api/listingservice'
        self.location_route = self.base_url + '/locationsuggestions'
        self.items_route = self.base_url + '/items'
        self.session = Session()

    def get_suggestions(self, location):
        try:
            return json.loads(
                self.session.get(
                    self.location_route + '?query=' + location,
                ).text
            )
        except ValueError:
            return []

    def get_items(self, location_id):
        try:
            return json.loads(
                self.session.post(
                    self.items_route,
                    data={
                        'SelectedLocationId': location_id,
                        'ContentId': 7069,
                        'PageIndex': 1,
                        'IncludeChildIndexes': False,
                        'FilterOnSelectedLocation': True,
                        'filter': None,
                        'GeoAreaType': 1,
                        'Latitude': 0,
                        'Longitude': 0,
                        'ListItemType': 1,
                        'PropertyIds': []
                    }
                ).text
            )['List']
        except ValueError:
            return []
