from django.conf import settings
from rest_framework import serializers
from rest_framework import routers


class RestRouter(routers.DefaultRouter):
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
