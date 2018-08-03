import webapp2

from google.appengine.ext import ndb

from restae.handlers import APIModelHandler
from restae.router import Router
from restae.serializers import ModelSerializer
from restae.response import JsonResponse
from restae.decorators import action


class User(ndb.Model):
    email = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Handler(APIModelHandler):
    queryset = User.query()
    serializer_class = UserModelSerializer

    @action(methods=['GET'], detail=True)
    def toto(self, *args, **kwargs):
        return JsonResponse(data={'ok': 42})


router = Router()
router.register('user', Handler)

app = webapp2.WSGIApplication(router.urls)
