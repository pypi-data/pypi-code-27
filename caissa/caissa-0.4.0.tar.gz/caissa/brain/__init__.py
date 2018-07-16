# -*- coding: utf-8 -*-
"""
Caissa voice-controlled personal assistant
Copyright © 2018  Dieter Dobbelaere

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import os
import pkgutil
import queue
import time

from .events import *
from .skills import *


class Brain:
    """
    The brain of Caissa

        - interacts with senses
        - holds skills
        - controls the interactions between skills and senses
    """

    def __init__(self, args, hearing, sense, speech):
        """
        Constructor
        """

        # store references to senses
        self.hearing = hearing
        self.sense = sense
        self.speech = speech

        # initialize event queue
        self._event_queue = queue.Queue()

        # initialize logger
        self.logger = logging.getLogger(__name__)

        # initialize all skills
        self._init_skills(args)

        # start senses
        self.sense.start(self.event_queue)

    @property
    def event_queue(self):
        """
        Return reference to event queue
        """

        return self._event_queue

    def _init_skills(self, args):
        """
        Initialize all skills
        """

        self.skills = []

        skills_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "skills")

        self.logger.debug("Searching for skills in \"{}\"".format(skills_path))
        for module_finder, name, is_pkg in pkgutil.walk_packages([skills_path]):
            try:
                loader = module_finder.find_module(name)
                module = loader.load_module(name)

                for attr in dir(module):
                    try:
                        cls = getattr(module, attr)
                        if issubclass(cls, Skill) and attr != "Skill":
                            self.logger.debug(
                                "Loading skill \"{}\" ".format(attr))
                            self.skills.append(cls(self, args))
                    except TypeError:
                        pass
            except:
                self.logger.debug("Exception occurred while trying to "
                                  "load skill \"{}\"".format(name),
                                  exc_info=True)

    def think_forever(self):
        """
        Think forever
        """

        # event loop
        while True:
            # process the next event
            e = self.event_queue.get()

            if type(e) is TextInputEvent:
                self.logger.debug(
                    "Processing text input event \"{}\"".format(e.text))

                if e.text == "exit":
                    # forced cleanup all skills
                    for skill in self.skills:
                        skill.__del__()

                    return

            elif type(e) is InfraredInputEvent:
                self.logger.debug(
                    "Processing infrared input event \"{}\"".format(e.cmd))

                if e.cmd in ["KEY_VOLUMEUP", "KEY_VOLUMEDOWN"]:
                    direction = 1 if e.cmd == "KEY_VOLUMEUP" else -1
                    self.change_volume(direction)

            # send event to each skill
            for skill in self.skills:
                skill.handle_event(e)

    def say(self, message):
        """
        Say the given message
        """

        self.speech.say(message)

    def change_volume(self, direction=1):
        """
        Change the volume
        """

        import alsaaudio

        mixer = None
        try:
            mixer = alsaaudio.Mixer()
        except alsaaudio.ALSAAudioError:
            try:
                # try PCM (default mixer on Raspberry PI)
                mixer = alsaaudio.Mixer("PCM")
            except alsaaudio.ALSAAudioError:
                # no suitable mixer found
                self.logger.warning(
                    "No suitable mixer found, cannot change volume.")
        finally:
            if mixer is not None:
                step = 2
                new_volume = min(
                    100, max(0, int(mixer.getvolume()[0]) + direction * step))

                self.logger.debug(
                    "Setting volume to {}%".format(new_volume))

                mixer.setvolume(new_volume)
