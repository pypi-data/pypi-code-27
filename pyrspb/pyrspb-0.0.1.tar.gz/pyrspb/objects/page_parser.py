from contextlib import closing
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException


def get_page(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if resp.status_code == 200:
                return BeautifulSoup(resp.content, "html.parser")
            else:
                return None
    except RequestException as e:
        print("Error @ \"{}\": {}".format(url, str(e)))
        return None


class PageParser:
    def __init__(self, location):
        self.url = location
        self.content = get_page(self.url)

    def __parse(self):
        pass
