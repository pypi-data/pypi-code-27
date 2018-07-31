class Device:
    """Entity used to store device information."""

    def __init__(self, data, license_plate):
        """Initialize a RitAssist device, also a vehicle."""
        self.attributes = {}
        self._data = data
        self._license_plate = license_plate

        self._identifier = None
        self._make = None
        self._model = None
        self._active = False
        self._odo = 0
        self._latitude = 0
        self._longitude = 0
        self._altitude = 0
        self._speed = 0
        self._last_seen = None
        self._equipment_id = None

        self._malfunction_light = False
        self._fuel_level = -1
        self._coolant_temperature = 0
        self._power_voltage = 0

    @property
    def identifier(self):
        """Return the internal identifier for this device."""
        return self._identifier

    @property
    def plate_as_id(self):
        """Format the license plate so it can be used as identifier."""
        return self._license_plate.replace('-', '')

    @property
    def license_plate(self):
        """Return the license plate of the vehicle."""
        return self._license_plate

    @property
    def equipment_id(self):
        """Return the equipment_id of the vehicle."""
        return self._equipment_id

    @property
    def latitude(self):
        """Return the latitude of the vehicle."""
        return self._latitude

    @property
    def longitude(self):
        """Return the longitude of the vehicle."""
        return self._longitude

    @property
    def state_attributes(self):
        """Return all attributes of the vehicle."""
        return {
            'id': self._identifier,
            'make': self._make,
            'model': self._model,
            'license_plate': self._license_plate,
            'active': self._active,
            'odo': self._odo,
            'latitude': self._latitude,
            'longitude': self._longitude,
            'altitude': self._altitude,
            'speed': self._speed,
            'last_seen': self._last_seen,
            'friendly_name': self._license_plate,
            'equipment_id': self._equipment_id,
            'fuel_level': self._fuel_level,
            'malfunction_light': self._malfunction_light,
            'coolant_temperature': self._coolant_temperature,
            'power_voltage': self._power_voltage
        }

    def get_extra_vehicle_info(self, authentication_info):
        """Get extra data from the API."""
        import requests

        base_url = "https://secure.ritassist.nl/GenericServiceJSONP.ashx"
        query = "?f=CheckExtraVehicleInfo" \
                "&token={token}" \
                "&equipmentId={identifier}" \
                "&lastHash=null&padding=false"

        parameters = {
            'token': authentication_info.access_token,
            'identifier': str(self.identifier)
        }

        response = requests.get(base_url + query.format(**parameters))
        json = response.json()

        self._malfunction_light = json['MalfunctionIndicatorLight']
        self._fuel_level = json['FuelLevel']
        self._coolant_temperature = json['EngineCoolantTemperature']
        self._power_voltage = json['PowerVoltage']

    def update_from_json(self, json_device):
        """Set all attributes based on API response."""
        self._identifier = json_device['Id']
        self._license_plate = json_device['EquipmentHeader']['SerialNumber']
        self._make = json_device['EquipmentHeader']['Make']
        self._model = json_device['EquipmentHeader']['Model']
        self._equipment_id = json_device['EquipmentHeader']['EquipmentID']
        self._active = json_device['EngineRunning']
        self._odo = json_device['Odometer']
        self._latitude = json_device['Location']['Latitude']
        self._longitude = json_device['Location']['Longitude']
        self._altitude = json_device['Location']['Altitude']
        self._speed = json_device['Speed']
        self._last_seen = json_device['Location']['DateTime']

