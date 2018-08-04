from django import forms

from .widgets import AutocompleteWidget


__all__ = ['AutocompleteWidget', 'AutocompleteField']


class AutocompleteField(forms.ModelChoiceField):
    widget = AutocompleteWidget

    def __init__(self, queryset=(), url=None, url_args=None, url_kwargs=None, query_name="q", *args, **kwargs):
        if "label" not in kwargs:
            kwargs["label"] = ''

        if "widget" not in kwargs:
            kwargs['widget'] = self.widget(queryset=queryset, url=url, url_args=url_args, url_kwargs=url_kwargs, query_name=query_name)
        super().__init__(*args, **kwargs)
