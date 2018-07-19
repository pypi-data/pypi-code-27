# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import redirect
from django_six import MiddlewareMixin


class SiteMaintainMiddleware(MiddlewareMixin):

    def process_request(self, request):
        yes_or_not = hasattr(settings, 'DJANGO_SITE_MAINTAIN') and settings.DJANGO_SITE_MAINTAIN

        # Set as maintain + Not in whitelist + Not superuser
        if yes_or_not and (not (hasattr(request, 'user') and request.user.is_superuser)):
            # TODO: Set notice_url when ``DJANGO_SITE_MAINTAIN_NOTICE_URL`` not exists
            # TODO: Support notice_url be template etc...
            notice_url = settings.DJANGO_SITE_MAINTAIN_NOTICE_URL if hasattr(settings, 'DJANGO_SITE_MAINTAIN_NOTICE_URL') else ''
            return redirect(notice_url)

        return None
