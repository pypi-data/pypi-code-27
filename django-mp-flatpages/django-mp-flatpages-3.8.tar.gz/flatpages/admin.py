
from importlib import import_module

from django.apps import apps
from django.db import models
from django.contrib import admin

from flatpages.forms import FlatpageForm
from flatpages.models import FlatPage
from flatpages.lib import get_wising_editor


def _get_flatpage_admin_base_class():

    if apps.is_installed('modeltranslation'):
        return import_module('modeltranslation.admin').TranslationAdmin

    return admin.ModelAdmin


class FlatPageAdmin(_get_flatpage_admin_base_class()):

    form = FlatpageForm

    list_display = ['url', 'title']

    list_filter = ['registration_required']

    search_fields = ['url', 'title']

    def __init__(self, *args, **kwargs):

        config = apps.get_app_config('flatpages')

        if config.wising_editor:
            self.formfield_overrides = {
                models.TextField: {
                    'widget': get_wising_editor(config.wising_editor)
                }
            }

        super(FlatPageAdmin, self).__init__(*args, **kwargs)


admin.site.register(FlatPage, FlatPageAdmin)
