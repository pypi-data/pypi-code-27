from enum import Enum


class BehaviorTypes(Enum):
    ToDefaultMode = 0  # change current mode to defined default mode
    ToggleActivePassive = 1  # change behavior of thermostat from observer to actuator (connect DAC to out)
    ResetToDefaultTemp = 2  # set-point for mode is changed to default temp

    @staticmethod
    def factory(name):
        if name.lower() == "to-default-mode":
            return BehaviorTypes.ToDefaultMode
        elif name.lower() == "toggle-active-passive":
            return BehaviorTypes.ToggleActivePassive
        elif name.lower() == "reset-to-default-temp":
            return BehaviorTypes.ResetToDefaultTemp
        else:
            raise ValueError("BehaviorTypes.factory - unknown value '{}'.".format(name))
