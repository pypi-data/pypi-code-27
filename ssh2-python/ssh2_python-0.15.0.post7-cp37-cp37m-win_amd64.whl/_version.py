
import json

version_json = '''
{"date": "2018-07-16T15:49:26.028876", "dirty": false, "error": null, "full-revisionid": "6428cb93e97815a372c12821f64272a7256863e8", "version": "0.15.0.post7"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

