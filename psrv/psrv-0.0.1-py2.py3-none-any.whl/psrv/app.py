import logging
import psutil
from json import loads
from time import time
from os.path import dirname
from os.path import join
from pkg_resources import get_distribution

from sanic import Sanic
from sanic.response import html
from sanic.response import json
from sanic.response import text

logger = logging.getLogger(__name__)
app = Sanic()

with open(join(dirname(__file__), 'static', 'index.html')) as fd:
    index_html = fd.read()

webpack_js = get_distribution('psrv').get_metadata(
    'calmjs_artifacts/webpack.js')
psrv_css = get_distribution('psrv').get_metadata(
    'calmjs_artifacts/styles.css')


@app.route('/psrv.js')
async def serve_js(request):
    return text(webpack_js, headers={'Content-Type': 'application/javascript'})


@app.route('/psrv.css')
async def serve_css(request):
    return text(psrv_css, headers={'Content-Type': 'text/css'})


@app.route('/')
async def root(request):
    return html(index_html)


@app.route('/status')
async def status(request):
    return json({
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
    })


def main():
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
