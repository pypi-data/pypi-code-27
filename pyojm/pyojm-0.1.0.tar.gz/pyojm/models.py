import json


class Model:
    class Meta:
        strict_validation = False

    def __init__(self, json_dict: dict = None, json_str: str = None):
        if json_dict:
            self.raw = json_dict
        elif json_str:
            json.loads(json_str)
        else:
            raise ValueError('Either json_dict or json_str is required.')
