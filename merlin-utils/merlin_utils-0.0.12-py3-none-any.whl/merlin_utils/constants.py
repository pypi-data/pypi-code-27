from google.cloud import datastore
import os


class Constants:
    class __Constants:
        def __init__(self):
            datastore_client = datastore.Client(os.environ.get("PROJECT"))
            query = datastore_client.query(kind="Params")
            query.add_filter("status", "=", "ACTIVE")
            constants = {}
            for entity in list(query.fetch()):
                constants[entity["name"]] = entity["langValues"]
            self.constants = constants

    instance = None

    def __init__(self):
        if not Constants.instance:
            Constants.instance = Constants.__Constants()

    def get_constant(self, key, language):
        constant = self.constants.get(key)
        if constant and language is not None:
            return constant.get(language)
        elif constant is not None:
            return constant.get("en")

    def __getattr__(self, name):
        return getattr(self.instance, name)
