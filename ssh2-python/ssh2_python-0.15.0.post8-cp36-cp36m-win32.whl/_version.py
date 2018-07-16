
import json

version_json = '''
{"date": "2018-07-16T16:38:51.512686", "dirty": false, "error": null, "full-revisionid": "8d3de49c6c04ce2d3fdfb3c56d1d3a05f352a875", "version": "0.15.0.post8"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

