# -*- coding: utf-8 -*-

from django.contrib import admin
from django_admin import DeleteOnlyModelAdmin
from django_onerror.models import OnerrorReportInfo


class OnerrorReportInfoAdmin(DeleteOnlyModelAdmin, admin.ModelAdmin):
    list_display = ('lineNo', 'columnNo', 'scriptURI', 'errorMessage', 'stack', 'created_at', 'updated_at')


admin.site.register(OnerrorReportInfo, OnerrorReportInfoAdmin)
