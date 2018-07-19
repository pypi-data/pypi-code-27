from rest_framework import authentication, exceptions
from tokenservice.models import TokenApp


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Per DRF token auth, token is prefixed by string
        # literal "Token" plus whitespace, e.g., "Token <AUTHTOKEN>"
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        except Exception:
            raise exceptions.AuthenticationFailed('No authorization header')
        if not token:
            raise exceptions.AuthenticationFailed(
                'No token or incorrect token format')

        try:
            app = TokenApp.objects.get(token=token)
        except TokenApp.DoesNotExist:
            raise exceptions.AuthenticationFailed('Unauthorized')

        return (app, None)
