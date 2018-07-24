class Config(object):
    def __init__(self, **kwargs):
        self.dict = kwargs or {}
        for key in self.dict:
            setattr(self, str(key), self.dict[key])

    def __setitem__(self, key, value):
        self.dict[key] = value
        setattr(self, str(key), value)

    def update(self, config=None, **kwargs):
        dict1 = config.dict if config else {}
        dict2 = kwargs
        self.dict.update(dict1)
        self.dict.update(dict2)
        for key in self.dict:
            setattr(self, str(key), self.dict[key])
