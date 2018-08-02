from django.contrib import admin
from django.urls import path
from qb.views import *

urlpatterns = [
    path('', PageView.as_view(), name="home"),
]
