import os
import sys
import re
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
    except (json.errors.JSONDecodeError, IOError):
        return None

def load_files(files):
    config = {}

    # Try to parse file contents as YAML, falling back to JSON
    for f in files:
        cfg = load_yaml(f) or load_json(f)

        if cfg:
            config.update(cfg)

    return config

def load_configs(app):
    # Get user dir path
    home = os.path.expanduser('~')

    # Generate a list of files to check
    locations = [
        os.path.join(home, '.config', app),
        os.path.join(os.getcwd(), '.' + app + 'rc')
    ]

    return load_files(locations)

def load_cmdline():
    cfg = False
    files = []

    for idx, arg in enumerate(sys.argv):
        # If populating config files, continue until a switch/option
        if cfg and re.match('\A--?.*\Z', arg) is None:
            files.append(arg)
        else:
            cfg = False

        # Swap to populating files mode
        if arg == '--config':
            cfg = True

        # --config=<file> syntax
        res = re.match('\A--config=(.*)\Z', arg)
        if res:
            files.append(res.group(1))

    if len(files) > 0:
        return load_files(files)
    else:
        return None

def load(app):
    config = {}

    files_cfg = load_configs(app)
    if files_cfg is not None:
        config.update(files_cfg)

    cmdline_cfg = load_cmdline()
    if cmdline_cfg is not None:
        config.update(cmdline_cfg)

    return config
