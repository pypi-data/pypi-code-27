"""
Permissões a serem utilizadas em contas/views.py
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permissão para que somente os donos da conta/lancamento
    possam visualiza-los e/ou altera-los
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
