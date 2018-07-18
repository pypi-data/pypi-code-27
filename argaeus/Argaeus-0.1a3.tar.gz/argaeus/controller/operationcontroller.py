from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.behaviortypes import BehaviorTypes


class OperationController(AController):
    _default_is_active = None
    active_operation = None
    
    _topic_pub = None
    _command_active = None
    _command_passive = None

    def __init__(self, behavior_controller, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._default_is_active = bool(self._config["default-is-active"])
        self.active_operation = self._default_is_active

        self._topic_pub = self._config["topic-pub"]
        self._command_active = self._config["command-active"]
        self._command_passive = self._config["command-passive"]

        try:
            behavior_controller.add_response_method(BehaviorTypes.ToggleActivePassive, self._behavior_response)
        except KeyError:
            self._logger.warning("OperationController.__init__ - caught exception from BehaviorController."
                                 "add_response_method. the requested behavior is not available.")

        self._logger.info("OperationController.__init__ - done")

    def _behavior_response(self):
        self.active_operation = not self.active_operation
        self._logger.info("OperationController._worker_executor - toggle active/passive (now: '{}').".
                          format(self.active_operation))
        self._publish()

    def _publish(self):
        if self.active_operation:
            self._mqtt_client.publish(self._topic_pub, self._command_active)
        else:
            self._mqtt_client.publish(self._topic_pub, self._command_passive)

    def start(self):
        self._publish()

    def stop(self):
        pass
