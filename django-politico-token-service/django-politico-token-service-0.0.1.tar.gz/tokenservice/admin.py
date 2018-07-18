import uuid

from django.contrib import admin
from tokenservice.models import TokenApp


def regenerate_token(modeladmin, request, queryset):
    for app in queryset:
        app.token = uuid.uuid4().hex[:30]
        app.save()


regenerate_token.short_description = 'Regenerate app tokens'


class TokenAppAdmin(admin.ModelAdmin):
    fields = ('app_name', 'token')
    readonly_fields = ('token',)
    list_display = fields
    actions = (regenerate_token,)


admin.site.register(TokenApp, TokenAppAdmin)
