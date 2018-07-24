from django.apps import apps as django_apps
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib import messages
from django_revision.revision import site_revision


class LoginView(BaseLoginView):

    template_name = 'edc_base/auth/login.html'

    def get_context_data(self, **kwargs):
        """Tests cookies."""
        self.request.session.set_test_cookie()
        if not self.request.session.test_cookie_worked():
            messages.add_message(
                self.request, messages.ERROR, 'Please enable cookies.')
        self.request.session.delete_test_cookie()
        return super().get_context_data(**kwargs)

    @property
    def extra_context(self):
        app_config = django_apps.get_app_config('edc_base')
        return {
            'copyright': app_config.copyright,
            'disclaimer': app_config.disclaimer,
            'institution': app_config.institution,
            'license': app_config.license,
            'revision': site_revision.tag,
            'project_name': app_config.project_name}
