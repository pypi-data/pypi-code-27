import os

from urllib.parse import urlparse, urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    'Accept': 'application/atom+xml, application/rss+xml, application/xml;q=0.8, text/xml;q=0.6, */*;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
}


def absolute_links_patch(doc, web_url):
    """Patching the invalid IPV6 URL. lxml was throwing an error due to which absolute links were
    not added.

    @:param: web_url: domain of the website from the page url.
    @:param: document in the form of lxml element.
    @:return: doc instance
    """
    to_drop = []
    for item in doc.xpath('.//a'):
        if item.get('href'):
            if item.get('href').__contains__('[') or item.get('href').__contains__(']'):
                to_drop.append(item)
    for node in to_drop:
        node.drop_tree()
    doc.make_links_absolute(web_url)
    return doc


def make_complete_url(url, domain):
    """
    url is the path which does not have http://.
    @:param url: A web link URL
    @:param domain: A main website domain url
    """
    if not url.startswith("http"):
        tld = urlparse(domain)
        main_url = tld.netloc
        url_type = tld.scheme + '://'

        # urljoin does not allow the // so we are stripping one /

        if url.startswith("//"):
            url = url[1:]

        url = urljoin(url_type + main_url, url)
        return url
    else:
        return url


def root_path():
    dir = os.path.dirname(os.path.abspath(__file__))
    split_form = dir.split("virtualenv/")
    root_dir = split_form[0] + "virtualenv/" + split_form[1].split("/")[0]
    return root_dir
