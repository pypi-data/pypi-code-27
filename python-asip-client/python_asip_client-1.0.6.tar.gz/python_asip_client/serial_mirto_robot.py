from python_asip_client.boards.serial_board import SerialBoard
from python_asip_client.services.bump_service import BumpService
from python_asip_client.services.ir_service import IRService
from python_asip_client.services.motor_service import MotorService

import sys
import time


class SerialMirtoRobot(SerialBoard):

    def __init__(self):
        SerialBoard.__init__(self)

        # Creating instances of services
        self._motors = [MotorService(0, self.asip), MotorService(1, self.asip)]  # init 2 motors (wheels)
        self._irs = [IRService(0, self.asip), IRService(1, self.asip), IRService(2, self.asip)]  # init 3 IR sensors
        self._bumps = [BumpService(0, self.asip), BumpService(1, self.asip)]  # init 2 bump sensors
        sys.stdout.write("DEBUG: instances of services created\n")

        # Setting reporting interval of sensors
        reporting_interval = 25
        self._motors[0].enable_encoder()
        self._motors[1].enable_encoder()
        self._irs[0].set_reporting_interval(reporting_interval)
        self._irs[1].set_reporting_interval(reporting_interval)
        self._irs[2].set_reporting_interval(reporting_interval)
        self._bumps[0].set_reporting_interval(reporting_interval)
        self._bumps[1].set_reporting_interval(reporting_interval)
        sys.stdout.write("DEBUG: reporting interval set to {}\n".format(reporting_interval))

        #  Adding services
        self.get_asip_client().add_service(self._motors[0].get_service_id(), self._motors)
        # self.get_asip_client().add_service(self._encoders[0].get_service_id(), self._encoders)
        self.get_asip_client().add_service(self._irs[0].get_service_id(), self._irs)
        self.get_asip_client().add_service(self._bumps[0].get_service_id(), self._bumps)

        sys.stdout.write("DEBUG: services added\n")

    def get_services(self):
        return {"motors": self._motors, "irs": self._irs, "bumps": self._bumps}

