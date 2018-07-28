# -----------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2018 Luzzi Valerio 
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        http.py.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     28/07/2018
# -----------------------------------------------------------------------------
from .filesystem import *
from .strings import *
from jinja2 import Environment, FileSystemLoader
import os,sys,math

def webpath(filename, pivot ):
    """
    webpath -  pivot = "/apps/"
    """
    return "/" + rightpart(normpath(filename), pivot)

def loadscripts(dirnames,type="js"):
    """
    loadjs
    """
    text = ""
    dirnames = listify(dirnames, sep=",")

    for dirname in dirnames:
        filenames = ls(dirname, r'.*\.%s$'%(type), recursive=True)
        for filename in filenames:
            filename = webpath(filename,"/apps/")
            if filename != '/':
                if   type=="js":
                    text += sformat("<script type='text/javascript' src='{filename}'></script>\n", {"filename": filename});
                elif type=="css":
                    text += sformat("<link href='{filename}' rel='stylesheet' type='text/css'/>\n",{"filename": filename});

    return text

def httpResponse(text, status, start_response):
    """
    httpResponse
    """
    text = "%s" % str(text)
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(text)))]
    if start_response:
        start_response(status, response_headers)
    return [text]

def httpResponseOK(text, start_response):
    """
    httpResponseOK
    """
    return httpResponse(text, "200 OK", start_response)

def httpResponseNotFound(start_response):
    """
    httpResponseNotFound
    """
    return httpResponse("404 NOT FOUND", "404 NOT FOUND", start_response)

def httpPage(environ, start_response=None, checkuser=False):
    """
    httpPage - return a Html Page
    """
    import gecosistema_core
    url = environ["url"] if "url" in environ else normpath(environ["SCRIPT_FILENAME"])
    url = forceext(url, "html")
    #root   = environ["ROOTDIR"] if "ROOTDIR" in environ else ""
    DOCUMENT_ROOT = environ["DOCUMENT_ROOT"] if "DOCUMENT_ROOT" in environ else ""
    HTTP_COOKIE   = environ["HTTP_COOKIE"]   if "HTTP_COOKIE"   in environ else ""

    #if checkuser and not check_user_permissions(environ):
    #    environ["url"] = "back.html"
    #    return httpPage(environ, start_response)

    if "__file__" in environ:
        chdir(justpath( environ["__file__"]))

    if not file(url):
        return httpResponseNotFound(start_response)

    workdir    = justpath(url)
    index_html = justfname(url)

    jss = (DOCUMENT_ROOT + "/apps/common/lib/js",
           justpath(url),)

    csss = (DOCUMENT_ROOT + "/apps/common/lib/css",
            DOCUMENT_ROOT + "/apps/common/lib/js",
            DOCUMENT_ROOT + "/apps/common/lib/images",
            justpath(url),)

    env = Environment(loader=FileSystemLoader(workdir))
    t = env.get_template(index_html)
    variables = {
        "loadjs":  loadscripts(jss,"js"),
        "loadcss": loadscripts(csss,"css"),
        #"splashscreen": loadsplash(justpath(url) + "/splashscreen.png"),
        "os": os,
        "math": math,
        "gecosistema_core": gecosistema_core,
        "environ":environ
    }
    html = t.render(variables).encode("utf-8","replace")
    return httpResponseOK(html, start_response)
