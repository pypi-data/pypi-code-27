from django import forms
from django.db.models import CharField, TextField, Q, ForeignKey

from .utils import SearchResult


__all__ = ["SearchResult", "SearchForm"]


class SearchForm(forms.Form):
    search_items = []
    search = forms.CharField(max_length=255)

    @classmethod
    def get_search_results(cls, search_text, filters=None, search_items=None):
        """Return a list of search results.

        Args:
            search_text (str): Test to search with
            filters (str/list)[None]: Names of models to use. Empty means use all given models
            search_items (list)[None]: List of models to use (filters argument will reduce the models searched).

        Returns:
            search_results (list): List of search results.
        """
        if search_items is None:
            search_items = cls.search_items

        if isinstance(filters, str):
            filters = [filt.strip() for filt in filters.split(",")]

        if filters is not None and len(filters) > 0:
            search_items = [item for item in search_items if item.model._meta.model_name.strip() in filters]

        search_results = []

        # Iterate over models and search
        for item in search_items:
            name = str(item)
            search_params = "ERROR"
            res = []
            try:
                name = item.model._meta.verbose_name
                search_params = item.get_search_params()
                res = item.filter_search(search_text).distinct()
                if len(res) == 0:
                    continue
            except (item.model.DoesNotExist, Exception) as err:
                print(err)
            search_results.append(SearchResult(res, name.title(), search_params, search_text))

        return search_results

    def search_fields(self, model, search_text, search_related=False):
        """Old search method for searching every text field in the model."""
        name = model._meta.verbose_name

        res = []
        try:
            model_fields = model._meta.get_fields()
            query = None
            for field in model_fields:
                if isinstance(field, (CharField, TextField)):
                    if query is None:
                        query = Q(**{field.name+"__icontains": search_text})
                    else:
                        query |= Q(**{field.name+"__icontains": search_text})

                elif search_related and isinstance(field, ForeignKey):
                    # Reverse foreign key search
                    n = field.name + "__"
                    for rel_f in field.related_model._meta.get_fields():
                        if isinstance(rel_f, (CharField, TextField)):
                            if query is None:
                                query = Q(**{n + rel_f.name + "__icontains": search_text})
                            else:
                                query |= Q(**{n + rel_f.name + "__icontains": search_text})

            res = model.objects.filter(query).distinct()
            if len(res) == 0:
                return None
        except (model.DoesNotExist, Exception):
            pass
        return SearchResult(res, name.title(), search_text)
