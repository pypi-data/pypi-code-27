from datapunt_api.rest import DatapuntViewSet

from tests.models import WeatherStation
from tests.models import TemperatureRecord
from tests.serializers import WeatherStationSerializer
from tests.serializers import TemperatureRecordSerializer


class WeatherStationViewSet(DatapuntViewSet):
    serializer_class = WeatherStationSerializer
    serializer_detail_class = WeatherStationSerializer
    queryset = WeatherStation.objects.all().order_by('id')


class TemperatureRecordViewSet(DatapuntViewSet):
    serializer_class = TemperatureRecordSerializer
    serializer_detail_class = TemperatureRecordSerializer
    queryset = TemperatureRecord.objects.all().order_by('date')
