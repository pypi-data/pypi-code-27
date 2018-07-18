# -*- coding: utf-8 -*-
"""
Module defining the processes and the steps.

A process is a sequence of steps, each step being an action with a
specification of parameter values for this action. A process can be be run,
it then executes each of the steps on the given input file.
"""

from traceback import format_exc
from glamconv.transformer.libraries import get_format, get_action
from glamconv.transformer.actions import WriteAction, ValidateAction
from glamconv.transformer.logger import RunLog


class Step(object):
    def __init__(self, action, log_details, specif_params):
        if specif_params is None:
            specif_params = {}
        self.action = action
        self.log_details = log_details
        self.params = specif_params


class Process(object):
    @classmethod
    def from_json(cls, data):
        proc = cls(data["in_dataformat"], data["out_dataformat"],
                   steps_specif=data["steps"])
        return proc

    def __init__(self, in_format_uid, out_format_uid, steps_specif=None):
        self.input_format = get_format(in_format_uid)
        if out_format_uid is not None:
            self.output_format = get_format(out_format_uid)
        else:
            self.output_format = None
        self.steps = []  # [Step(), ]
        if steps_specif is not None:
            self.build_steps(steps_specif)

    def build_steps(self, steps_specif):
        self.steps[:] = []  # Delete list content
        ending_idx = len(steps_specif)
        if self.output_format is not None:
            # Last two actions should be the validating action and the writing
            # action for the output format
            ending_idx = len(steps_specif)-2
        for idx, specif in enumerate(steps_specif):
            format_uid = self.input_format.uid
            if idx >= ending_idx:
                format_uid = self.output_format.uid
            try:
                action_class = get_action(format_uid, specif[u"id"])
            except KeyError:
                raise RuntimeError(
                    u"Can't find the action '{0}' for format '{1}'"
                    u"".format(specif[u"id"], format_uid))
            self.steps.append(
                Step(action_class(), specif[u"log_details"],
                     specif[u"params"])
            )

    def check(self):
        if len(self.steps) == 0:
            return True
        assert len(self.steps) > 2, \
            (u"Process should at least contain two steps for reading and "
             u"validating the file in input format")
        assert isinstance(self.steps[0].action,
                          self.input_format.reading_class), \
            (u"First step should read the file in input format")
        assert isinstance(self.steps[1].action,
                          self.input_format.validating_class), \
            (u"Second step should validate the file in input format")
        if self.output_format is not None:
            assert isinstance(self.steps[-1].action,
                              self.output_format.writing_class), \
                (u"Last step should write the file in output format")
            assert isinstance(self.steps[-2].action,
                              self.output_format.validating_class), \
                (u"Penultimate step should validate the file in output format")
        return True

    def run(self, input_stream, output_stream=None, progress_callback=None):
        logger = RunLog()
        logger.start_run()
        input_obj = input_stream
        output_obj = None
        for idx, step in enumerate(self.steps):
            if progress_callback is not None:
                progress_callback(idx)
            logger.start_step(idx)
            try:
                output_obj = step.action.run(input_obj, logger,
                                             step.log_details, step.params)
            except Exception:
                # An error has occured during the execution of the action.
                logger.error(
                    u"The following error has occured and has stopped "
                    u"the run:", format_exc())
                logger.failure = True
                logger.failure_step_index = idx
                logger.failure_message = (
                    u"The run was interrupted because of the following error "
                    u"during step #{0}:\n{1}".format(idx+1, format_exc()))
                logger.end_step()
                if idx > 1 and isinstance(self.steps[-1].action, WriteAction):
                    # We already have started the transformation. Tries to
                    # write the previous result (before the error) thanks to
                    # the last step (as it is a writing action).
                    logger.start_step(len(self.steps)-1)
                    logger.info(u"Trying to write the latest intermediate "
                                u"result...")
                    try:
                        last_step = self.steps[-1]
                        output_obj = last_step.action.run(input_obj, logger,
                                                          last_step.params)
                        logger.info(u"The write operation succeed")
                    except Exception:
                        logger.error(
                            u"The write failed because of the following error:"
                            u"\n{0}".format(format_exc()))
                        output_obj = None
                    logger.end_step()
                # Stops the process.
                break
            # If the action is a validation action, takes into account the
            # result of this validation
            if isinstance(step.action, ValidateAction):
                # output_obj is the result of the validation
                if output_obj:
                    if idx == 1:
                        # The second step is the validation of the input file.
                        logger.input_validation = True
                    else:
                        logger.output_validation = True
                else:
                    _, msg, msg_data = logger.get_last_message()
                    if msg is not None:
                        if len(msg_data) > 256:
                            msg_data = (msg_data[:253]
                                        + u"...\nSee log for full message")
                    if idx == 1:
                        # The second step is the validation of the input file.
                        logger.input_validation = False
                        logger.input_validation_message = (
                            u"The input file is not valid. The following "
                            u"errors have been "
                            u"reported:\n{0}".format(msg_data))
                        logger.error(
                            u"The input validation has failed! "
                            u"Nevertheless, try to apply the steps...")
                    else:
                        logger.output_validation = False
                        logger.output_validation_message = (
                            u"The output file is not valid. The following "
                            u"errors have been "
                            u"reported:\n{0}".format(msg_data))
                        logger.error(u"The output validation has failed!")
            else:
                # For the actions other than the validation ones, the output
                # object becomes the input object of the next action.
                input_obj = output_obj
            logger.end_step()
        if output_stream is not None and output_obj is not None:
            output_stream.write(output_obj)
        logger.end_run()
        return logger


def build_validation_process(format_uid):
    prc = Process(format_uid, None)
    steps = [
        Step(prc.input_format.reading_class()),
        Step(prc.input_format.validating_class()),
    ]
    prc.steps.extend(steps)
    prc.check()
    return prc
