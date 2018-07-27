"""oauth validators for lti."""

import logging
from oauthlib.oauth1 import RequestValidator
from oauthlib.oauth1 import SIGNATURE_HMAC
from oauthlib.common import to_unicode
import redis

from django.conf import settings
from django.http import HttpRequest

from .models import Consumer

log = logging.getLogger(__name__)

NONCE_TTL = 3600 * 6

class LTIRequestValidator(RequestValidator):

    @property
    def enforce_ssl(self):
        return getattr(settings, 'HXLTI_ENFORCE_SSL', False)

    @property
    def dummy_client(self):
        client = settings.HXLTI_DUMMY_CONSUMER_KEY
        return to_unicode(client)

    @property
    def dummy_secret(self):
        c = self._get_consumer(self.dummy_client)
        if c:
            return to_unicode(c.secret_key)  # make sure secret val is unicode
        return self.dummy_client


    def check_client_key(self, key):
        # redefine: any non-empty string is OK as a client key
        return len(key) > 0


    def check_nonce(self, nonce):
        # redefine: any non-empty string is OK as a nonce
        return len(nonce) > 0


    def validate_client_key(self, client_key, request):
        c = self._get_consumer(client_key)
        return c is not None


    def validate_timestamp_and_nonce(
        self, client_key, timestamp, nonce,
        request, request_token=None, access_token=None):

        try:
            r = redis.from_url(settings.HXLTI_REDIS_URL)
            r.ping()
        except redis.ConnectionError as e:
            raise ImproperlyConfigured("redis connect failure: " + str(e))

        exists = r.getset('hxlti_nonce:' + nonce, timestamp)
        if exists:
            log.debug("nonce already exists: %s", nonce)
            return False
        else:
            log.debug("unused nonce, storing: %s", nonce)
            r.expire('hxlti_nonce:' + nonce,
                     int(timestamp) + self.timestamp_lifetime)
            return True


    def _get_consumer(self, client_key):
        query = Consumer._default_manager.filter(consumer=client_key)
        return query[0] if query.count() == 1 else None


    def get_client_secret(self, client_key, request):
        c = self._get_consumer(client_key)
        if c:
            return to_unicode(c.secret_key)  # make sure secret val is unicode
        return self.dummy_secret


