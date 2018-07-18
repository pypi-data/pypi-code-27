from rest_framework import serializers
from datapunt_api.rest import HALSerializer, SelfLinkSerializerMixin

from tests import models


class WeatherStationSerializer(HALSerializer):
    class Meta:
        model = models.WeatherStation
        fields = '__all__'


class TemperatureRecordSerializer(HALSerializer):
    class Meta:
        model = models.TemperatureRecord
        fields = '__all__'
