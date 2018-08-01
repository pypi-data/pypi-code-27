"""
Serializers a serem utilizadas em contas/views.py
"""
from django.contrib.auth.models import User
from rest_framework import serializers

from contasOrama.models import Conta, Lancamento


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


class LancamentoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer para preencher novos lançamentos e vincular
    contas e donos.
    """
    conta = serializers.ReadOnlyField(source='conta.id')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Lancamento
        fields = ('url', 'id', 'name', 'value', 'date', 'lanc_tp',
                  'conta', 'owner')


class DateFilterSerializer(serializers.Serializer):
    """
    Serializer para preencher datas que filtrarão os lançamentos.
    De modo a formar um extrato.
    """
    def validate(self, data):
        """
        Função para se certificar que a data inicial é anterior a data final
        """
        if data['data_ini'] > data['data_end']:
            raise serializers.ValidationError("Data final deve ser posterior \
                                               a data inicial")
        return data

    data_ini = serializers.DateField('Data Inicial:')
    data_end = serializers.DateField('Data Final:')


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
