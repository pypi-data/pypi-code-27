# coding: utf-8

#Import Models

from djangocms_partners.models import Partner
from django import template

register = template.Library()

@register.assignment_tag
def list_partners():
    partners = Partner.objects.all().order_by('name')
    return partners

