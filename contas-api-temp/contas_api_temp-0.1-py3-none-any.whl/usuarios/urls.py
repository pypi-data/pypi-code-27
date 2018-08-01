"""
URLs relacionadas aos usuários
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from usuarios import views

SCHEMA_VIEW = get_schema_view(title="Contas API")

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^usuarios/$', views.UserList.as_view(), name='user-list'),
    url(r'^usuarios/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
        name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
