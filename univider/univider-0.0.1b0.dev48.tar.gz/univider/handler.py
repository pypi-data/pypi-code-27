# -*- coding: utf-8 -*-
import json

from flask import Flask, request, jsonify

from univider.settings import app_user

app = Flask(__name__)

@app.route("/crawl", methods=['GET', 'POST'])
def crawl():

    # parse needs
    data = request.get_data()
    params = json.loads(data)

    # authentication
    if (params.has_key("user") and params.has_key("secret") and params["secret"] == app_user.get(params["user"])):
        # handle needs
        from univider.fetcher import Fetcher
        fetcher = Fetcher()
        result = fetcher.fetch_page_with_cache(params)
    else:
        result = {
            'status': 'error',
            'description': 'Authentication failed.'
        }

    # return needs
    return jsonify(result)
    # return result["html"].decode('gbk')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5010,debug=False)

def main():
    app.run(host='0.0.0.0',port=5010,debug=False)