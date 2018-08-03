from difflib import SequenceMatcher

import time
import logging
from typing import List

from botworks.slack.Payload import Payload

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ResponseDefinition:
    def __init__(self, trigger_definition=None, response=None, as_thread=True,
                 custom_response=None, custom_matcher=None, cooldown_duration=600,
                 full_text=None, mod_exempt=True, event=None):
        self.triggerWords = trigger_definition
        self.response = response
        self.asThread = as_thread
        self.cooldown_duration = cooldown_duration
        self.cooldown_end = 0
        self.fullText = full_text
        self.responseMethod = custom_response
        self.matchMethod = custom_matcher
        self.modExempt = mod_exempt
        self.conf = {}
        self.event = event

    def finalize(self, config):
        self.conf = config
        log.setLevel(self.conf['log_level'])

    def check(self, payload: Payload, mod_ids: List[str]) -> bool:
        log.info("Checking for response " + str(self.response))
        if self.modExempt and payload.user in mod_ids:
            return False
        if self.matchMethod:
            return self.matchMethod(payload)
        if self.event == payload.event_type:
            return True
        if self.fullText and payload.imageText and \
                SequenceMatcher(None, self.fullText, payload.imageText).ratio() > 0.7:
            return True
        if payload.imageText and self.triggerWords and self.triggerWords.check(payload.imageText):
            return True
        return self.triggerWords and payload.lower_message and self.triggerWords.check(payload.lower_message)

    def respond(self, clacker, payload: Payload):
        if time.time() < self.cooldown_end:
            return
        self.cooldown_end = time.time() + self.cooldown_duration
        if self.responseMethod:
            self.responseMethod(clacker, payload)
        else:
            self.response.respond(clacker, payload)


class And:
    def __init__(self, *args):
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message) -> bool:
        log.debug("Checking And " + str(len(self.triggers)))
        res = True
        for t in self.triggers:
            if type(t) is str:
                res &= t in message
            else:
                res &= t.check(message)
                if not res:
                    break
        return res


class Or:
    def __init__(self, *args):
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message) -> bool:
        log.debug("Checking Or " + str(len(self.triggers)))
        res = False
        for t in self.triggers:
            if type(t) is str:
                res |= t in message
            else:
                res |= t.check(message)
            if res:
                break
        return res


class Not:
    def __init__(self, *args):
        if len([*args]) != 1:
            log.error("Misconfigured Not, it's going to get weird")
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message) -> bool:
        log.debug("Checking Not " + str(len(self.triggers)))
        if type(self.triggers[0]) is str:
            res = self.triggers[0] not in message
        else:
            res = not self.triggers[0].check(message)

        return res


class StartsWith:
    def __init__(self, *args):
        if len([*args]) != 1:
            log.error("Misconfigured Startswith, it's going to get weird")
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message: str) -> bool:
        log.debug("Checking StartsWith " + str(len(self.triggers)))
        if type(self.triggers[0]) is str:
            return message.startswith(self.triggers[0])

        return False

