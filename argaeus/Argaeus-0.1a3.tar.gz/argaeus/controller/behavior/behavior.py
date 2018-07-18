from pelops.mylogger import get_child
from argaeus.controller.behavior.behaviortypes import BehaviorTypes


class Behavior:
    _config = None
    _verbose = None
    _mqtt_client = None
    _state = None

    _name = None
    _topic_sub = None
    _topic_command = None
    behavior_type = None

    response_methods = None

    def __init__(self, config, mqtt_client, logger):
        self._logger = get_child(logger, __name__)
        self._config = config
        self._mqtt_client = mqtt_client
        self._logger.info("Behavior.__init__ - initializing instance")
        self._logger.debug("Behavior.__init__ - config: '{}'".format(self._config))

        self._name = self._config["name"]

        self._topic_sub = self._config["topic-sub"]
        self._topic_command = self._config["command-active"]

        self.behavior_type = BehaviorTypes.factory(self._config["behavior"])
        self.response_methods = []

    def _topic_handler(self, value):
        if value.decode("utf-8") == self._topic_command:
            self._logger.info("Behavior._topic_handler - detected behavior '{}' from input '{}'.".
                              format(self.behavior_type._name_, self._name))
            for method in self.response_methods:
                self._logger.debug("Behavior._topic_handler - processing behavior '{}' by calling method '{}'".
                                   format(self.behavior_type, method))
                method()
        else:
            self._logger.info("Behavior._topic_handler - received unknown value '{}'".format(value))

    def start(self):
        self._logger.info("Behavior.start - subscribing topic.")
        self._mqtt_client.subscribe(self._topic_sub, self._topic_handler)

    def stop(self):
        self._logger.info("Behavior.start - unsubscribing topic.")
        self._mqtt_client.unsubscribe(self._topic_sub, self._topic_handler)
