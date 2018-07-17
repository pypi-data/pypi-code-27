
import json

version_json = '''
{"full-revisionid": "a4d844018d9ee0d78cea1cfbc9b42ecbc0620314", "error": null, "dirty": false, "date": "2018-07-17T15:28:48.569474", "version": "0.15.0.post9"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

