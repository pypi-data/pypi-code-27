
import json

version_json = '''
{"version": "0.15.0.post7", "date": "2018-07-16T14:58:16.759283", "error": null, "dirty": false, "full-revisionid": "6428cb93e97815a372c12821f64272a7256863e8"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

