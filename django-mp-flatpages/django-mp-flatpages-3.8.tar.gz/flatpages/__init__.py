
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from flatpages.constants import FLATPAGE_EDITORS


__version__ = '3.8'


class DefaultFlatPagesConfig(AppConfig):

    name = 'flatpages'
    verbose_name = _("Flat Pages")

    wising_editor = None
    wising_editors = FLATPAGE_EDITORS

    default_template = 'flatpages/default.html'


default_app_config = 'flatpages.DefaultFlatPagesConfig'
