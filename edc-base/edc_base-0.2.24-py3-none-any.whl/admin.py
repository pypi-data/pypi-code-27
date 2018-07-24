from django.contrib import admin
from django.contrib.auth.models import User

from .auth.admin import UserAdmin


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
