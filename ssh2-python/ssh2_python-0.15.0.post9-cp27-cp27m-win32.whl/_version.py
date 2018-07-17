
import json

version_json = '''
{"date": "2018-07-17T15:18:05.815000", "full-revisionid": "a4d844018d9ee0d78cea1cfbc9b42ecbc0620314", "dirty": false, "version": "0.15.0.post9", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

