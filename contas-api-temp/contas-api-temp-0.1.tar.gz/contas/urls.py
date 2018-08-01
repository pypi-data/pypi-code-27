"""
URLs relacionadas aos lançamentos
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from contas import views

SCHEMA_VIEW = get_schema_view(title="Contas API")

urlpatterns = [
    url(r'^contas/$', views.ContaList.as_view(), name='conta-list'),
    url(r'^contas/(?P<pk>[0-9]+)/$',
        views.ContaDetail.as_view(), name='conta-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
