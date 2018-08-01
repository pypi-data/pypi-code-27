"""
Criado automaticamente pelo comando:
$ django-admin startapp contasOrama
"""
from django.contrib import admin
from contasOrama.models import Conta, Lancamento

admin.site.register(Conta)
admin.site.register(Lancamento)
