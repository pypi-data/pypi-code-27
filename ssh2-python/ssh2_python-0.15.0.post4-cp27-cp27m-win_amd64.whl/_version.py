
import json

version_json = '''
{"date": "2018-07-16T10:54:08.664000", "full-revisionid": "2c7ba5bd8fa1e97fd4b327dd96e3becdf55001fd", "dirty": false, "version": "0.15.0.post4", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

