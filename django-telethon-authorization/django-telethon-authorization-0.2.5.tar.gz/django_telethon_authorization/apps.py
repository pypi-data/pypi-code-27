from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class TelegramAuthConfig(AppConfig):
    name = 'django_telethon_authorization'

    def ready(self):
        if not (
            settings.TG_API_ID and
            settings.TG_API_HASH
        ):
            raise ImproperlyConfigured(
                "\nIn order to use django-telethon-authorization you must set environment variables:\n"
                "TG_API_ID\n"
                "TG_API_HASH"
            )
