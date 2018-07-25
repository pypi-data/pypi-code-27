
from functools import wraps

import logging

from lti.contrib.django import DjangoToolProvider
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden

from .validators import LTIRequestValidator


def require_lti_launch(view_func):
    def _decorator(request, *args, **kwargs):
        # is this an lti launch request?
        # https://www.imsglobal.org/recipe-making-lti-1-tool-providers
        if request.method == 'POST':
            is_basic_lti_launch = \
                    request.POST.get('lti_message_type', '') == \
                    'basic-lti-launch-request'
            has_lti_version = request.POST.get('lti_version', '') == 'LTI-1p0'
            oauth_consumer_key = request.POST.get('oauth_consumer_key', None)
            resource_link_id = request.POST.get('resource_link_id', None)
        else:
            return HttpResponseBadRequest()

        if not (is_basic_lti_launch and has_lti_version and \
                oauth_consumer_key and resource_link_id):
            return HttpResponseBadRequest()

        # lti request authentication
        validator = LTIRequestValidator()
        tool_provider = DjangoToolProvider.from_django_request(
            secret=validator.get_client_secret(oauth_consumer_key, request),
            request=request)

        valid_lti_request = tool_provider.is_valid_request(validator)

        if valid_lti_request:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return HttpResponseForbidden()

    return wraps(view_func)(_decorator)


