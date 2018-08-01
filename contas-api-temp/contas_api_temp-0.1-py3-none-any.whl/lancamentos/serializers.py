"""
Serializers a serem utilizadas em lancamentos/views.py
"""
from rest_framework import serializers
from lancamentos.models import Lancamento


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
