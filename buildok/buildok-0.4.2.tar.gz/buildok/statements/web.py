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

import webbrowser as wb

from buildok.action import Action


class ViewWeb(Action):
    r"""Open a link in default browser.

    Args:
        url (str): URL to open.

    Retuns:
        str: Output as string.

    Raises:
        TypeError: If an invalid `url` is provided.

    Accepted statements:
        ^open in browser `(?P<url>.+)`$
        ^open (?:link|url) `(?P<url>.+)`$

    Sample (input):
        - Open link `https://github.com/lexndru/buildok`.

    Expected:
        Opened URL in browser => https://github.com/lexndru/buildok
    """

    def run(self, url=None, *args, **kwargs):
        error = self.open_url(url)
        if error is not None:
            self.fail(error)
        else:
            self.success("Opened URL in browser => %s" % url)

    def open_url(self, url):
        try:
            wb.get().open(url, new=2)
        except wb.Error as e:
            return str(e)
        except TypeError as e:
            return str(e)
        except Exception as e:
            return "Cannot open \"%s\": %s" % (url, str(e))
        return None

    @classmethod
    def convert_shell(cls, url=None, *args, **kwargs):
        if url is None:
            return "echo Cannot open browser: URL is missing?"
        return "echo Cannot open URL in browser: %s" % url
