import datetime
from argaeus.controller.modes.modefactory import ModeFactory
from argaeus.controller.modes.modeschedule import ModeSchedule
from argaeus.controller.acontroller import AController


class ModeController(AController):
    _modes = None
    _selectable_modes = None
    _selectable_pos = None
    _default_mode = None

    _topic_sub_prev = None
    _command_prev = None
    _topic_sub_next = None
    _command_next = None
    _topic_pub_schedule_image = None
    _topic_sub_to_default = None
    _command_default = None

    current_mode = None
    current_program = None
    current_schedule = None

    def __init__(self, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._modes, self._selectable_modes = ModeFactory.create_modes(self._config["modes"],
                                                                       self._config["topics-pub"], mqtt_client, logger)

        self._default_mode = self._modes[self._config["default-mode"]]
        self._activate_default_mode()

        self._topic_sub_prev = self._config["topics-sub"]["to-prev"]
        self._command_prev = self._config["topics-sub"]["command-prev"]
        self._topic_sub_next = self._config["topics-sub"]["to-next"]
        self._command_next = self._config["topics-sub"]["command-next"]
        self._topic_pub_schedule_image = self._config["topics-pub"]["display-server-schedule-image"]

        try:
            self._topic_sub_to_default = self._config["topics-sub"]["to-default"]
        except KeyError:
            pass

        if self._topic_sub_to_default is not None:
            try:
                self._command_default = self._config["topics-sub"]["command-default"]
            except KeyError:
                self._logger.error("OperationController.__init__ - 'to-default' is set but 'command-default' "
                                   "is missing.")
                raise KeyError("OperationController.__init__ - 'to-default' is set but 'command-default' "
                               "is missing.")

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

    def _to_default_handler(self, value):
        if len(value) > 0 and value.decode("UTF-8") == self._command_default:
            self._logger.info("ModeController._to_default_handler - activate default mode")
            self._activate_default_mode()
            self.update()
        else:
            self._logger.warning("ModeController._to_default_handler - dont know how to handle "
                                 "message '{}'".format(value))

    def _topic_handler_prev(self, value):
        if value.decode("utf-8") == self._command_prev:
            self._logger.info("ModeController._topic_handler - command prev.")
            self._selectable_pos = self._selectable_pos - 1
            self._post_topic_handler()

    def _topic_handler_next(self, value):
        if value.decode("utf-8") == self._command_next:
            self._logger.info("ModeController._topic_handler - command next.")
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
        self._mqtt_client.subscribe(self._topic_sub_prev, self._topic_handler_prev)
        self._mqtt_client.subscribe(self._topic_sub_next, self._topic_handler_next)
        self._mqtt_client.subscribe(self._topic_sub_to_default, self._to_default_handler)
        self.update()
        self._logger.info("ModeController.start - started")

    def stop(self):
        self._logger.info("ModeController.start - stopping")
        self._mqtt_client.unsubscribe(self._topic_sub_prev, self._topic_handler_prev)
        self._mqtt_client.unsubscribe(self._topic_sub_next, self._topic_handler_next)
        self._mqtt_client.unsubscribe(self._topic_sub_to_default, self._to_default_handler)
        self._logger.info("ModeController.start - stopped")

