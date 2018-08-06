import os


class Analytics(object):
    _DESCRIPTION = "description"
    _VALUE = "value"
    _EVENT_NAME = "user run error"

    def __init__(self):
        self._error_type_list = ["unimplemented_instruction", "unimplemented_section", "jemu_error", "user_error"]

        self._web_api = None
        self._filename = None
        self._jemu_cmd = None

    def set_jemu_connection(self, jemu_connection, local_jemu):
        if not local_jemu:
            jemu_connection.register(self.receive_packet)

    def set_web_api(self, web_api):
        self._web_api = web_api

    def set_filename(self, filename):
        self._filename = filename

    def set_jemu_cmd(self, jemu_cmd):
        self._jemu_cmd = ' '.join(jemu_cmd)

    def receive_packet(self, jemu_packet):
        if not self._web_api:
            return

        jemu_packet_type = jemu_packet[self._DESCRIPTION]
        if any(jemu_packet_type in error_type for error_type in self._error_type_list):
            # print(jemu_packet)
            to_send = {'event': self._EVENT_NAME, 'labels': {
                'message': jemu_packet[self._VALUE],
                'filename': self._filename,
                'jemu_cmd': self._jemu_cmd,
                'error_type': jemu_packet_type,
                'running_from_cloud': 'RUNNING_FROM_CLOUD' in os.environ
                }}
            try:
                self._web_api.add_event(to_send)
            except:
                print("error sending error event")
