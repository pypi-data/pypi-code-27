
import json

version_json = '''
{"date": "2018-07-16T16:09:33.718000", "full-revisionid": "8d3de49c6c04ce2d3fdfb3c56d1d3a05f352a875", "dirty": false, "version": "0.15.0.post8", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

