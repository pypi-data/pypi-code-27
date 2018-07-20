# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

"""Make Kindle Collection."""
# TODO:
# ~/.webs.json

# dependencies:
# texlive-latex-base, dvipng,
# python3-httplib2, python3-bs4, python3-cairosvg, python3-pil

import os
import sys
import subprocess
import re
import json
import httplib2
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import namedtuple
import html
from functools import reduce
import argparse

from mkc import images, formulas, macros


WEBS_FILE = os.path.expanduser("~/.webs.json")
if not os.path.isfile(WEBS_FILE):
    with open(WEBS_FILE, 'w') as f:
        f.write(r"{}")
# CACHE_DIR = tempfile.mkdtemp()
CACHE_DIR = "/tmp/mkc"
Article = namedtuple("Article", "title, content")

with open(WEBS_FILE, "r", encoding="utf-8") as f:
    webs = json.load(f)


def _find_content(soup):
    soup.find('article')
    soup.find('div', {'class': 'article'})
    soup.find('h1').parent
    soup.find('h2').parent
    soup.find('h3').parent
    soup.find('font')


def get_article(url, imgs=False, maths=True):
    context_element = get_context_element(url)

    h = httplib2.Http(CACHE_DIR, disable_ssl_certificate_validation=True)
    try:
        response, content = h.request(url)
    except Exception:
        print(url)
        raise
    # soup = BeautifulSoup(content)
    soup = BeautifulSoup(content, 'lxml')

    title = soup.find("title").contents[0]

    snip = soup.find(*context_element)
    if snip is None:
        print(context_element)
        print(url)
        raise RuntimeError(url)

    if imgs:
        for img in snip.findAll("img"):
            img["src"] = images[url, img.get("src", "")]

    content = str(snip)
    if maths:
        with open(macros.MACROS_FILE, 'w') as f:
            macros.write_macros(f, soup)
        content = html.unescape(content)
        content = replace_maths(content)

    return Article(title, content)


EQUATION_REGEXES = [re.compile(p) for p in (
    r"(\\begin{equation}.*?\\end{equation})",
    r"(\\begin{equation\*}.*?\\end{equation\*})",
    r"(\\begin{align}.*?\\end{align})",
    r"(\\begin{align\*}.*?\\end{align\*})",
    r"(\\begin{alignat}.*?\\end{alignat})",
    r"(\\begin{alignat\*}.*?\\end{alignat\*})",
    r"(\\begin{gather}.*?\\end{gather})",
    r"(\\begin{gather\*}.*?\\end{gather\*})",
    # r"\$$(.*?)\$$",
)]
INPLACE_REGEXES = [re.compile(p) for p in (
    r"\\\((.*?)\\\)",
    # r"\$(.*?)\$",
    # r"\eq{<br />(.*?)}<br />",
    r"\\\[(.*?)\\\]",
)]


def replace_maths(text):
    def eq_frepl(matchobj):
        return r"""<img src={} />""".format(formulas[matchobj.group(1)])

    def in_frepl(matchobj):
        return r"""<img src={} />""".format(formulas[
            '$' + matchobj.group(1) + '$'])

    text = re.sub(r"\n\r?", " ", text)
    text = reduce(lambda s, x: re.sub(x, eq_frepl, s), EQUATION_REGEXES, text)
    text = reduce(lambda s, x: re.sub(x, in_frepl, s), INPLACE_REGEXES, text)
    return text


def make_multiple_page(articles, name=None, titles=True):
    filename = os.path.join(CACHE_DIR, name + ".html")
    with open(filename, "w") as f:
        f.write(
            """<!DOCTYPE HTML PUBLIC
            "-//W3C//DTD HTML 4.0//EN"
            "http://www.w3.org/TR/1998/REC-html40-19980424/strict.dtd">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>""")
        f.write(name)
        f.write("""</title>
                </head>
                <body>
                """)

        # TOC
        for i in articles:
            f.write("""<a href="#{title}">{title}<br/></a>
                    """.format(title=i.title))

        # content
        for i in articles:
            if titles:
                f.write("""<a name="{title}"><h1>{title}</h1></a>
                        """.format(title=i.title))
            else:
                f.write("""<a name="{title}"></a>""".format(title=i.title))
            f.write(i.content)

        f.write("</body></html>")

    return filename


def html_to_mobi(html):
    mobi = re.sub(r".html$", ".mobi", os.path.basename(html))
    # os.system("ebook-convert {html} {mobi} > {log}".format(**locals()))
    subprocess.check_output(["ebook-convert", html, mobi])
    return mobi


def get_context_element(url):
    try:
        context_element = webs[urlparse(url).hostname]
    except KeyError:
        print('URL "%s" not listed in %s file. Using <body> element.' % (
            urlparse(url).hostname, WEBS_FILE))
        context_element = "body", {"": ""}
    return context_element


def main():
    parser = argparse.ArgumentParser(
        prog='mkc',
        description="Make Kindle Collection.")

    parser.add_argument("name",
                        default="Spam",
                        help="""title of the collection""")

    # parser.add_argument("--images",
    #                     action="store_true", dest="images", default=True,
    #                     help="""include images (default)""")
    parser.add_argument("--noimages",
                        action="store_false", dest="images",
                        help="""do not include images""")

    parser.add_argument("--formulas",
                        action="store_true", dest="formulas", default=False,
                        help="""include formulas""")
    # parser.add_argument("--noformulas",
    #                     action="store_false", dest="formulas",
    #                     help="""do not include formulas (default)""")

    parser.add_argument("--sort",
                        action="store_true",
                        help="""sort articles by title""")

    parser.add_argument("--notitles",
                        action="store_false", dest="titles",
                        help="""show title above each article""")

    args = parser.parse_args()

    urls = sys.stdin.read().splitlines()

    articles = [get_article(url, imgs=args.images, maths=args.formulas)
                for url in urls]
    if args.sort:
        articles.sort(key=lambda a: a.title)

    page = make_multiple_page(articles, name=args.name,
                              titles=args.titles)
    print(html_to_mobi(page))


if __name__ == "__main__":
    # sys.exit(main())

    url = ("http://motls.blogspot.cz/2016/02/"
           "ligo-wows-bh-masses-3629-to-62-suns-51.html")
    url = "http://www.feynmanlectures.caltech.edu/II_01.html"
    name = "II_01"

    articles = [get_article(url, imgs=False, maths=True)]
    page = make_multiple_page(articles, name=name, titles=True)
    print(html_to_mobi(page))
