from django.db.models import Q

from ..navigation.utils import list_property


__all__ = ['SearchResult', 'list_property']


class SearchItem(list):
    model = list_property(0, None)
    lookup_expr = list_property(1, "")
    lookup_kwargs = list_property(2, None)

    def __init__(self, model, lookup_expr, lookup_kwargs):
        if lookup_kwargs is None:
            lookup_kwargs = {}
        super().__init__((model, lookup_expr, lookup_kwargs))

    def get_search_params(self):
        lookup_expr = self.lookup_expr
        if isinstance(self.lookup_expr, str):
            lookup_expr = [self.lookup_expr]

        try:
            lookup_str = " | ".join(("%s%s" % (str(lookup)[0].title(), str(lookup)[1:].replace("__", "_").replace("_", " ")) for lookup in lookup_expr))
            if self.lookup_kwargs:
                return "".join(("(", lookup_str, ") && ", " & ".join((str(key) + " = " + str(val)
                                                                      for key, val in self.lookup_kwargs.items()))))

            return lookup_str
        except:
            return "ERROR"

    def get_lookup(self, filter_text):
        if isinstance(self.lookup_expr, str):
            return Q(**{self.lookup_expr: filter_text})
        elif isinstance(self.lookup_expr, (list, tuple, dict)):
            q = Q()
            for lookup in self.lookup_expr:
                q |= Q(**{lookup: filter_text})
            return q
        else:
            return Q()

    def filter_search(self, search_text):
        return self.model.objects.filter(self.get_lookup(search_text), **self.lookup_kwargs)


class SearchResult(list):
    """Search results. Stores information about a search.

    Args:
        results (QuerySet): Result queryset
        model (str): Model name.
        search_text (str): Test that was used in the search.
    """
    results = list_property(0, [])
    model = list_property(1, None)
    search_params = list_property(2, "")
    search_text = list_property(3, "")

    def __init__(self, results, model, search_params, search_text):
        super().__init__((results, model, search_params, search_text))
