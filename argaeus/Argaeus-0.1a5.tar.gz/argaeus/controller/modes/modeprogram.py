from argaeus.controller.modes.amode import AMode


class ModeProgram(AMode):
    set_point = None
    default_set_point = None
    _topic_pub_set_point = None
    _topic_pub_mode_icon = None

    def __init__(self, config, config_topics_pub, mqtt_client, logger):
        AMode.__init__(self, config, mqtt_client, logger)
        self.set_point = float(self._config["set-point"])
        self.default_set_point = self.set_point
        self._topic_pub_set_point = config_topics_pub["temperature-set-point"]
        self._topic_pub_mode_icon = config_topics_pub["display-server-mode-icon"]

    def publish(self):
        self._mqtt_client.publish(self._topic_pub_set_point, self.set_point)
        self._mqtt_client.publish(self._topic_pub_mode_icon, self.name.lower())

