import os, json
import aperture.errors as errors
from aperture.util.output import apt_logger as logger

OPTION_TYPES = {
    'outpath': 'str',
    'quality': 'int',
    'resolutions': 'str',
    'verbose': 'bool',
    'log': 'bool',
    'max-depth': 'int',
    'wmark-img': 'str',
    'wmark-txt': 'str'
}

OPTION_DEFAULTS = {'quality': 75, 'max-depth': 10}

SUPPORTED_CONFIG_FILES = ['.aperture', 'aperture.json', 'aperturerc']


def config_or_provided(option_key, config_dict, options_dict):
    ''' Determine whether an option was provided by the user in the terminal, and if not use the option specified 
        in the config file if it exists. '''

    flag = '--' + option_key

    # wasn't provided in terminal, so we have to check conf file
    if ((OPTION_TYPES[option_key] == 'bool' and options_dict[flag] is False) or
            options_dict[flag] is None):
        if config_dict is not None and option_key in config_dict:
            return config_dict[option_key]  # use config file value
        elif option_key in OPTION_DEFAULTS:  # wasnt in config file, use default
            return OPTION_DEFAULTS[option_key]

    return options_dict[flag]  # was provided in terminal, use that


def read_config():
    ''' Search for the aperture config file within the current working directory. 
        If it exists, read the json and return the dictionary of validated values. '''

    config_file = select_config_file()

    if not config_file == '':
        logger.log('Using config file \'{}\''.format(config_file), 'info')

        try:
            with open(config_file, 'r') as config_json:
                data = json.load(config_json)
        except json.decoder.JSONDecodeError:
            raise errors.ApertureError(
                'Invalid json found within the config file.')

        validated = validate_data(data)
        return validated
    else:
        return None


def select_config_file():
    ''' Select which config file to read from.

    Returns:
        A string representing the config file to use.
    '''

    config_to_use = ''
    config_file_count = 0
    for config in SUPPORTED_CONFIG_FILES:
        if os.path.isfile(config):
            config_to_use = config
            config_file_count += 1

    if config_file_count > 1:
        raise errors.ApertureError(
            'Multiple config files in current working directory. Only one is permitted.'
        )

    return config_to_use


def validate_data(data):
    ''' Determine whether the config file contains valid syntax, datatypes, ect. '''
    to_remove = []
    for part in data:
        if not (part in OPTION_TYPES and
                isinstance(data[part], eval(OPTION_TYPES[part]))):
            to_remove.append(part)

    if len(to_remove) != 0:
        error_msg = 'Unrecognized key(s) within config file:'

        for issue in to_remove:
            error_msg += ' \'{}\','.format(issue)

        # Remove the final comma from the message
        error_msg = error_msg[:len(error_msg) - 1]
        error_msg += '.'

        raise errors.ApertureError(error_msg)

    return data