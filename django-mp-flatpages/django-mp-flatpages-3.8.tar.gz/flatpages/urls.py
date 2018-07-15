
from django.urls import path

from flatpages.views import flatpage


app_name = 'flatpages'


urlpatterns = [

    path('<str:url>/', flatpage, name='page')

]
