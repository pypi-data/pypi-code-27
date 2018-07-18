from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.behaviortypes import BehaviorTypes


class SetPointController(AController):
    _step_size = None
    _min_temp = None
    _max_temp = None

    _topic_sub_left = None
    _command_left = None
    _topic_sub_right = None
    _command_right = None

    _mode_controller = None

    def __init__(self, behavior_controller, mode_controller, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._step_size = float(self._config["step-size"])
        self._min_temp = float(self._config["min-temp"])
        self._max_temp = float(self._config["max-temp"])

        self._topic_sub_left = self._config["topic-sub-left"]
        self._command_left = self._config["command-left"]
        self._topic_sub_right = self._config["topic-sub-right"]
        self._command_right = self._config["command-right"]

        try:
            behavior_controller.add_response_method(BehaviorTypes.ResetToDefaultTemp, self._behavior_response)
        except KeyError:
            self._logger.warning("SetPointController.__init__ - caught exception from BehaviorController."
                                 "add_response_method. the requested behavior is not available.")

        self._mode_controller = mode_controller

        self._logger.info("SetPointController.__init__ - done")

    def _behavior_response(self):
        self._logger.info("SetPointController._worker_executor - reset to default set point.")
        self._post_topic_handler(self._mode_controller.current_program.default_set_point)

    def _topic_handler_left(self, value):
        if value.decode("utf-8")  == self._command_left:
            self._logger.info("SetPointController._topic_handler - command left.")
            set_point = self._mode_controller.current_program.set_point - self._step_size
            self._post_topic_handler(set_point)

    def _topic_handler_right(self, value):
        if value.decode("utf-8")  == self._command_right:
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
        self._mqtt_client.subscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.subscribe(self._topic_sub_right, self._topic_handler_right)

    def stop(self):
        self._mqtt_client.unsubscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.unsubscribe(self._topic_sub_right, self._topic_handler_right)
