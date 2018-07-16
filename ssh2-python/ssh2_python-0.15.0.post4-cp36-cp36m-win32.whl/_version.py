
import json

version_json = '''
{"date": "2018-07-16T11:19:22.145653", "dirty": false, "error": null, "full-revisionid": "2c7ba5bd8fa1e97fd4b327dd96e3becdf55001fd", "version": "0.15.0.post4"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

