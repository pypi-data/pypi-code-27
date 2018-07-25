from django.forms import Form, fields

from directory_forms_api_client import backends


class DirectoryFormsEmailBackendMixin:
    backend_class = backends.DirectoryFormsBackendEmail

    def save(self, submission_recipients, *args, **kwargs):
        backend = self.backend_class(recipients=submission_recipients)
        return backend.save(self.cleaned_data)


class DirectoryFormsZendeskBackendMixin:
    backend_class = backends.DirectoryFormsBackendZendesk

    requester_email = fields.EmailField()

    def save(self, *args, **kwargs):
        backend = self.backend_class()
        return backend.save(self.cleaned_data)


class DirectoryFormsEmailBaseForm(DirectoryFormsEmailBackendMixin, Form):
    pass


class DirectoryFormsZendeskBaseForm(DirectoryFormsZendeskBackendMixin, Form):
    pass
