import yaml

from pathlib import Path


class Config:

    def __init__(self, config_dir: Path) -> None:
        self.config_dir = config_dir

    def read_home(self):
        return [file for file in self.config_dir.iterdir()]

    def config_options(self):
        return [file.stem for file in self.config_dir.iterdir()]

    def read_config(self, file):
        with (self.config_dir / file).open() as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as error:
                raise error
