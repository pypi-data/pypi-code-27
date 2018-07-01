from django.utils.module_loading import autodiscover_modules
from django.apps import AppConfig


class BotsConfig(AppConfig):
    name = 'bots'

    def ready(self):
        autodiscover_modules('bot', 'signals', 'preferences', 'urls')
        print('App initialization finished')
