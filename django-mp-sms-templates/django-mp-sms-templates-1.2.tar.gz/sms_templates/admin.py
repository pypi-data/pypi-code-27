
from importlib import import_module

from django.apps import apps
from django.urls import path
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy

from sms_templates.models import SMSTemplate
from sms_templates.forms import SendSMSForm

# TODO: remove turbosms dependency
from turbosms.lib import send_sms


def _get_sms_template_admin_base_class():

    if apps.is_installed('modeltranslation'):
        return import_module('modeltranslation.admin').TranslationAdmin

    return admin.ModelAdmin


class SMSTemplateAdmin(_get_sms_template_admin_base_class()):

    list_display = ['name', 'slug', 'get_item_actions']
    search_fields = ['name', 'slug', 'recipients', 'text']

    def get_readonly_fields(self, request, obj=None):
        return ['placeholders'] if obj else []

    def get_urls(self):

        return [
            path('<int:object_id>/send/', self.send_sms_template, name='send-sms'),
        ] + super(SMSTemplateAdmin, self).get_urls()

    def send_sms_template(self, request, object_id):

        template = get_object_or_404(SMSTemplate, pk=object_id)

        form = SendSMSForm(request.POST or None, instance=template)

        if request.method == 'POST' and form.is_valid():
            data = form.cleaned_data
            send_sms(data['text'], data['recipients'])
            messages.success(request, _('SMS was sent'))
            return redirect('admin:smstemplates_smstemplate_changelist')

        return render(request, 'sms_templates/send_sms.html', {'form': form})

    def get_item_actions(self, item):
        return render_to_string('sms_templates/list_item_actions.html', {
            'object': item
        })

    get_item_actions.allow_tags = True
    get_item_actions.short_description = _('Actions')


admin.site.register(SMSTemplate, SMSTemplateAdmin)
