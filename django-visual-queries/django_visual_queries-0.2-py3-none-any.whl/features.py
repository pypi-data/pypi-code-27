from django.shortcuts import render, redirect, render_to_response
from django.views import generic
from qb.models import *
from django.conf import settings
from django.apps import apps
from django.db.models import Q

# Create your views here.
class Features():

    def getft_queryset(self, slug):
        feature = Feature.objects.get(slug=slug)
        model_name = feature.model_verbose_name
        queries = feature.query_set.all()
        order_field = 'id'
        params = Q()
        for q in queries:
            # print(q.filter_criteria)
            fc = ''
            if q.filter_criteria == 'Greater Than':
                fc = '__gte'
            if q.filter_criteria == 'Less Than':
                fc = '__lte'
            if q.filter_criteria == 'Contains':
                fc = '__contains'
            
            if q.filter_value == 'None':
                fv = None
            else:
                fv = q.filter_value
            
            if feature.order_by != "" and not feature.order_asc:
                order_field = feature.order_by
            elif feature.order_by != "" and feature.order_asc:
                order_field = '-%s' % feature.order_by

            kwargs = {
                "{fbn}{fc}".format(fbn=q.field_verbose_name, fc=fc): fv
            }
            if q.join == "AND":
                params = params & Q(**kwargs)
            else:
                params = params | Q(**kwargs)

        # print (params)       
        model = self.getModelInst(model_name)
        if feature.limit > 0:
            queryset = model.objects.filter(params).order_by(order_field)[:feature.limit]
        else:
            queryset = model.objects.filter(params).order_by(order_field)

        return queryset

    def getModelInst(self, model_name):
        for _app in settings.QB_APPS:
            app_models = apps.get_app_config(_app).get_models()
            res = False
            for model in app_models:
                if not hasattr(model._meta, 'qb'):
                    if model._meta.verbose_name == model_name:
                        res = model
            return res
