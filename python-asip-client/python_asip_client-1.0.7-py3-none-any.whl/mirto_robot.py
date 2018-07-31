from python_asip_client.tcp_mirto_robot import TCPMirtoRobot
from python_asip_client.serial_mirto_robot import SerialMirtoRobot
import sys


class MirtoRobot:
    def __init__(self, _services):
        self.motors = _services.get("motors")
        self.irs = _services.get('irs')
        self.bumps = _services.get('bumps')
        self.lcd = _services.get('lcd')

    def set_motors(self, speed1, speed2):
        """
        Setting the two motors speed. Speed value is between: -100 and 100
        :param speed1: int
        :param speed2: int
        :return:
        """
        self.motors[0].set_motor(speed1)
        self.motors[1].set_motor(speed2)
        sys.stdout.write("DEBUG: setting motors to {}, {}\n".format(speed1, speed2))

    def stop_motors(self):
        """
        Stopping the two motors
        :return:
        """
        self.motors[0].stop_motor()
        self.motors[1].stop_motor()

    def get_ir(self, sensor):
        """
        Retrieving data from IR sensor, -1 if sensor number is wrong
        :param sensor: int
        :return:
        """
        return self.irs[sensor].get_ir() if sensor in [0, 1, 2] else -1

    def get_count(self, sensor):
        """
        Retrieving count value from encoder sensor, -1 if sensor number is wrong
        :param sensor: int
        :return:
        """
        return self.motors[sensor].get_count() if sensor in [0, 1] else -1

    def get_encoders(self, pulse=True):
        """
        This function is returning a list with count and pulse values from both encoders.
        By default function is returning them both, however you can provide second optional argument to change it.
        :return: encoders values: list
        """
        if pulse:
            return [[self.motors[0].get_count(), self.motors[0].get_pulse()],
                    [self.motors[1].get_count(), self.motors[1].get_pulse()]]
        else:
            return [self.motors[0].get_count(), self.motors[1].get_count()]

    def is_bump_pressed(self, sensor):
        """
        Retrieving count value from bump sensor, -1 if sensor number is wrong.
        :param sensor: int
        :return:
        """
        return self.bumps[sensor].is_pressed() if sensor in [0, 1] else -1

    def reset_count(self):
        """
        This function is resetting count for both encoders.
        :return:
        """
        self.motors[0].reset_count()
        sys.stdout.write("Reset encoders\n")

    def get_all_ir_values(self, sensor_order=None):
        """
        This function is getting IR sensor values and return a list with those results.
        Some robots have ir sensors in different order, hence as a parameter it can take a list with a order of sensors.
        :param sensor_order:
        :return: sensor values: list
        """
        if sensor_order is None:
            sensor_order = [0, 1, 2]
        sensor_values = []
        for sensor in sensor_order:
            sensor_values.append(self.get_ir(sensor))
        return sensor_values

    def set_motor_rpm(self, motor_ID, rpm, duration):
        """
        This function takes in a motor_ID, RPM and duration
        :param motor_ID: int
        :param rpm: int
        :param duration: int
        :return: if error return -1
        """
        if motor_ID in [0,1]:
            self.motors[motor_ID].set_motor_rpm( rpm, duration)
        else:
            return -1

    def set_motors_rpm(self,rpm0, rpm1, duration):
        """
        This function takes in a RPM0, RPM1 and duration
        :param rpm0: int
        :param rpm1: int
        :param duration: int
        :return: None
        """
        self.motors[0].set_motors_rpm(rpm0, rpm1, duration)

    def set_LCD_message(self, message, line):
        """
        This function takes in a message and a line number
        :param message: string
        :param line: int
        :return: if error return -1
        """
        if line in [0,1,2,3,4]:
            self.lcd[0].set_LCD_message(message, line)
        else:
            return -1

    def clear_LCD(self):
        """
        This function clears the LCD display
        :return: None
        """
        self.lcd[0].clear_LCD()


if __name__ == '__main__':
    # services = SerialMirtoRobot()
    ip_address = "10.14.122.61"
    services = TCPMirtoRobot(ip_address, 9999).get_services()
    mirto_robot = MirtoRobot(services)
