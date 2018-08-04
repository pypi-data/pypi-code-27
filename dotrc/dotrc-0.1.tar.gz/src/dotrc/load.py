import os
import yaml
import simplejson as json

def load_yaml(path):
    try:
        return yaml.load(open(path, 'r'))
    except (yaml.scanner.ScannerError, IOError):
        return None

def load_json(path):
    try:
        return json.load(open(path, 'r'))
    except IOError:
        return None

def load(app):
    # Result
    config = {}
    # Get user dir path
    home = os.path.expanduser('~')

    # Generate a list of files to check
    locations = [
        os.path.join(home, '.config', app),
        os.path.join(os.getcwd(), '.' + app + 'rc')
    ]

    # Try to parse file contents as YAML
    for loc in locations:
        cfg = load_yaml(loc) or load_json(loc)

        if cfg:
            config.update(cfg)

    return config
