"""App composing and Configuration infrastructure"""
from .config_system import declare_config, set_config
from .app_composing import (call_app_composing_function, init_mara_config_once,
                            register_functionality, get_contributed_functionality,
                            register_functionality_in_all_imported_modules)


def MARA_CONFIG_MODULES():
    import mara_config.config
    yield mara_config.config

def MARA_CLICK_COMMANDS():
    import mara_config.cli
    # only the main command!
    yield mara_config.cli.mara_config



