import yaml
from mlbootstrap.fetch import AbstractFetcher, BasicFetcher
from mlbootstrap.preprocess import AbstractPreprocessor, BasicPreprocessor
from mlbootstrap.model import AbstractModel
from typing import Dict


class Bootstrap:
    def __init__(self,
                 config_path: str,
                 fetcher: AbstractFetcher = BasicFetcher(),
                 preprocessor: AbstractPreprocessor = BasicPreprocessor(),
                 models: Dict[str, AbstractModel] = None):
        self.__load_config(config_path)
        self.__fetcher = fetcher
        self.__preprocessor = preprocessor

        model_name = self.config['model'].get('current', None)
        if model_name and models:
            self.__model = models[model_name]
            self.__model.set_model_name(model_name)
            tag = self.config['model'].get('tag', None)
            self.__model.set_tag(tag)

    def __load_config(self, config_path: str):
        with open(config_path, 'r') as stream:
            self.config = yaml.load(stream)

    def fetch(self):
        self.__fetcher.set_config(self.config)
        if not self.__fetcher.finished():
            self.__fetcher.fetch()
        self.__fetcher.check()

    def preprocess(self, force: bool = False):
        self.fetch()

        self.__preprocessor.set_config(self.config)
        if force:
            self.__preprocessor.process(force=force)
        elif not self.__preprocessor.finished():
            self.__preprocessor.process()

        self.__preprocessor.load_processed()
        self.__preprocessor.check()

    def train(self):
        self._init_model()

        self.__model.train()

    def evaluate(self):
        self._init_model()

        self.__model.evaluate()

    def predict(self):
        self._init_model()

        self.__model.predict()

    def _init_model(self):
        self.preprocess()
        self.__model.set_config(self.config)
        self.__model.set_visible_gpus()
        self.__model.set_dataset(self.__preprocessor.dataset)
