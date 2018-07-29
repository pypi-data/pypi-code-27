import asyncio
import os

from mlcrypto import Asymmetric
from pkg_resources import DistributionNotFound, get_distribution

from api import API_MAPPING
from controllers.configuration import get_active_config
from controllers.transport import Backbone
from .config import init_cluster


class CliTools:
    @classmethod
    def load_config(cls, loop=None):
        conf_path = os.environ.get('MLADMIN_CONF_DIR', os.path.expanduser('~/.config'))
        debug = os.environ.get('MLADMIN_DEBUG') is not None
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(init_cluster(config_folder=conf_path))
        return conf_path, debug, loop

    @classmethod
    def is_in_container(cls):
        return os.environ.get("ML_RM_MANAGER") == '1'

    @classmethod
    def save_ssh_key(cls, ssh_key_data):
        cipher = Asymmetric.create_from(Asymmetric.ensure_bytes(ssh_key_data))
        config = get_active_config()
        config.general.default_public_key = cipher.export_public_key_bytes().decode('utf-8')
        config.general.default_private_key = cipher.bytes_to_b64str(cipher.export_private_key_bytes('DER'))
        # todo: load old keys
        get_active_config().general.save()

    @classmethod
    def run_ws(cls, loop=None):
        conf_path, debug, loop = cls.load_config(loop)
        active_config = get_active_config()
        return Backbone.create_and_serve(API_MAPPING, debug, active_config, loop)

    @classmethod
    def get_version(cls, package='missinglinkai-resource-manager-docker'):
        try:
            dist = get_distribution(package)
        except DistributionNotFound:
            return None

        return str(dist.version)

    @classmethod
    def save_mali_config(cls, config_prefix, config_data):
        conf_path, debug, loop = cls.load_config()

        mali_path = os.path.join(conf_path, '.MissingLinkAI')
        os.makedirs(mali_path, exist_ok=True)
        filename = 'missinglink.cfg'
        if config_prefix is not None and len(config_prefix) > 0:
            filename = f"{config_prefix}-{filename}"

        if 'access_token' in config_data:
            config_data = config_data.encdode('utf-8')
        else:
            config_data = Asymmetric.b64str_to_bytes(config_data)

        with open(os.path.join(mali_path, filename), 'wb') as f:
            f.write(config_data)
