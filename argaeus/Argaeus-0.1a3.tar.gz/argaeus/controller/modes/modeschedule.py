import collections
import datetime
from argaeus.controller.modes.amode import AMode
from argaeus.controller.modes.schedule_image import ScheduleImage
from io import BytesIO


class ModeSchedule(AMode):
    schedule_raw = None
    schedule = None
    img = None
    _topic_pub = None
    _modes_mapped = None

    def __init__(self, config, config_topics_pub, mqtt_client, logger):
        AMode.__init__(self, config, mqtt_client, logger)
        self.schedule_raw = ModeSchedule._sort_dict(self._config["schedule"])
        self.schedule = collections.OrderedDict()
        self._topic_pub = config_topics_pub["display-server-schedule-image"]
        self._modes_mapped = False

    @staticmethod
    def _sort_dict(d):
        result = collections.OrderedDict()
        for h in range (0, 24):
            for m in range(0, 60):
                key = "{:02}:{:02}".format(h, m)
                dt = datetime.time(hour=h, minute=m)
                try:
                    result[dt] = d[key]
                except KeyError:
                    pass
        return result

    def map_schedule_modes(self, modes):
        self._logger.info("ModeSchedule.map_schedule_modes - mapping schedule '{}' to mode '{}'.".
                          format(self.schedule_raw, modes))
        for k,v in self.schedule_raw.items():
            program = modes[v]
            if isinstance(program, ModeSchedule):
                self._logger.error("ModeSchedule.map_schedule_modes -  mode must not be of type ModeSchedule ('{}').".
                                   format(type(program)))
                raise ValueError("ModeSchedule.map_schedule_modes -  mode must not be of type ModeSchedule ('{}').".
                                 format(type(program)))
            self.schedule[k] = program

        self._logger.info("ModeSchedule.map_schedule_modes - generate schedule image")
        renderer = ScheduleImage(self.schedule, self._config["image"], self._logger)
        self.img = renderer.img

        self._modes_mapped = True

    def get_program_at_time(self, time):  # time as datetime.time instance
        if not self._modes_mapped:
            self._logger.error("ModeSchedule.get_program_at_time - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")
            raise RuntimeError("ModeSchedule.get_program_at_time - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")

        result = None
        for dt, program in self.schedule.items():
            if dt > time:
                break
            result = program
        self._logger.info("ModeSchedule.get_program_at_time - program '{}' at time '{}'.".format(result.name, time))
        return result

    def publish(self):
        self._logger.info("ModeSchedule.publish - sending schedule image")

        if not self._modes_mapped:
            self._logger.error("ModeSchedule.publish - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")
            raise RuntimeError("ModeSchedule.publish - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")

        bytes_image = BytesIO()
        self.img.save(bytes_image, format="png")
        mqtt_message = bytes_image.getvalue()
        self._logger.debug("ModeSchedule.publish - mqtt_message: {}".format(mqtt_message))
        self._mqtt_client.publish(self._topic_pub, mqtt_message)
