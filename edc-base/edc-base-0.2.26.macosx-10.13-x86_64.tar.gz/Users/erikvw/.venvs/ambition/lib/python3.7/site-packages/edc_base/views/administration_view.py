from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from edc_navbar import NavbarViewMixin

from ..view_mixins import AdministrationViewMixin, EdcBaseViewMixin


class AdministrationView(EdcBaseViewMixin,
                         NavbarViewMixin, AdministrationViewMixin, TemplateView):

    navbar_name = settings.APP_NAME
    navbar_selected_item = 'administration'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
