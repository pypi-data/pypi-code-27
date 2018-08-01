"""
URLs relacionadas aos lançamentos
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from lancamentos import views

SCHEMA_VIEW = get_schema_view(title="Contas API")

urlpatterns = [
    url(r'^contas/(?P<pk>[0-9]+)/novo-lancamento/$',
        views.LancamentoCreate.as_view(),
        name='lancamento-create'),
    url(r'^lancamento/(?P<pk>[0-9]+)$',
        views.LancamentoDetail.as_view(),
        name='lancamento-detail'),
    url(r'^contas/(?P<pk>[0-9]+)/lancamentos/(?P<ini>.+)/(?P<end>.+)/$',
        views.LancamentoList.as_view(),
        name='lancamento-list')
]

urlpatterns = format_suffix_patterns(urlpatterns)
