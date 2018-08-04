import json
import collections
from django.forms import widgets
from django.urls import reverse

__all__ = ['AutocompleteWidget']


class AutocompleteWidget(widgets.Select):
    input_type = 'select'
    template_name = 'materialize_nav/forms/widgets/autocomplete.html'

    class Media:
        js = ('materialize_nav/autocomplete.js',)

    def __init__(self, queryset=(), url=None, url_args=(), url_kwargs=None, query_name="q", attrs=None):
        self.queryset = queryset
        self.url = url
        self.url_args = url_args
        self.url_kwargs = url_kwargs
        self.query_name = query_name
        super().__init__(attrs=attrs)

    def get_url(self):
        url = self.url
        if url is not None:
            try:
                url = reverse(url, args=self.url_args or (), kwargs=self.url_kwargs or {})
            except:
                try:
                    url = url.get_absolute_url()
                except:
                    pass
        return url

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['url'] = self.get_url()
        context['widget']['data'] = [(item.id, str(item)) for item in self.queryset]
        context['widget']['has_div'] = getattr(self, "has_div", False)
        if self.query_name:
            context['widget']['query_name'] = str(self.query_name)
        if self.queryset:
            context['widget']['options'] = json.dumps(collections.OrderedDict([(val.id, str(val)) for val in self.queryset]))
        return context

    # def render(self, name, value, attrs=None, renderer=None):
    #     """Render the widget as an HTML string."""
    #     context = self.get_context(name, value, attrs)
    #     return self._render(self.template_name, context, renderer)
