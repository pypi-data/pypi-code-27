import requests
import json
import base64


class Serde:

    @staticmethod
    def serialize(a):
        pass

    @staticmethod
    def deserialize(s):
        pass


class StringSerde:

    @staticmethod
    def serialize(a) -> str:
        return make_json_friendly(bytes(a, "UTF-8"))

    @staticmethod
    def deserialize(s) -> str:
        return str(decode_json_friendly(s), "UTF-8")


class JsonSerde:

    @staticmethod
    def serialize(a) -> str:
        serialized = json.dumps(a)
        return make_json_friendly(bytes(serialized, "UTF-8"))

    @staticmethod
    def deserialize(s) -> object:
        deserialized_string = str(decode_json_friendly(s), "UTF-8")
        return json.loads(deserialized_string)


class BytesSerde:

    @staticmethod
    def serialize(b: bytes) -> str:
        return make_json_friendly(b)

    @staticmethod
    def deserialize(s) -> bytes:
        return decode_json_friendly(s)


class BridgeClient:

    def __init__(self, host):
        self.host = host
        self.topics: {str: (Serde, Serde)} = {}

    def init_topic(self, topic_name: str, key_serde: Serde = StringSerde, value_serde: Serde=StringSerde):
        if topic_name in self.topics:
            print("Already initialized")
        else:
            self.topics[topic_name] = (key_serde, value_serde)
            response = requests.get("http://{}/topic/{}".format(self.host, topic_name), headers={'KAFKA-TIMEOUT-MS': '1000'})
            assert len(response.json()) == 0

    def send(self, topic_name: str, key, value):
        if topic_name not in self.topics:
            raise Exception("Topic {} not initialized".format(topic_name))

        key_serde, value_serde = self.topics.get(topic_name)

        headers = {"Content-Type": "application/json"}
        request_data = {"key": key_serde.serialize(key), "value": value_serde.serialize(value)}

        response = requests.post("http://{}/topic/{}".format(self.host, topic_name), json=request_data,
                                 headers=headers)
        assert response.status_code == 200
        return response.json()

    def poll(self, topic_name: str, timeout_ms: int=1000) -> dict:
        if topic_name not in self.topics:
            raise Exception("Topic {} not initialized".format(topic_name))

        key_serde, value_serde = self.topics.get(topic_name)
        headers = {'KAFKA-TIMEOUT-MS': str(timeout_ms)}
        response = requests.get("http://{}/topic/{}".format(self.host, topic_name), headers=headers)
        assert response.status_code == 200

        kafkaJson = response.json()
        if len(kafkaJson) == 0:
            return None
        assert len(kafkaJson) == 1, 'Usually means the topic was not properly created in kafka'
        serialized_key = kafkaJson[0]["key"]
        serialized_value = kafkaJson[0]["value"]
        return {"key": key_serde.deserialize(serialized_key), "value": value_serde.deserialize(serialized_value)}


def make_json_friendly(key_or_value: bytes) -> str:
    encoded = base64.b64encode(key_or_value)
    encoded_as_string = str(encoded, 'utf-8')
    return encoded_as_string


def decode_json_friendly(key_or_value: str) -> bytes:
    bytes_from_friendly = bytes(key_or_value, "utf-8")
    decoded = base64.b64decode(bytes_from_friendly)
    return decoded


