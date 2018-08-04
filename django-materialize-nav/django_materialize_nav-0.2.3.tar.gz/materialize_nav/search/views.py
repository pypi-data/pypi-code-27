from django.http import JsonResponse
from dynamicmethod import dynamicmethod

from .forms import SearchForm
from .nav_option_views import SearchOptions
from ..navigation.views import BaseNavView


__all__ = ["SearchNavView", "SearchView"]


class SearchNavView(SearchOptions, BaseNavView):
    SearchURL = None
    SearchItems = []

    @dynamicmethod
    def get_context(self, request, context=None, title=None, page_title=None, show_page_title=None, home_url=None,
                    nav_color=None, nav_items=None,
                    show_sidebar=None, fixed_sidebar=None, container_on=None, side_panel=None,
                    search_url=None, search_items=None,
                    notification=None, notification_classes=None, notification_time=None, **kwargs):

        return super().get_context(request, context=context, title=title, page_title=page_title,
                                   show_page_title=show_page_title, home_url=home_url,
                                   nav_color=nav_color, nav_items=nav_items,
                                   show_sidebar=show_sidebar, fixed_sidebar=fixed_sidebar, container_on=container_on,
                                   side_panel=side_panel,
                                   search_url=search_url, search_items=search_items,
                                   notification=notification, notification_classes=notification_classes,
                                   notification_time=notification_time, **kwargs)


class SearchView(SearchNavView):
    """Search through multiple models.

    Still need to think this one through a little bit. The SearchForm seems pointless.

    Note:
        search_results contains a list of list of SearchResult's.
            Ex. [SearchResult(QuerySet, Model, "Searched Text"), SearchResult(QuerySet, Model, "Searched Text")],]

    Note:
        If Ajax is used this returns the json object which is a list of [[String value, URL]].
        {search_results: [["[Model] value1", url1], ["[Model 2] value2", url2]]}
    """
    PageTitle = "Search Results"
    template_name = 'materialize_nav/search_results.html'
    context_object_name = 'search_results'
    search_form = SearchForm
    paginate_by = 10

    @dynamicmethod
    def add_search_model(self, model):
        return super().add_search_model(model)

    @dynamicmethod
    def get_search_models(self):
        return super().get_search_models()

    def get_context_object_name(self):
        """Get the name of the item to be used in the context."""
        if self.context_object_name:
            return self.context_object_name
        return "search_results"

    @classmethod
    def get_object_url(cls, obj):
        try:
            return obj.get_absolute_url()
        except:
            return ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "GET":
            request_dict = self.request.GET
        else:
            request_dict = self.request.POST

        # search_form = self.search_form(request_dict)
        search_results = self.search_form.get_search_results(request_dict.get("search", ""),
                                                             request_dict.get("filters", []),
                                                             self.get_search_items())
        context[self.get_context_object_name()] = search_results

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            context_name = self.get_context_object_name()
            li = []
            for sr in context[context_name]:
                li.extend([[str(res) + " [" + str(sr.model) + "]", self.get_object_url(res)]
                           for res in sr.results[: self.paginate_by]])
            return JsonResponse({context_name: li}, status=200)
        else:
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            context_name = self.get_context_object_name()
            li = []
            for sr in context[context_name]:
                li.extend([[str(res) + " [" + str(sr.model) + "]", self.get_object_url(res)]
                           for res in sr.results[: self.paginate_by]])
            return JsonResponse({context_name: li}, status=200)
        else:
            return self.render_to_response(context)
