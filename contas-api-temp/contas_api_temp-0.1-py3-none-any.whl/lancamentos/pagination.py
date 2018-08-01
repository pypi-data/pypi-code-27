"""
Paginação a ser utilizada em lancamento/views.py
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LancamentoPagination(PageNumberPagination):
    """
    Paginação customizada para que fosse possível retornar um Response
    com todos os dados necessários para a renderização da URL
    lancamento-list
    """
    def get_paginated_response(self, data, ext_inf):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'extra_info': ext_inf,
        })
