from argaeus.controller.modes.modecontroller import ModeController
from argaeus.controller.setpointcontroller import SetPointController
from argaeus.controller.operationcontroller import OperationController
from pelops.abstractmicroservice import AbstractMicroservice
import time
from argaeus.schema.thermostatguicontroller import get_schema
import argaeus
import threading


class ThermostatGUIController(AbstractMicroservice):
    _version = argaeus.version  # version of software
    _state = None
    _controller = None
    _loop_thread = None

    _mode_controller = None
    _set_point_controller = None
    _operation_controller = None

    def __init__(self, config, mqtt_client=None, logger=None):
        AbstractMicroservice.__init__(self, config, "controller", mqtt_client=mqtt_client, logger=logger,
                                      logger_name=__name__)

        self._mode_controller = ModeController(self._config["mode-controller"], self._mqtt_client, self._logger)
        self._set_point_controller = SetPointController(self._mode_controller, self._config["setpoint-controller"],
                                                        self._mqtt_client, self._logger)
        self._operation_controller = OperationController(self._config["operation-controller"], self._mqtt_client,
                                                         self._logger)

        self._loop_thread = threading.Thread(target=self._poll_loop)

    @staticmethod
    def _calc_sleep_time():
        current_time = time.time()
        seconds_to_next_full_minute = (60 - current_time % 60)  # next full minute in seconds
        return seconds_to_next_full_minute

    def _poll_loop(self):
        self._logger.info("ThermostatGUIController._poll_loop - start")
        while not self._stop_service.isSet():
            self._mode_controller.update()
            sleep_for = ThermostatGUIController._calc_sleep_time()
            self._logger.info("ThermostatGUIController._poll_loop - sleeping for {} seconds.".format(sleep_for))
            self._stop_service.wait(timeout=sleep_for)
        self._logger.info("ThermostatGUIController._poll_loop - end")

    def _start(self):
        self._mode_controller.start()
        self._set_point_controller.start()
        self._operation_controller.start()
        self._loop_thread.start()

    def _stop(self):
        self._loop_thread.join()
        self._mode_controller.stop()
        self._set_point_controller.stop()
        self._operation_controller.stop()

    @classmethod
    def _get_schema(cls):
        return get_schema()

    @classmethod
    def _get_description(cls):
        return "Argaeus is the gui controller element for a thermostat."


def standalone():
    ThermostatGUIController.standalone()


if __name__ == "__main__":
    ThermostatGUIController.standalone()
