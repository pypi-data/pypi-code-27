# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import logging
from django import template
from django.conf import settings

logger = logging.getLogger(__name__)
register = template.Library()


class UF:
    @classmethod
    def get(cls, format_response: str='json', date: str=None, callback: str=None):
        endpoint = '{endpoint}uf/'.format(endpoint=settings.SBIF_ENDPOINT)
        data = {
            'apikey': settings.SBIF_APIKEY,
            'formato': format_response,
        }
        try:
            if callback:
                data['callback'] = callback

            return requests.get(url=endpoint, params=data)
        except Exception as e:
            logger.exception('SBIF Request Exception: {error}'.format(error=e))
            return None