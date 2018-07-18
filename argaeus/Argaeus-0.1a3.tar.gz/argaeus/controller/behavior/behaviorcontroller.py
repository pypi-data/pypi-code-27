from argaeus.controller.acontroller import AController
from argaeus.controller.behavior.behavior import Behavior


class BehaviorController:
    _behaviors = None

    def __init__(self, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._behaviors = {}
        for conf in self._config:
            behavior = Behavior(conf, self._mqtt_client, self._logger)
            try:
                self._behaviors[behavior.behavior_type].append(behavior)
            except KeyError:
                self._behaviors[behavior.behavior_type] = [behavior]

    def add_response_method(self, behavior_type, method):
        self._logger.info("BehaviorController.add_response_method - adding method to '{}'".format(behavior_type))
        try:
            for behavior in self._behaviors[behavior_type]:
                behavior.response_methods.append(method)
        except KeyError:
            self._logger.error("BehaviorController.add_response_method - unknown behavior type '{}'.".
                               format(behavior_type))
            raise KeyError("BehaviorController.add_response_method - unknown behavior type '{}'.".
                           format(behavior_type))

    def start(self):
        for behavior_list in self._behaviors.values():
            for behavior in behavior_list:
                behavior.start()

    def stop(self):
        for behavior_list in self._behaviors.values():
            for behavior in behavior_list:
                behavior.stop()
