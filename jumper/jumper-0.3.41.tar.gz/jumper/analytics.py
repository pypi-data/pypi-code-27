class Analytics(object):
    _DESCRIPTION = "description"
    _VALUE = "value"
    _EVENT_NAME = "user run error"
    _UNIMPLEMENTED_INSTRUCTION = "unimplemented_instruction"
    _UNIMPLEMENTED_SECTION = "unimplemented_section"

    _web_api = None
    _filename = None

    def __init__(self):
        pass

    def set_jemu_connection(self, jemu_connection, local_jemu):
        if not local_jemu:
            jemu_connection.register(self.receive_packet)

    def set_web_api(self, web_api):
        self._web_api = web_api

    def set_filename(self, filename):
        self._filename = filename

    def receive_packet(self, jemu_packet):
        if not self._web_api:
            return
        if jemu_packet[self._DESCRIPTION] == self._UNIMPLEMENTED_INSTRUCTION or jemu_packet["description"] == self._UNIMPLEMENTED_SECTION:
            # print(jemu_packet)
            to_send = {'event': self._EVENT_NAME, 'labels': {
                'message': jemu_packet[self._VALUE],
                'filename': self._filename
            }}
            try:
                self._web_api.add_event(to_send)
            except:
                print("error sending error event")
