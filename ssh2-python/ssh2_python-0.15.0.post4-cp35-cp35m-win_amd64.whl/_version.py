
import json

version_json = '''
{"version": "0.15.0.post4", "error": null, "dirty": false, "date": "2018-07-16T11:12:37.556478", "full-revisionid": "2c7ba5bd8fa1e97fd4b327dd96e3becdf55001fd"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

