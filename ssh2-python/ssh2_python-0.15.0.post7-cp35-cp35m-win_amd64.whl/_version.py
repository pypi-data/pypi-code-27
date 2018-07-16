
import json

version_json = '''
{"version": "0.15.0.post7", "full-revisionid": "6428cb93e97815a372c12821f64272a7256863e8", "date": "2018-07-16T15:17:34.170516", "dirty": false, "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

