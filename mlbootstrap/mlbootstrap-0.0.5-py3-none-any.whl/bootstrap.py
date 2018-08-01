import yaml
from mlbootstrap.fetch import AbstractFetcher, BasicFetcher
from mlbootstrap.preprocess import AbstractPreprocessor, BasicPreprocessor
from mlbootstrap.model import AbstractModel
from typing import Dict
import fire

_roots = [
    'hyperparameter',
    'train',
    'predict',
    'custom'
]

_protected_roots = [
    'dataset',
    'processed'
]


class Bootstrap:
    def __init__(self,
                 config_path: str,
                 fetcher: AbstractFetcher = BasicFetcher(),
                 preprocessor: AbstractPreprocessor = BasicPreprocessor(),
                 models: Dict[str, AbstractModel] = None):
        self.__load_config(config_path)
        self._fetcher = fetcher
        self._preprocessor = preprocessor
        self._models = models

    def __load_config(self, config_path: str):
        with open(config_path, 'r') as stream:
            self.config = yaml.load(stream)

    def fetch(self, **kwargs):
        self._parse_arguments(**kwargs)

        self._fetcher.set_config(self.config)
        if not self._fetcher.finished():
            self._fetcher.fetch()
        self._fetcher.check()

    def preprocess(self, force: bool = False, **kwargs):
        self.fetch(**kwargs)

        self._preprocessor.set_config(self.config)
        if force:
            self._preprocessor.process(force=force)
        elif not self._preprocessor.finished():
            self._preprocessor.process()

        self._preprocessor.load_processed()
        self._preprocessor.check()

    def train(self, **kwargs):
        self._init_model(**kwargs)

        self.__model.train()

    def evaluate(self, **kwargs):
        self._init_model(**kwargs)

        self.__model.evaluate()

    def predict(self, **kwargs):
        self._init_model(**kwargs)

        self.__model.predict()

    def add_action(self, action_name, action):
        def _action(**kwargs):
            self._init_model(**kwargs)

            action(self.__model)

        self.__setattr__(action_name, _action)

    def cli(self):
        fire.Fire(self)

    def _init_model(self, **kwargs):
        self.preprocess(**kwargs)

        model_name = self.config['model'].get('name', None)
        if model_name and self._models:
            self.__model = self._models[model_name]
            self.__model.set_model_name(model_name)
            tag = self.config['model'].get('tag', None)
            self.__model.set_tag(tag)

        self.__model.set_config(self.config)
        self.__model.set_visible_gpus()
        self.__model.set_dataset(self._preprocessor.dataset)

    def _parse_arguments(self, **kwargs):
        for key, value in kwargs.items():
            if key in _protected_roots:
                print("cannot set '{}' attribute in cli".format(key))
                exit(1)
            elif key in self.config:
                if isinstance(self.config[key], dict):
                    print("{} is a dict, cannot be set in cli".format(key))
                    exit(1)
                else:
                    value = type(self.config.get(key, ''))(value)
                    self.config[key] = value
            elif any(key in self.config.get(i, {}) for i in _roots):
                root = next(i for i in _roots if key in self.config.get(i, {}))
                self.config[root][key] = value
            elif '.' in key:
                keys = [k for k in key.split('.') if k]
                node = self.config
                for k in keys[:-1]:
                    if k not in node:
                        node[k] = dict()
                    node = node[k]

                k = keys[-1]
                node[k] = value
            else:
                print("no attribute named '{}'".format(key))

        return self.config
