"""
Criado automaticamente pelo comando:
$ django-admin startapp usuarios
"""
from django.contrib import admin
from contas.models import Conta

admin.site.register(Conta)
