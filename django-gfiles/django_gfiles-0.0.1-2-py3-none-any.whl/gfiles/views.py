# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import os


from django.http import JsonResponse
from celery.result import AsyncResult

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, MultiTableMixin

from gfiles.models import GenericFile
from gfiles.forms import GFileForm
from django.shortcuts import render

from gfiles.filter import GFileFilter
from gfiles.tables import GFileTableWithCheck

from django_tables2.export.views import ExportMixin
from django.urls import reverse_lazy


class GFileCreateView(LoginRequiredMixin, CreateView):
    """ Class to create a save a generic file using the GenericFile model.

    Inherits the CreateView class and uses the LoginRequiredMixin
    """
    model = GenericFile
    success_msg = "File uploaded"
    success_url = reverse_lazy('success')
    form_class = GFileForm
    template_name = 'gfiles/gfile_form.html'

    def update_form(self, form):
        ofn = self.request.FILES['data_file'].name
        form.instance.original_filename = ofn
        form.instance.user = self.request.user
        return form

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form = self.update_form(form)
        return super(GFileCreateView, self).form_valid(form)


class GFileListView(ExportMixin, SingleTableMixin, FilterView):
    """ Class to view a table and filter all of the currently saved GenericFiles

    Inherits the FilterView class and uses the SingleTableMixin for viewing the django-tables2 table and
    uses the ExportMixin so that the table can be exported as a csv file
    """
    table_class = GFileTableWithCheck
    model = GenericFile
    template_name = 'gfiles/gfile_summary.html'
    filterset_class = GFileFilter


def status_update(request):
    """ Updates for tracking status of long processes via celery
    """

    id = request.session['result']

    result = AsyncResult(id)

    status = result.status

    if status == 'FAILURE':
        progress = 0
    elif status == 'SUCCESS':
        progress = 100
    elif result.info:
        progress = (float(result.info['current'])/float(result.info['total']))*100.0
    else:
        progress = 0

    return JsonResponse({'s': status, 'progress':progress, 'info':str(result.info)})


def index(request):
    """ basic index view
    """
    return render(request, 'gfiles/index.html')


def success(request):
    """ basic success view
    """
    return render(request, 'gfiles/success.html')