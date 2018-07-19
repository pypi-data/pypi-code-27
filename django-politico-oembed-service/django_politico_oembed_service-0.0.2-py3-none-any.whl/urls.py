from django.urls import path

from .views import TwitterOembedView, YouTubeOembedView

urlpatterns = [
    path('twitter/', TwitterOembedView.as_view()),
    path('youtube/', YouTubeOembedView.as_view()),
]
