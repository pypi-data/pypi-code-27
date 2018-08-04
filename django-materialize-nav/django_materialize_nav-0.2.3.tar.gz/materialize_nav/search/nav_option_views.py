import copy
from django.http import JsonResponse
from django.urls import reverse
from dynamicmethod import dynamicmethod

from .utils import SearchItem
from .forms import SearchForm

from ..navigation.base_nav_options import BaseNavOptions


__all__ = ["SearchOptions"]


class SearchOptions(BaseNavOptions):
    AppName = ""
    SearchURL = None
    _SearchURL_CACHE_ = None
    SearchItems = []

    def __init__(self, *args, app_name=None, search_url=None, search_models=None, **kwargs):
        if app_name is not None:
            self.AppName = app_name
        if search_url is not None:
            self.SearchURL = search_url
        if search_models is not None:
            self.SearchItems = search_models
        else:
            self.SearchItems = copy.deepcopy(self.__class__.SearchItems)

        super().__init__(*args, **kwargs)

    @dynamicmethod
    def add_search_model(self, model, lookup_expr, **lookup_kwargs):
        """Add a model and lookup expression to search with. The lookup expression can be a Q or a list of strings to
        be or'ed together.
        
        Args:
            model (django.db.model): Model to search.
            lookup_expr (str/list): lookup expression or list of lookup expressions
            **lookup_kwargs (dict): Dictionary of lookups that are and'ed with the lookup_expr
        """
        self.SearchItems.append(SearchItem(model, lookup_expr, lookup_kwargs))

    @dynamicmethod
    def get_search_items(self):
        return [item for item in self.SearchItems]

    @dynamicmethod
    def get_search_models(self):
        return [item.model for item in self.SearchItems]

    @dynamicmethod
    def get_context(self, request, search_url=None, search_models=None, **kwargs):
        context = super().get_context(request, **kwargs)

        # Search url
        if search_url is None:
            search_url = self._SearchURL_CACHE_
            if not search_url:
                search_url = self.SearchURL
                try:
                    search_url = reverse(search_url)
                except:
                    try:
                        search_url = search_url.get_absolute_url()
                    except:
                        pass
                self._SearchURL_CACHE_ = search_url

        if search_models is None:
            search_models = self.get_search_models()

        # Search
        if search_url:
            try:
                app_name = " " + self.AppName
            except AttributeError:
                app_name = ""
            context["SearchURL"] = search_url
            context["SearchName"] = "Search" + app_name
            context["SearchFilters"] = [str(model._meta.model_name).strip() for model in search_models]
            context["SearchForm"] = SearchForm()

        return context
