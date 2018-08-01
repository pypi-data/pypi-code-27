"""
Serializers a serem utilizadas em usuarios/views.py
"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer para preencher novos usuários e vincular as
    contas aos mesmos
    """
    contas = serializers.HyperlinkedRelatedField(many=True,
                                                 view_name='conta-detail',
                                                 read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'contas')
