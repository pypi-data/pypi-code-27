from python_asip_client.tcp_mirto_robot import TCPMirtoRobot
from python_asip_client.mirto_robot import MirtoRobot


ip_address = "10.14.122.61"
services = TCPMirtoRobot(ip_address, 9999).get_services()

mirto_robot = MirtoRobot(services)

c = mirto_robot.get_count(0)

print(c)
