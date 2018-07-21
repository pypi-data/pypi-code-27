import yaml


def load_path(path):
    with open(path) as f:
        data = yaml.loads(f)
