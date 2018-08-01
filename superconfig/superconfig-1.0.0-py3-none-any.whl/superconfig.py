import os
import json
import argparse

class SuperConfig(object):
    def __init__(self, prefix, config_file_name):
        self._prefix = prefix
        self._config_file_name = config_file_name
        self._config = {}
        self._parsed_config_file = None
        self._argparse_parser = argparse.ArgumentParser()
        self._argparse_args = None

    def add_argument(self, name, default, argparse_kwargs={}):
        self._config[name] = default
        self._argparse_parser.add_argument('--%s' % name, default=default)

    def _get_config_file_path(self):
        for path in ('.%s' % self._config_file_name,
                     os.path.expanduser('~/.%s' % self._config_file_name),
                     '/etc/%s' % self._config_file_name):
            if os.path.exists(path):
                return os.path.abspath(path)

    def _get_value_env(self, name):
        return os.environ.get(('%s_%s' % (self._prefix, name)).upper())

    def _get_value_file(self, name):
        file_path = self._get_config_file_path()
        if not file_path:
            return None, False
        if not self._parsed_config_file:
            with file(file_path) as f:
                self._parsed_config_file = json.load(f)
        try:
            val = self._parsed_config_file[name]
            return val, True
        except KeyError:
            return None, False

    def _get_value_argparser(self, name):
        if not self._argparse_args:
            self._argparse_args = self._argparse_parser.parse_args()
        return getattr(self._argparse_args, name)

    def get_value(self, name):
        # Default
        value = self._config[name]
        # System environment
        new_value = self._get_value_env(name)
        if new_value:
            value = new_value
        # Config file
        new_value, success = self._get_value_file(name)
        if success:
            value = new_value
        new_value = self._get_value_argparser(name)
        # Argparse
        if self._config[name] != new_value:
            value = new_value
        return value