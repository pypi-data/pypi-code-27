"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""
from django.conf import settings as project_settings

from oembedservice.utils.importers import import_class


class Settings:
    pass


Settings.API_AUTHENTICATION_CLASS = import_class(
    getattr(
        project_settings,
        'OEMBEDSERVICE_API_AUTHENTICATION_CLASS',
        'rest_framework.authentication.BasicAuthentication'
    )
)

Settings.API_PERMISSION_CLASS = import_class(
    getattr(
        project_settings,
        'OEMBEDSERVICE_API_PERMISSION_CLASS',
        'rest_framework.permissions.IsAuthenticated'
    )
)

settings = Settings
