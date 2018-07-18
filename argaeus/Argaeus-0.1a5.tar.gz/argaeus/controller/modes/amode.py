from pelops.mylogger import get_child


class AMode:
    _config = None
    _logger = None
    _mqtt_client = None

    name = None
    selectable = None

    def __init__(self, config, mqtt_client, logger):
        self._config = config
        self._mqtt_client = mqtt_client
        self.name = self._config["name"]
        self._logger = get_child(logger, self.name)

        self._logger.info("{}.__init__ - initializing".format(self.name))
        self._logger.debug("{}.__init__ - config: '{}'.".format(self.name, self._config))

        self.selectable = bool(self._config["selectable"])

    def publish(self):
        raise NotImplementedError
