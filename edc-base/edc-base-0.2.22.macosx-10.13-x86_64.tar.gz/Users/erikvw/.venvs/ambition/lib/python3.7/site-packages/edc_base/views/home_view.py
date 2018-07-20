from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from django.conf import settings


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'edc_base/home.html'
    navbar_name = 'edc_base'
    navbar_selected_item = 'edc_base'

    def get_context_data(self, **kwargs):
        from edc_base.freeze import edc_packages, third_party_packages
        context = super().get_context_data(**kwargs)
        context.update(
            edc_packages=edc_packages,
            third_party_packages=third_party_packages,
            installed_apps=settings.INSTALLED_APPS)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
