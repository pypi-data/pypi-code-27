
import json

version_json = '''
{"date": "2018-07-16T12:34:36.379000", "full-revisionid": "69a7ff3406bf862059712f31fdd7a7999721624d", "dirty": false, "version": "0.15.0.post6", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

