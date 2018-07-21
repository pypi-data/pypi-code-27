from flask import Flask, request

from cutt_sd import register_api, find_api, unregister_api, zk
from cutt_sd.config import *

app = Flask(__name__)


@app.route('/', methods=['POST'])
def func():
    ip = request.remote_addr
    port = request.form.get('port')
    uri = request.form.get('uri')
    action = request.form.get('action')
    env = request.form.get('env', DEFAULT_ENV)

    if action and uri and port:
        if 'register' == action:
            register_api(uri, ip, port, env)
        elif 'unregister' == action:
            unregister_api(uri, ip, port, env)

    return 'OK'


@app.route('/query', methods=['POST', 'GET'])
def locate():
    api_func = request.values.get('uri')
    env = request.values.get('env', DEFAULT_ENV)
    if func:
        ret = find_api(api_func, env)
        return ret if ret else ''

    return ''


if 'ZK_SERVER' in os.environ:
    zk.init(os.environ['ZK_SERVER'])

if __name__ == '__main__':
    app.run(port=4367, debug=True)
