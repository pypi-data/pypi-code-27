from django.urls import path

from .views import AuthTestView

app_name = 'tokenservice'
urlpatterns = [
    path('test/', AuthTestView.as_view(), name='test'),
]
