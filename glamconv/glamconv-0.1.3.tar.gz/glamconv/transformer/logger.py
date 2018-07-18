# -*- coding: utf-8 -*-
"""
Module defining the classes used to log the run of a transformation process
in order to transform of a file into another file thanks to a series of steps
(action + parameter values).
"""

import datetime as dtm
import logging

from dateutil.tz import tzutc


ERROR = u"error"
"""
Type of log message describing an error

Type: :class:`str`
"""
WARNING = u"warning"
"""
Type of log message describing an error

Type: :class:`str`
"""
INFO = u"info"
"""
Type of log message describing an error

Type: :class:`str`
"""
EPOCH = dtm.datetime.fromtimestamp(0, tzutc())
"""
Datetime of the 1st January 1970 (Epoch).

Type: :class:`datetime.datetime`
"""


class RunLog(object):
    def __init__(self, stdlogger=None):
        self.start_timestamp = None
        self.steps_log = []  # StepLog
        self.end_timestamp = None
        self.input_validation = None
        self.input_validation_message = u""
        self.output_validation = None
        self.output_validation_message = u""
        self.failure = False
        self.failure_step_index = None
        self.failure_message = u""
        self._current_log = None
        self.stdlogger = stdlogger or logging.getLogger('ead.transform')

    @property
    def result(self):
        if self.failure:
            return True
        if self.output_validation is not None:
            return self.output_validation
        # output_validation can still be None if there was only two steps
        # for validating a file
        return self.input_validation or False

    def start_run(self):
        self.start_timestamp = dtm.datetime.now(tzutc())

    def end_run(self):
        self.end_timestamp = dtm.datetime.now(tzutc())

    def start_step(self, index):
        self._current_step_log = StepLog(index)
        self.steps_log.append(self._current_step_log)

    def end_step(self):
        self._current_step_log = None

    def action_start(self, name, param_values):
        if self._current_step_log is not None:
            self._current_step_log.set_action(name, param_values)
        else:
            raise RuntimeError(
                u"Can't log an action start as no step has begun")

    def info(self, message, data=u""):
        self.stdlogger.info(message + data)
        if self._current_step_log is not None:
            self._current_step_log.record_message(INFO, message, data)
        else:
            raise RuntimeError(u"Can't log a message as no step has begun")

    def warning(self, message, data=u""):
        self.stdlogger.warning(message + data)
        if self._current_step_log is not None:
            self._current_step_log.record_message(WARNING, message, data)
        else:
            raise RuntimeError(u"Can't log a message as no step has begun")

    def error(self, message, data=u""):
        self.stdlogger.error(message + data)
        if self._current_step_log is not None:
            self._current_step_log.record_message(ERROR, message, data)
        else:
            raise RuntimeError(u"Can't log a message as no step has begun")

    def get_last_message(self):
        if len(self.steps_log) > 0:
            last_step = self.steps_log[-1]
            if len(last_step.messages) > 0:
                return last_step.messages[-1]
        return None, None, None

    def dump(self):
        start_delta = self.start_timestamp - EPOCH
        start_msecs = int(start_delta.total_seconds() * 1000)
        end_delta = self.end_timestamp - EPOCH
        end_msecs = int(end_delta.total_seconds() * 1000)
        return {u"startTime": start_msecs,
                u"endTime": end_msecs,
                u"result": self.result,
                u"inputValidation": self.input_validation,
                u"inputValidationMessage": self.input_validation_message,
                u"outputValidation": self.output_validation,
                u"outputValidationMessage": self.output_validation_message,
                u"failure": self.failure,
                u"failureStepIndex": self.failure_step_index,
                u"failureMessage": self.failure_message,
                u"steps": [step.dump() for step in self.steps_log]}


class StepLog(object):
    def __init__(self, step_index):
        self.step_index = step_index
        self.action_name = u""
        self.action_params_val = []  # [ (param_name, param_val), ]
        self.messages = []  # [ (level, message_text, data_text), ]

    def set_action(self, name, param_values):
        self.action_name = name
        self.action_params_val = param_values

    def record_message(self, level, message, data):
        self.messages.append((level, message, data))

    def dump(self):
        data = {u"index": self.step_index,
                u"actionName": self.action_name,
                u"actionParamsVal": self.action_params_val,
                u"messages": []}
        for (level, msg, msg_data) in self.messages:
            data[u"messages"].append({u"level": level,
                                      u"message": msg,
                                      u"data": msg_data})
        return data
