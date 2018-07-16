from . import BaseEndpointTestCase


class TemplateEndpointTestCase(BaseEndpointTestCase):
    def test_template_get(self):
        self.client._credentials = (
            '2zSiihsjuX5Eas6wv9kFAellKJk3CvS3xqcz7Uim',
            'uJJaW9AcwJhkKHXH6b9XkwWpYGwz6DrS7lALOzuh8NmRn0HUwqUMVmjwZXMn9BTFxy3WNNjk9GROYJ5efPmmvV3l99JsazvMILHJPKm0vC3obWXtr9yKIbmtAh7czhXG'
        )

        template = self.client.Templates.get('new_requisition_default')
        print(template.id)
        assert template
