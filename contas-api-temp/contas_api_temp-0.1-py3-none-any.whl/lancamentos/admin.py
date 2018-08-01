"""
Criado automaticamente pelo comando:
$ django-admin startapp usuarios
"""
from django.contrib import admin
from lancamentos.models import Lancamento

admin.site.register(Lancamento)
