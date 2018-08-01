from django.forms import Form, fields

from directory_forms_api_client import backends


class EmailBackendMixin:
    backend_class = backends.EmailBackend

    def save(self, submission_recipients, *args, **kwargs):
        backend = self.backend_class(recipients=submission_recipients)
        return backend.save(self.cleaned_data)


class ZendeskBackendMixin:
    backend_class = backends.ZendeskBackend

    requester_email = fields.EmailField()

    def save(self, *args, **kwargs):
        backend = self.backend_class()
        return backend.save(self.cleaned_data)


class EmailAPIForm(EmailBackendMixin, Form):
    pass


class ZendeskAPIForm(ZendeskBackendMixin, Form):
    pass
