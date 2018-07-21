# Django
from django.contrib import admin
from django.utils.html import format_html

# local Django
from .models import DBLogEntry


class DBLogEntryAdmin(admin.ModelAdmin):

    list_display = ('level', 'message', 'formatted_trace', 'created_on')
    list_filter = ('level', 'created_on')
    list_per_page = 100

    @staticmethod
    def formatted_trace(instance):
        if instance.trace:
            traceback = instance.trace
        else:
            traceback = ''

        return format_html(
            '''<pre><code>{0}</code></pre>'''.format(traceback)
        )


admin.site.register(DBLogEntry, DBLogEntryAdmin)
