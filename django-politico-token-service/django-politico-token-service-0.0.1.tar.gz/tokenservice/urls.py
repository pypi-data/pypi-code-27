from django.urls import path

from .views import AuthTestView

urlpatterns = [
    path('test/', AuthTestView.as_view()),
]
