from django.urls import path

from .views import TwitterOembedView, YouTubeOembedView

app_name = 'oembedservice'
urlpatterns = [
    path('twitter/', TwitterOembedView.as_view(), name="twitter"),
    path('youtube/', YouTubeOembedView.as_view(), name="youtube"),
]
