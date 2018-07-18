from argaeus.controller.acontroller import AController


class SetPointController(AController):
    _step_size = None
    _min_temp = None
    _max_temp = None

    _topic_sub_down = None
    _command_down = None
    _topic_sub_up = None
    _command_up = None

    _topic_sub_reset = None
    _command_reset = None

    _mode_controller = None

    def __init__(self, mode_controller, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._step_size = float(self._config["step-size"])
        self._min_temp = float(self._config["min-temp"])
        self._max_temp = float(self._config["max-temp"])

        self._topic_sub_down = self._config["topic-sub-down"]
        self._command_down = self._config["command-down"]
        self._topic_sub_up = self._config["topic-sub-up"]
        self._command_up = self._config["command-up"]

        try:
            self._topic_sub_reset = self._config["topic-sub-reset"]
        except KeyError:
            pass

        if self._topic_sub_reset is not None:
            try:
                self._command_reset = self._config["command-reset"]
            except KeyError:
                self._logger.error("OperationController.__init__ - 'topic-sub-reset' is set but 'command-reset' "
                                   "is missing.")
                raise KeyError("OperationController.__init__ - 'topic-sub-reset' is set but 'command-reset' is "
                               "missing.")

        self._mode_controller = mode_controller

        self._logger.info("SetPointController.__init__ - done")

    def _reset_temp_handler(self, value):
        if len(value) > 0 and value.decode("UTF-8") == self._command_reset:
            self._logger.info("SetPointController._reset_temp_handler - reset to default set point.")
            self._post_topic_handler(self._mode_controller.current_program.default_set_point)
        else:
            self._logger.warning("SetPointController._reset_temp_handler - dont know how to handle "
                                 "message '{}'".format(value))

    def _topic_handler_left(self, value):
        if value.decode("utf-8")  == self._command_down:
            self._logger.info("SetPointController._topic_handler - command left.")
            set_point = self._mode_controller.current_program.set_point - self._step_size
            self._post_topic_handler(set_point)

    def _topic_handler_right(self, value):
        if value.decode("utf-8")  == self._command_up:
            self._logger.info("SetPointController._topic_handler - command right.")
            set_point = self._mode_controller.current_program.set_point + self._step_size
            self._post_topic_handler(set_point)

    def _post_topic_handler(self, set_to):
        set_point = min(self._max_temp, max(self._min_temp, set_to))
        self._logger.info("SetPointController._topic_handler - set temp to '{}'.".
                          format(self._mode_controller.current_mode.name))
        self._mode_controller.current_program.set_point = set_point
        self._mode_controller.current_program.publish()

    def start(self):
        self._mqtt_client.subscribe(self._topic_sub_down, self._topic_handler_left)
        self._mqtt_client.subscribe(self._topic_sub_up, self._topic_handler_right)
        self._mqtt_client.subscribe(self._topic_sub_reset, self._reset_temp_handler)

    def stop(self):
        self._mqtt_client.unsubscribe(self._topic_sub_down, self._topic_handler_left)
        self._mqtt_client.unsubscribe(self._topic_sub_up, self._topic_handler_right)
        self._mqtt_client.unsubscribe(self._topic_sub_reset, self._reset_temp_handler)
