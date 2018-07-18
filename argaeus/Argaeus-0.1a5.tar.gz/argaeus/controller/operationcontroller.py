from argaeus.controller.acontroller import AController


class OperationController(AController):
    _default_is_active = None
    active_operation = None
    
    _topic_pub = None
    _command_active = None
    _command_passive = None

    _topic_sub_toggle = None
    _command_sub_toggle = None

    def __init__(self, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._default_is_active = bool(self._config["default-is-active"])
        self.active_operation = self._default_is_active

        self._topic_pub = self._config["topic-pub"]
        self._command_active = self._config["command-active"]
        self._command_passive = self._config["command-passive"]

        try:
            self._topic_sub_toggle = self._config["topic-sub-toggle"]
        except KeyError:
            pass

        if self._topic_sub_toggle is not None:
            try:
                self._command_sub_toggle = self._config["command-toggle"]
            except KeyError:
                self._logger.error("OperationController.__init__ - 'topic-sub-toggle' is set but 'command-toggle' is "
                                   "missing.")
                raise KeyError("OperationController.__init__ - 'topic-sub-toggle' is set but 'command-toggle' "
                               "is missing.")

        self._logger.info("OperationController.__init__ - done")

    def _toggle_operation_handler(self, value):
        if len(value) > 0 and value.decode("UTF-8") == self._command_sub_toggle:
            self._toggle_operation()
        else:
            self._logger.warning("OperationController._toggle_operation_handler - dont know how to handle "
                                 "message '{}'".format(value))

    def _toggle_operation(self):
        self.active_operation = not self.active_operation
        self._logger.info("OperationController._toggle_operation - toggle active/passive (now: '{}').".
                          format(self.active_operation))
        self._publish()

    def _publish(self):
        if self.active_operation:
            self._mqtt_client.publish(self._topic_pub, self._command_active)
        else:
            self._mqtt_client.publish(self._topic_pub, self._command_passive)

    def start(self):
        self._mqtt_client.subscribe(self._topic_sub_toggle, self._toggle_operation_handler)
        self._publish()

    def stop(self):
        self._mqtt_client.unsubscribe(self._topic_sub_toggle, self._toggle_operation_handler)
