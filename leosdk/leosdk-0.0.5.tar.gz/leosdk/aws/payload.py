import datetime
import json
import time


class Payload:

    def __init__(self):
        self.payloadObj = {}
        self.start = 0
        self.end = 0
        self.units = 0
        self.source = ''
        self.payload_id = ''
        self.event = ''
        self.eventSourceTimestamp = 0
        self.now = round(time.time() * 1000)

    def get_payload_data(self):
        return json.dumps({
            'event': self.get_event(),
            'id': self.get_id(),
            'eid': self.get_eid(),
            'payload': self.get_payload(),
            'correlation_id': {
                'source': self.get_source(),
                'start': self.get_start(),
                'units': self.get_units(),
                'end': self.get_end(),
            },
            'event_source_timestamp': self.get_event_source_timestamp(),
            'timestamp': self.now
        }, separators=(',', ':')) + '\n'

    def set_payload(self, name, payload):
        if name in self.payloadObj:
            self.payloadObj[name] += self.get_payload_obj(payload)
        else:
            self.payloadObj = self.get_payload_obj(payload)

    def set(self, payload):
        self.set_payload('', payload)

    def get_payload(self, name=''):
        return self.payloadObj[name] if name else self.payloadObj

    def set_start(self, start: int):
        self.start = start

    def get_start(self) -> int:
        return self.start

    def set_end(self, end: int):
        self.end = end

    def get_end(self) -> int:
        return self.end

    def set_units(self, units: int):
        self.units = units

    def get_units(self):
        return self.units

    def increment_units(self):
        self.units += 1

    def decrement_units(self):
        self.units -= 1

    def increase_units(self, amount: int):
        self.units += amount

    def decrease_units(self, amount: int):
        self.units -= amount

    def set_source(self, source: str):
        self.source = source

    def get_source(self) -> str:
        return self.source

    def set_id(self, payload_id: str):
        self.payload_id = payload_id

    def get_id(self) -> str:
        return self.payload_id

    def set_event(self, event: str):
        self.event = event

    def get_event(self) -> str:
        return self.event

    @staticmethod
    def get_payload_obj(payload) -> {}:
        if type(payload) is dict:
            return payload
        if type(payload) is str:
            return json.loads(payload)

        raise ValueError("Payload must be an object or pre-encoded JSON")

    def set_event_source_timestamp(self, event_source_timestamp: int):
        self.eventSourceTimestamp = event_source_timestamp if event_source_timestamp else self.now

    def get_event_source_timestamp(self) -> int:
        return self.eventSourceTimestamp if self.eventSourceTimestamp else self.now

    def get_eid(self) -> str:
        return datetime.datetime.fromtimestamp(self.now / 1000).strftime('z/%Y/%m/%d/%H/%M/%S/%%d-0000000') % self.now
