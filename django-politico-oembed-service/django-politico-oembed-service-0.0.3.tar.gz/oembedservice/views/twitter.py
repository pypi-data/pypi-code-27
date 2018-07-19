import requests
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from oembedservice.conf import settings
from oembedservice.utils.validators import check_domain


def truthy(value):
    """
    Checks for twitter's valid "truthy" values.
    """
    value = value.lower()
    if value == 't' or value == 'true' or value == '1':
        return True
    return False


class TwitterOembedView(APIView):
    authentication_classes = (settings.API_AUTHENTICATION_CLASS,)
    permission_classes = (settings.API_PERMISSION_CLASS,)

    def post(self, request):
        url = request.data.get('url', None)
        if not url:
            raise ParseError('No url')
        if not check_domain(url, domain="twitter.com"):
            raise ParseError('Invalid url')
        print(request.data)
        maxwidth = int(request.data.get('maxwidth', 550))
        hide_media = truthy(request.data.get('hide_media', 'f'))
        hide_thread = truthy(request.data.get('hide_thread', 'f'))
        omit_script = truthy(request.data.get('omit_script', 'f'))
        link_color = request.data.get('link_color', '%2355acee')
        r = requests.get('https://publish.twitter.com/oembed', params={
            "url": url,
            "maxwidth": maxwidth,
            "hide_media": hide_media,
            "hide_thread": hide_thread,
            "omit_script": omit_script,
            "link_color": link_color,
        })
        if r.status_code == 200:
            return Response(r.json())
        raise NotFound('Tweet not found')
