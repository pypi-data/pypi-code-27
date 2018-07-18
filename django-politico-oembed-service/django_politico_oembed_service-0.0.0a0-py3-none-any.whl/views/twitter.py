import requests

from oembedservice.conf import settings
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView


class TwitterOembedView(APIView):
    authentication_classes = (settings.API_AUTHENTICATION_CLASS,)
    permission_classes = (settings.API_PERMISSION_CLASS,)

    def post(self, request):
        url = request.data.get('url', None)
        if not url:
            raise ParseError('No url')
        r = requests.get('https://publish.twitter.com/oembed', params={
            "url": url
        })
        if r.status_code == 200:
            return Response(r.json())
        raise NotFound('Tweet not found')
