from spell.api import base_client


KEYS_RESOURCE_URL = "keys"


class KeysClient(base_client.BaseClient):
    def __init__(self, resource_url=KEYS_RESOURCE_URL, **kwargs):
        self.resource_url = resource_url
        super(KeysClient, self).__init__(**kwargs)

    def new_key(self, title, key):
        """Send a new public key to the server.

        Keyword arguments:
        title -- the title for this key
        key -- the public key (openSSH format as specified in RFC 4716 )

        Returns:
        a Key object for the created key

        """
        payload = {"title": title, "key": key}
        r = self.request("post", self.resource_url, payload=payload)
        self.check_and_raise(r)
        return self.get_json(r)["key"]

    def get_keys(self):
        """Get a list of public keys from the server.

        Returns:
        a list of Key objects for this user

        """
        r = self.request("get", self.resource_url)
        self.check_and_raise(r)
        return self.get_json(r)["keys"]

    def get_key(self, key_id):
        """Get a public key from the server

        Keyword arguments:
        key_id -- the id of the public key to retrieve from the server

        Returns:
        a Key object with id key_id for this user

        """
        r = self.request("get", "{}/{}".format(self.resource_url, key_id))
        self.check_and_raise(r)
        return self.get_json(r)["key"]

    def delete_key(self, key_id):
        """Delete a public key from the server

        Keyword arguments:
        key_id -- the id of the public key to delete from the server

        """
        r = self.request("delete", "{}/{}".format(self.resource_url, key_id))
        self.check_and_raise(r)
