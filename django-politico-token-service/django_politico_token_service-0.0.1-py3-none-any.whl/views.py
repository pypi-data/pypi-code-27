from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tokenservice.authentication import TokenAuthentication


class TokenAuthedAPIView(APIView):
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated,
    )


class AuthTestView(TokenAuthedAPIView):
    def get(self, request, format=None):
        return Response('GET request authentication succeeded.')

    def post(self, request, format=None):
        return Response('POST request authentication succeeded.')
