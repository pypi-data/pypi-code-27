from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('authen/', include("authen.urls")),
    path('admin/', admin.site.urls),
]
