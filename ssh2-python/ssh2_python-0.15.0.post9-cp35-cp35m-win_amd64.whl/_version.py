
import json

version_json = '''
{"version": "0.15.0.post9", "date": "2018-07-17T15:42:45.203497", "dirty": false, "full-revisionid": "a4d844018d9ee0d78cea1cfbc9b42ecbc0620314", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

