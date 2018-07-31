import os
import json
import logging


logger = logging.getLogger('setup_log')


def get_secrets(SETTINGS_DIR):
    SECRET_FILE = os.path.join(SETTINGS_DIR, 'secrets.json')
    try:
        with open(SECRET_FILE, 'r') as file:
            SECRETS = json.load(file)
    except FileNotFoundError:
        logger.warning('File not found! "generator <PROJ_NAME>" first please!')
        return None
    return type('secrets', (), SECRETS)
