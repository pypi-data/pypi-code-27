from django.contrib import admin
from django.apps import apps
from django.conf import settings

# Register your models here.
from qb.models import *

class QueryInline(admin.TabularInline):
    fields = ('join', 'field_verbose_name', 'filter_criteria', 'filter_value')
    model = Query
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        form = super().get_formset(request, obj, **kwargs)
        choicelist = []
        for _app in settings.QB_APPS:
            print(_app)
            app_models = apps.get_app_config(_app).get_models()
            for model in app_models:
                if not hasattr(model._meta, 'qb'):
                    for field in model._meta.fields:
                        field_dets = '%s - %s' % (field.name, model._meta.verbose_name)
                        choicelist.append((field.name, field_dets))
            # obj.model_verbose_name.choices = choicelist
            # print(choicelist)
        Query._meta.get_field('field_verbose_name').choices = choicelist
        # form.fields["field_verbose_name"].choices = choicelist
        return form

class FeatureAdmin(admin.ModelAdmin):
    """ Admin class for Features """
    list_display = ['name', 'slug', 'model_verbose_name', 'template']
    inlines = [
        QueryInline,
    ]
    list_per_page = 10

    def get_form(self, request, obj=None, **kwargs):
        choicelist = []
        fieldlist = []
        for _app in settings.QB_APPS:
            app_models = apps.get_app_config(_app).get_models()
            for model in app_models:
                if not hasattr(model._meta, 'qb'):
                    choicelist.append((model._meta.verbose_name , model._meta.verbose_name))

                    # update field names for order functionality
                    for field in model._meta.fields:
                        field_dets = '%s - %s' % (field.name, model._meta.verbose_name)
                        fieldlist.append((field.name, field_dets))
            # obj.model_verbose_name.choices = choicelist
            # print(choicelist)
        Feature._meta.get_field('model_verbose_name').choices = choicelist
        Feature._meta.get_field('order_by').choices = fieldlist

        return super(FeatureAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Feature, FeatureAdmin)
# admin.site.register(Contact)
