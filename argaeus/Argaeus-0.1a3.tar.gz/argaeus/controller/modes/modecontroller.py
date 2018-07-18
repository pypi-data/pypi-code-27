import datetime
from argaeus.controller.modes.modefactory import ModeFactory
from argaeus.controller.modes.modeschedule import ModeSchedule
from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.behaviortypes import BehaviorTypes


class ModeController(AController):
    _modes = None
    _selectable_modes = None
    _selectable_pos = None
    _default_mode = None

    _topic_sub_left = None
    _command_left = None
    _topic_sub_right = None
    _command_right = None
    _topic_pub_schedule_image = None

    current_mode = None
    current_program = None
    current_schedule = None

    def __init__(self, behavior_controller, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._modes, self._selectable_modes = ModeFactory.create_modes(self._config["modes"],
                                                                       self._config["topics-pub"], mqtt_client, logger)

        self._default_mode = self._modes[self._config["default-mode"]]
        self._activate_default_mode()

        self._topic_sub_left = self._config["topics-sub"]["to-left"]
        self._command_left = self._config["topics-sub"]["command-left"]
        self._topic_sub_right = self._config["topics-sub"]["to-right"]
        self._command_right = self._config["topics-sub"]["command-right"]
        self._topic_pub_schedule_image = self._config["topics-pub"]["display-server-schedule-image"]

        try:
            behavior_controller.add_response_method(BehaviorTypes.ToDefaultMode, self._behavior_response)
        except KeyError:
            self._logger.warning("ModeController.__init__ - caught exception from BehaviorController."
                                 "add_response_method. the requested behavior is not available.")

        self._logger.info("ModeController.__init__ - done")

    def _activate_default_mode(self):
        self._logger.info("ModeController._activate_default_mode")
        self._selectable_pos = self._selectable_modes.index(self._default_mode)
        self.current_mode = self._default_mode

        if isinstance(self.current_mode, ModeSchedule):
            dt = datetime.datetime.time(datetime.datetime.now())
            self.current_program = self.current_mode.get_program_at_time(dt)
            self.current_schedule = self.current_mode.schedule_raw
        else:
            self.current_program = self.current_mode
            self.current_schedule = None

    def _behavior_response(self):
        self._logger.info("ModeController._worker_executor - activate default mode")
        self._activate_default_mode()
        self.update()

    def _topic_handler_left(self, value):
        if value.decode("utf-8") == self._command_left:
            self._logger.info("ModeController._topic_handler - command left.")
            self._selectable_pos = self._selectable_pos - 1
            self._post_topic_handler()

    def _topic_handler_right(self, value):
        if value.decode("utf-8") == self._command_right:
            self._logger.info("ModeController._topic_handler - command right.")
            self._selectable_pos = self._selectable_pos + 1
            self._post_topic_handler()

    def _post_topic_handler(self):
        self._selectable_pos = self._selectable_pos % len(self._selectable_modes)
        self.current_mode = self._selectable_modes[self._selectable_pos]
        self._logger.info("ModeController._topic_handler - selected mode '{}' at pos '{}'.".
                          format(self.current_mode.name, self._selectable_pos))
        self.update()

    def update(self):
        self._logger.info("ModeController.update")
        if isinstance(self.current_mode, ModeSchedule):
            dt = datetime.datetime.now().time()
            self.current_program = self.current_mode.get_program_at_time(dt)
            self.current_schedule = self.current_mode.schedule_raw
            self.current_program.publish()
            self.current_mode.publish()
        else:
            self.current_program = self.current_mode
            self.current_schedule = None
            self.current_program.publish()
            # no schedule active - publish empty message instead
            self._mqtt_client.publish(self._topic_pub_schedule_image, "")

    def start(self):
        self._logger.info("ModeController.start - starting")
        self._mqtt_client.subscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.subscribe(self._topic_sub_right, self._topic_handler_right)
        self.update()
        self._logger.info("ModeController.start - started")

    def stop(self):
        self._logger.info("ModeController.start - stopping")
        self._mqtt_client.unsubscribe(self._topic_sub_left, self._topic_handler_left)
        self._mqtt_client.unsubscribe(self._topic_sub_right, self._topic_handler_right)
        self._logger.info("ModeController.start - stopped")

