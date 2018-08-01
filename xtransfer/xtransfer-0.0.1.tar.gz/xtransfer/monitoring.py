import socket
import json


class Monitoring(object):

    def __init__(self, profile, options):
        self.profile = profile
        self.options = options
        self.disabled = False

        if 'disabled' in self.options:
            self.disabled = self.options['disabled']

    def __send_alert(self, message, status=0):
        """
        Send a Sensu check result
        """
        if self.disabled:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        check_result = {
            'name': self.profile,
            'status': status,
            'output': message
        }

        sock.sendto(json.dumps(check_result).encode('utf-8'),
                    (self.options['host'], self.options['port']))

    def ok(self, message):
        self.__send_alert(message, 0)

    def warning(self, message):
        self.__send_alert(message, 1)

    def critical(self, message):
        self.__send_alert(message, 2)

    def unknown(self, message):
        self.__send_alert(message, 3)
