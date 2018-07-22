from sys import stderr
from typing import Type

from django.conf import settings
from django.db.models import Model
from django.utils.module_loading import autodiscover_modules
from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter


class RestRouter(DefaultRouter):
    _registered_serializers = {}

    def __init__(self, *args, **kwargs):
        skip_warning = kwargs.pop('skip_warning') or False
        if not skip_warning:
            print("You're instantiating RestRouter, you should probably use channels_redux.rest.router instead")
        super(RestRouter, self).__init__(*args, **kwargs)

    def get_default_base_name(self, viewset):
        """
        If `base_name` is not specified, attempt to automatically determine
        it from the viewset.
        """
        queryset = getattr(viewset, 'queryset', None)

        assert queryset is not None, '`base_name` argument not specified, and could ' \
                                     'not automatically determine the name from the viewset, as ' \
                                     'it does not have a `.queryset` attribute.'

        return queryset.model._meta.label_lower

    def register_model(self, model, serializer=None, viewset=None,
                       fields=None, exclude_fields=None, include_fields=None,
                       queryset=None, filter_func=None, url=None, permissions_classes=None):
        exclude_fields = exclude_fields or set()
        include_fields = include_fields or set()
        fields = self.get_default_fields_for_model(model, fields, exclude_fields, include_fields)

        serializer = serializer or self.get_default_serializer(model, fields)
        self._registered_serializers[model] = serializer
        if not issubclass(serializer, HyperlinkedModelSerializer):
            print("Serializer is not an instance of channels_redux.rest.HyperlinkedModelSerializer "
                  "unexpected behavior may occur", file=stderr)

        queryset = queryset or self.get_default_queryset(model)
        if viewset is None:
            viewset = self.get_default_viewset(queryset, serializer, filter_func, permissions_classes)
        else:
            viewset.serializer_class = serializer  # Ensure that the serializer on the viewset matches the one we expect

        if url is None:
            url = self.get_default_url(model)
        self.register(url, viewset)

    def get_default_queryset(self, model):
        return model.objects.all()

    def get_serializer(self, model):
        return self._registered_serializers[model]

    def get_default_url(self, model):
        return '/'.join((model._meta.app_label, model._meta.verbose_name_plural.replace(' ', '-')))

    def get_default_serializer(self, model_class, serializer_fields):
        class ModelSerializer(HyperlinkedModelSerializer):
            class Meta:
                model = model_class
                fields = serializer_fields
        return ModelSerializer

    def get_default_viewset(self, qs, serializer, filter_func, permissions):
        class ModelViewSet(viewsets.ModelViewSet):
            queryset = qs
            serializer_class = serializer
            permission_classes = permissions or tuple()

            def get_queryset(self):
                if filter_func is None:
                    return self.queryset
                return filter_func(self.queryset, self.request)
        return ModelViewSet

    def get_default_fields_for_model(self, model: Type[Model], fields, exclude_fields, include_fields):
        if fields is not None:
            updated_fields = set(fields)
            updated_fields.add('pk')
            updated_fields.add('url')
            return tuple(updated_fields)

        updated_fields = set(include_fields)
        excluded = set(exclude_fields)

        updated_fields.add('url')  # Always include this
        updated_fields |= model._meta._property_names  # This include pk as well as developer defined properties

        for field in model._meta.get_fields():
            if field.auto_created or field.name in excluded:  # Skip reverse relations
                continue
            updated_fields.add(field.name)

        return tuple(updated_fields)


def autodiscover():
    autodiscover_modules('rest', register_to=None)


router = RestRouter(skip_warning=True)


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    @staticmethod
    def fix_view_name(field_kwargs, model):
        if 'view_name' in field_kwargs:
            view_name_suffix = field_kwargs['view_name'].split('-')[-1]
            field_kwargs['view_name'] = "{}:{}-{}".format(settings.API_APP_NAMESPACE,
                                                          model._meta.label_lower,
                                                          view_name_suffix)
        return field_kwargs

    def build_url_field(self, field_name, model_class):
        field_class, field_kwargs = super().build_url_field(field_name, model_class)
        return field_class, self.fix_view_name(field_kwargs, self.Meta.model)

    def build_relational_field(self, field_name, relation_info):
        field_class, field_kwargs = super().build_relational_field(field_name, relation_info)
        return field_class, self.fix_view_name(field_kwargs, model=relation_info[1])
