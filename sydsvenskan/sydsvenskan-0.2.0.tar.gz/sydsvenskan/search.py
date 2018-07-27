'''search.py


'''
from urllib.parse import urljoin, urlencode
from collections import namedtuple
import requests
from lxml import etree, html
from pyrfc3339 import parse

ROOT_URL = "https://www.sydsvenskan.se"


_teaser_links = etree.XPath("//a[contains(@class, 'teaser__text-link')]/@href")
_teaser_heading = etree.XPath("//h2[contains(@class, 'teaser__heading')]/text()")
_teaser_datetime = etree.XPath("//time/@datetime")
_nextpagination_link = etree.XPath("//a[contains(@class, 'pagination__link--next')]/@href")

Article = namedtuple("Article", "link heading date")

def search(query):
    '''Yields all search results based on some query. NOTE: Result can be big!'''

    url = "{}/sok?{}".format(ROOT_URL, urlencode({"q": query}))
    print(url)

    while True:
                
        res = requests.get(url)
        doc = html.fromstring(res.content)

        links = [urljoin(ROOT_URL, lnk) for lnk in _teaser_links(doc)]
        headings = _teaser_heading(doc)
        dates = [parse(dt) for dt in _teaser_datetime(doc)]  # convert to dateteime
        yield zip(links, headings, dates)

        # Check if there is another page
        pagination_link = _nextpagination_link(doc)
        if len(pagination_link) == 0:
            return        
        url = urljoin(ROOT_URL, pagination_link[0])


