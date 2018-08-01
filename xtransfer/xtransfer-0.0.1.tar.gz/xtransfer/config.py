#!/usr/bin/env python

import os
import yaml
import tempfile

from collections import OrderedDict

DEFAULT_CONFIG = '''
loggers:
  console:
    level: info
monitoring:
  host: localhost
  port: 3030
'''


class Config(object):

    def __init__(self, config_filename='~/xtransfer.yaml'):
        '''
        The Config class is intended to resolve configuration from sensible
        defaults and user provided configuration.

        :arg str config_filename: Name / path to the configuration file on which
            this config object.
        '''

        self.config_filename = config_filename

        self.default_config = self.__init_defaults()

        self.loggers = None
        self.monitoring = None
        self.profiles = None
        self.work_dir = None

        self.__setup()

    def __init_defaults(self):
        '''Initialise default configuration from DEFAULT_CONFIG
        '''
        return ordered_load(DEFAULT_CONFIG)

    def __setup(self):
        '''Reads in the xtransfer config file on sets config values appropriately
        '''
        try:
            with open(self.config_filename, 'r') as stream:
                try:
                    user_config = ordered_load(stream)

                    if user_config and 'profiles' in user_config:
                        self.profiles = OrderedDict(user_config['profiles'])
                    else:
                        raise KeyError("Unable to find profiles in: %s" %
                                       self.config_filename)

                    if user_config and 'loggers' in user_config:
                        self.loggers = OrderedDict(user_config['loggers'])
                    else:
                        self.loggers = self.default_config['loggers']

                    if user_config and 'monitoring' in user_config:
                        self.monitoring = OrderedDict(user_config['monitoring'])
                    else:
                        self.monitoring = self.default_config['monitoring']

                    if user_config and 'work_dir' in user_config:
                        self.work_dir = user_config['work_dir']
                    else:
                        self.work_dir = os.path.join(tempfile.gettempdir(),
                                                     'xtransfer')

                except yaml.YAMLError as exc:
                    print("Error in configuration file: %s" % exc)
                    if hasattr(exc, 'problem_mark'):
                        mark = exc.problem_mark
                        print("Error position: (%s:%s)" % (mark.line+1,
                                                           mark.column+1))
                    raise

        except IOError:
            print("Can't find or open config file: %s" % self.config_filename)
            raise


def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    """
    Loads YAML to an OrderedDict rather than an (unordered) dict.
    """
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)
