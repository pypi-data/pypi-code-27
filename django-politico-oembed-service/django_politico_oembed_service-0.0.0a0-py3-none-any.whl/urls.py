from django.urls import path

from .views import TwitterOembedView

urlpatterns = [
    path('oembed/twitter/', TwitterOembedView.as_view()),
]
