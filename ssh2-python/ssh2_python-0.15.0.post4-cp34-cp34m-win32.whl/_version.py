
import json

version_json = '''
{"error": null, "version": "0.15.0.post4", "dirty": false, "date": "2018-07-16T10:56:12.642609", "full-revisionid": "2c7ba5bd8fa1e97fd4b327dd96e3becdf55001fd"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

