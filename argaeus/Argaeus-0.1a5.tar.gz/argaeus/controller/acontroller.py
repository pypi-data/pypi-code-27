from pelops.mylogger import get_child


class AController:
    _config = None
    _mqtt_client = None
    _logger = None

    def __init__(self, config, mqtt_client, logger, logger_name=__name__):
        self._mqtt_client = mqtt_client
        self._config = config
        self._logger = get_child(logger, logger_name)

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
