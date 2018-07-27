'''newsday.py

Reads articles form the daily newsday feed.
'''
import datetime
from collections import namedtuple
import requests
from lxml import etree, html

_newsday_articles_links = etree.XPath("//a[contains(@class, 'newsday__title')]/@href")
_newsday_articles_titles = etree.XPath("//a[contains(@class, 'newsday__title')]/text()")
_newsday_articles_time = etree.XPath("//*[contains(@class, 'newsday__published')]/text()")
_newsday_articles_tags = etree.XPath("//*[contains(@class, 'tag__title')]/text()")

Article = namedtuple("Article", "link title date tag")

def newsday(year, month, day):
    '''Yields all news articles for the given date.'''

    # Download the newsday feed
    url = "https://www.sydsvenskan.se/nyhetsdygnet/{}-{}-{}".format(year, month, day)
    res = requests.get(url)
    doc = html.fromstring(res.content)


    def to_datetime(dt):
        '''Convert time (e.g. 08:34) to proper datetime type'''
        hh, mm = dt.split(":")
        return datetime.datetime(year, month, day, int(hh), int(mm))

    # Extract data from HTML page
    links = _newsday_articles_links(doc)
    titles = _newsday_articles_titles(doc)
    dates = [to_datetime(a) for a in _newsday_articles_time(doc)]
    tags = [t.strip().lower() for t in _newsday_articles_tags(doc)]

    return (Article(*article) for article in zip(links, titles, dates, tags))
