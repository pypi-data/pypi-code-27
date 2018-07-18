from argaeus.controller.modes.modeprogram import ModeProgram
from argaeus.controller.modes.modeschedule import ModeSchedule
from pelops.mylogger import get_child


class ModeFactory:
    @staticmethod
    def create_mode(config, config_topics_pub, mqtt_client, logger):
        log = get_child(logger, __name__)
        log.info("ModeFactory.create_mode - creating mode ('{}').".format(config))

        t = config["type"].lower()
        if t == "program":
            mode = ModeProgram(config, config_topics_pub, mqtt_client, logger)
        elif t == "schedule":
            mode = ModeSchedule(config, config_topics_pub, mqtt_client, logger)
        else:
            log.error("ModeFactory.create_mode - unknown type '{}'.".format(t))
            raise ValueError("ModeFactory.create_mode - unknown type '{}'.".format(t))

        return mode

    @staticmethod
    def create_modes(config, config_topics_pub, mqtt_client, logger):
        log = get_child(logger, __name__)
        log.info("ModeFactory.create_modes - creating modes ('{}').".format(config))

        modes = {}
        modes_selectable = []
        for c in config:
            mode = ModeFactory.create_mode(c, config_topics_pub, mqtt_client, logger)
            modes[mode.name] = mode
            if mode.selectable:
                modes_selectable.append(mode)
        log.info("ModeFactory.create_modes - map_schedule_modes")
        for mode in modes.values():
            if isinstance(mode, ModeSchedule):
                mode.map_schedule_modes(modes)

        return modes, modes_selectable
