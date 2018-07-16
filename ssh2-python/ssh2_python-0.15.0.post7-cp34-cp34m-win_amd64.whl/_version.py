
import json

version_json = '''
{"date": "2018-07-16T15:03:49.264043", "full-revisionid": "6428cb93e97815a372c12821f64272a7256863e8", "error": null, "dirty": false, "version": "0.15.0.post7"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

