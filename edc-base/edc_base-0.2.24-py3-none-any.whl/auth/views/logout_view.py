from django.apps import apps as django_apps
from django.contrib.auth.views import LogoutView as BaseLogoutView


class LogoutView(BaseLogoutView):

    next_page = 'login'

    @property
    def extra_context(self):
        app_config = django_apps.get_app_config('edc_base')
        return {
            'copyright': app_config.copyright,
            'disclaimer': app_config.disclaimer,
            'institution': app_config.institution,
            'license': app_config.license,
            'project_name': app_config.project_name}
