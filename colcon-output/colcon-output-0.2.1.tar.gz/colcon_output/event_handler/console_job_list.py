# Copyright 2016-2018 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import sys
import time

from colcon_core.event.job import JobQueued
from colcon_core.event.job import JobStarted
from colcon_core.event_handler import EventHandlerExtensionPoint
from colcon_core.plugin_system import satisfies_version


class ConsoleJobListEventHandler(EventHandlerExtensionPoint):
    """
    Output list of queued task names.

    The extension handles events of the following types:
    - :py:class:`colcon_core.event.job.JobQueued`
    """

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            EventHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')
        self.enabled = False
        self._queued = []

    def __call__(self, event):  # noqa: D102
        data = event[0]

        if isinstance(data, JobQueued):
            job = event[1]
            self._queued.append(job)
        if isinstance(data, JobStarted):
            if self._queued:
                print('Topplogical order')
                for job in self._queued:
                    t = job.task

                    k = job.__dict__.keys()
                    print('- {job} ({t}) [{k}]'.format_map(locals()))
                self._queued = []
