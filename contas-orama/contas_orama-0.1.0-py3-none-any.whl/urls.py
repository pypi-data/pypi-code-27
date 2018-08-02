"""
URLs da API
"""
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from contas_orama import views

SCHEMA_VIEW = get_schema_view(title="Contas API")

urlpatterns = [
    url(r'^contas/$', views.ContaList.as_view(), name='conta-list'),
    url(r'^contas/(?P<pk>[0-9]+)/$',
        views.ContaDetail.as_view(), name='conta-detail'),
    url(r'^contas/(?P<pk>[0-9]+)/novo-lancamento/$',
        views.LancamentoCreate.as_view(),
        name='lancamento-create'),
    url(r'^lancamento/(?P<pk>[0-9]+)$',
        views.LancamentoDetail.as_view(),
        name='lancamento-detail'),
    url(r'^contas/(?P<pk>[0-9]+)/lancamentos/(?P<ini>.+)/(?P<end>.+)/$',
        views.LancamentoList.as_view(),
        name='lancamento-list'),
    url(r'^$', views.api_root),
    url(r'^usuarios/$', views.UserList.as_view(), name='user-list'),
    url(r'^usuarios/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
        name='user-detail'),
]

# URL PARA O LOGIN DO USUÁRIO
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls'), name='login')
]

urlpatterns = format_suffix_patterns(urlpatterns)
