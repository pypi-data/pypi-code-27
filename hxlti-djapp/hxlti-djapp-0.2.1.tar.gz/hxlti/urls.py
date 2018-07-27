
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^launch/', views.lti_landing_page, name='lti_landing'),
]


