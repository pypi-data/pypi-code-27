"""
Serializers a serem utilizadas em contas/views.py
"""
from rest_framework import serializers

from contas.models import Conta


class ContaSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer para preencher novas contas e vincular aos donos.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    lancamentos = serializers.HyperlinkedRelatedField(
        many=True, view_name='lancamento-detail', read_only=True)

    class Meta:
        model = Conta
        fields = ('url', 'id', 'name', 'description', 'owner', 'lancamentos')
