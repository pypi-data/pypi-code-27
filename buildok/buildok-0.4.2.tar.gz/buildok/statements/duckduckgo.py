# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from buildok.statements.web import ViewWeb


class DuckDuckGoSearch(ViewWeb):
    r"""Open a DuckDuckGo search in default browser.

    Args:
        search (str): Search string to lookup.

    Retuns:
        str: Output as string.

    Raises:
        TypeError: If an invalid `search` is provided.

    Accepted statements:
        ^lookup `(?P<search>.+)` online$

    Sample (input):
        - Lookup `buildok` online.

    Expected:
        Lookup results => https://duckduckgo.com/?q=buildok
    """

    def run(self, search=None, *args, **kwargs):
        url = r"https://duckduckgo.com/?q={}".format(search)
        error = self.open_url(url)
        if error is not None:
            self.fail(error)
        else:
            self.success("Lookup results => %s" % url)
