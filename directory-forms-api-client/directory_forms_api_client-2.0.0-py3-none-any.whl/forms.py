from django.forms import Form, fields

from directory_forms_api_client import actions


class EmailActionMixin:
    action_class = actions.EmailAction

    def save(
        self, recipients, subject, reply_to, from_email, *args, **kwargs
    ):
        action = self.action_class(
            recipients=recipients,
            subject=subject,
            reply_to=reply_to,
            from_email=from_email,
        )
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return {
            'text_body': self.text_body,
            'html_body': self.html_body,
        }

    @property
    def text_body(self):
        raise NotImplementedError()

    @property
    def html_body(self):
        raise NotImplementedError()


class ZendeskActionMixin:
    action_class = actions.ZendeskAction

    requester_email = fields.EmailField()

    def save(self, *args, **kwargs):
        action = self.action_class()
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return self.cleaned_data


class EmailAPIForm(EmailActionMixin, Form):
    pass


class ZendeskAPIForm(ZendeskActionMixin, Form):
    pass
