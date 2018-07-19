import requests

from urllib.parse import urljoin

from lxml.html import fromstring, HTMLParser
from lxml import etree
from datetime import datetime
from time import mktime
from functools import reduce
from webparser.utils import absolute_links_patch, HEADERS

import feedparser
import logging

log = logging.getLogger('Parser')


def convert_to_doc(html, domain_for_absolute_link=None):
    """
    Accept the html content document, convert it to the doc element
    If we want to convert relative links to absolute links, we pass the
    domain url to the absolute links.

    :param html: A response html content or string body
    :param domain_for_absolute_link: A domain URL which used for creating an absolute links
    :return doc instance of the html.
    """
    # if isinstance(html, (unicode)):
    #     html = html.encode('ascii', 'xmlcharrefreplace')

    parser = HTMLParser(encoding='utf-8')
    try:
        doc = fromstring(html, parser=parser)
    except TypeError:
        doc = etree.parse(html, parser)
    except ValueError:
        doc = fromstring(html.encode('utf-8'))

    if domain_for_absolute_link:
        try:
            doc.make_links_absolute(domain_for_absolute_link)
        except Exception as ex:
            absolute_links_patch(doc, domain_for_absolute_link)

    return doc


def has_rss_feed(html, website_url=None):
    """

    :param html: HTML content of a web page.
    :param website_url: A website URL of a web page.
    :return:
    """
    ACCEPTED_MIMETYPES = [
        'application/rss+xml',
        'application/rdf+xml',
        'application/atom+xml',
        'application/xml',
        'text/xml'
    ]

    feed_links = []
    # if it has a website url, convert to absolute links.
    doc = convert_to_doc(html, website_url)

    # checking the links if they contains the accepted mimetype, if they does, they have the RSS URL.

    for selector in ACCEPTED_MIMETYPES:
        links = doc.xpath(".//link[@type='{0}']/@href".format(selector))
        if links:
            for link in links:
                if not link.__contains__('comments'):
                    feed_links.append(link)

    # if there are no RSS URL found using above mechanism, run a fuzzy search for the website.

    if not feed_links:
        log.debug('Attempting for the /feed/ method to find the URL')
        fuzzy_url_search(website_url, feed_links)

    return feed_links


def fuzzy_url_search(url, feed_links):
    """

    :param url: A website/domain URL
    :param feed_links: An existing list of feed links.
    :return: list of feed links.
    """
    if url:
        request_instance = requests  # TODO: replace with the proxy instance later on.
        feed_url = urljoin(url, 'feed')
        response = request_instance.get(feed_url, headers=HEADERS)
        if response.status_code == 200:
            if response.url.__contains__('feed'):
                feed_links.append(feed_url)

    return feed_links


class FeedParser(object):
    """Parsing the feed by content or url, the user will have to pass the feed link/description"""

    def __init__(self, feed=None):
        """If we are passing the feed object, we can check the eTag, and Modified Tag."""
        self.feed = feed

    def tokenize(self, text):
        try:
            text = fromstring(text).text_content().encode('ascii', 'xmlcharrefreplace')
        except:
            pass

        if text:
            try:
                return len(str(text).split(" "))
            except UnicodeDecodeError as ex:
                log.debug('unicode decode error at tokenize', ex=ex)
        else:
            return 0

    def has_entries(self, parsed_feed):
        return parsed_feed['entries'] or not parsed_feed['bozo']

    def parse(self, url=None, doc=None):
        if not url and not doc:
            if self.feed:
                url = self.feed
        parsed = None
        feed = {}
        feed_average_words = []
        feed_posts = []
        if url:
            parsed = feedparser.parse(url)
        if doc:
            parsed = feedparser.parse(doc)
        if parsed:
            if self.has_entries(parsed):
                # if the feed has entries, process them.

                for item in parsed['entries']:
                    words_count = {}
                    description = {}
                    try:

                        if len(item['links']) > 1:
                            feed = {
                                'title': item['title'].encode('ascii', 'xmlcharrefreplace'),
                                'link': item['links'],
                            }

                        else:
                            try:
                                feed = {
                                    'title': item['title'].encode('ascii', 'xmlcharrefreplace'),
                                    'link': item['links'][0]['href'],
                                }
                            except:
                                pass
                    except:
                        pass

                    try:
                        feed['published'] = datetime.fromtimestamp(mktime(item['published_parsed'])),
                    except KeyError:
                        feed['published'] = None
                    except TypeError:
                        feed['published'] = None

                    try:
                        feed['media'] = item['media_content'][0]['url']
                    except KeyError:
                        feed['media'] = None

                    if not feed['media']:
                        try:
                            feed['media'] = item['media_thumbnail'][0]['url']
                        except KeyError:
                            feed['media'] = None

                    # Max number of words depending on the type of feed data.

                    try:
                        description['summary_detail'] = item['summary_detail']['value'].encode(
                            'ascii', 'xmlcharrefreplace'),
                        words_count['summary_detail'] = self.tokenize(description['summary_detail'])
                    except KeyError:
                        description['summary_detail'] = None
                        words_count['summary_detail'] = 0

                    try:
                        description['content'] = item['content'][0]['value'].encode('ascii', 'xmlcharrefreplace')
                        words_count['content'] = self.tokenize(description['content'])
                    except KeyError:
                        description['content'] = None
                        words_count['content'] = 0

                    try:
                        description['body'] = item['body'][0]['value'].encode('ascii', 'xmlcharrefreplace')
                        words_count['body'] = self.tokenize(description['body'])
                    except KeyError:
                        description['body'] = None
                        words_count['body'] = 0

                    # get highest number

                    max_number = max(words_count['summary_detail'], words_count['content'], words_count['body'])

                    feed['max_number'] = max_number
                    feed_average_words.append(max_number)

                    # place the highest number value to feed description

                    for name, value in enumerate(words_count):
                        if max_number == words_count[value]:
                            feed['description'] = description[value]

                    try:
                        feed['author'] = item['author_detail']['name']
                    except KeyError:
                        feed['author'] = None
                        pass

                    feed_posts.append(feed)

                try:
                    average_words = reduce(lambda x, y: x + y, feed_average_words) / len(feed_average_words)
                except TypeError:
                    average_words = 0
                return {
                    'feeds': feed_posts,
                    'average_words': average_words
                }

    def parse_links(self, url=None, doc=None):
        # TODO: return empty array instead of false.
        # But, first need to see the use case for it.

        parsed = None
        if url:
            parsed = feedparser.parse(url)
        if doc:
            parsed = feedparser.parse(doc)
        feed_links = []
        if parsed:
            if self.has_entries(parsed):
                for item in parsed['entries']:
                    try:
                        if item['links'][0].get('href'):
                            feed_links.append(item['links'][0]['href'])
                    except KeyError as ex:
                        pass

                return feed_links
            else:
                return False
        else:
            return False
