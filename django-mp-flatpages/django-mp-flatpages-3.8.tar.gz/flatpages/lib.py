
from django.apps import apps
from django.utils.module_loading import import_string


def get_wising_editor(editor_name):

    if not editor_name:
        return None

    config = apps.get_app_config('flatpages')
    
    try:
        return import_string(config.wising_editors[editor_name])
    except ImportError:
        raise Exception('Flatpage editor module is undefined')
    except KeyError:
        raise Exception('Unknown flatpage editor module')
