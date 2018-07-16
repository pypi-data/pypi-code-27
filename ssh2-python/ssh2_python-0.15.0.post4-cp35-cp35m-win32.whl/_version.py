
import json

version_json = '''
{"dirty": false, "full-revisionid": "2c7ba5bd8fa1e97fd4b327dd96e3becdf55001fd", "error": null, "version": "0.15.0.post4", "date": "2018-07-16T11:04:53.114887"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

