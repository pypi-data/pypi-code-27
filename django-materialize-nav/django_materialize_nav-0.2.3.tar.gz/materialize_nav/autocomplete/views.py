import collections
from django.db.models import Q
from django.http import JsonResponse

from ..navigation.template_mixin import TemplateMixin


__all__ = ['AutocompleteView']


class AutocompleteView(TemplateMixin):
    model = None
    query_name = "q"
    lookup_expr = "name__istartswith"  # ['name__icontains', 'description__icontains']

    def get_queryset(self):
        """Return the general queryset for all objects."""
        return self.model.objects.all()

    def get_lookup_expr(self):
        """Return a list of names to use for the query filter."""
        if isinstance(self.lookup_expr, (list, tuple)):
            return self.lookup_expr
        return [self.lookup_expr]

    def filter_queryset(self, qs, q):
        """Filter and return the new queryset.

        Args:
            qs (QuerySet): Queryset that needs to be filtered.
            q (str): Query value that was the query_name GET parameter

        Returns:
            qs (QuerySet): The filtered queryset to use.
        """
        if q:
            query = Q()
            for lookup in self.get_lookup_expr():
                query = query | Q(**{lookup: q})
            qs = qs.filter(query)
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        q = request.GET.get(self.query_name, None)
        if q:
            qs = self.filter_queryset(qs, q)
        data = collections.OrderedDict([(obj.id, str(obj)) for obj in qs])
        return JsonResponse(data, status=200)
