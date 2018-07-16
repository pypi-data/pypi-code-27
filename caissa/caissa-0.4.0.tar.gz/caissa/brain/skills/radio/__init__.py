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
import signal
import subprocess
import threading
import time
import oyaml as yaml

from caissa.brain.events import *
from caissa.brain.skills import Skill


class Radio(Skill):
    """
    Internet radio player
    """

    CONFIG_FNAME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "stations.yml")

    def init(self, args=None):
        """
        Initialize skill
        """

        # initialize logger
        self.logger = logging.getLogger(__name__)

        # load configuration file
        self.config = yaml.load(open(self.CONFIG_FNAME))

        self.logger.debug("Found {} radio stations in \"{}\"".format(
            len(self.config["stations"]), self.CONFIG_FNAME))

        self.stations = list(self.config["stations"].items())

        # initialize other variables
        self.proc = None
        self.current_id = 0

        # initialize and start threads
        self._process_output_thread = threading.Thread(
            target=self.process_output_thread, daemon=True)

        self._process_output_thread.start()

        if args.play_radio:
            self.play()

    def __del__(self):
        """
        Destructor
        """

        self.stop_playing()

    def handle_event(self, e):
        """
        Handle the given event
        """

        if type(e) is TextInputEvent:
            if e.text == "play radio":
                if not self.is_playing:
                    self.play()
            elif e.text == "prev":
                self.play_prev()
            elif e.text == "next":
                self.play_next()
            elif e.text == "stop radio":
                self.stop_playing()
        elif type(e) is InfraredInputEvent:
            if e.cmd == "KEY_PLAY":
                if not self.is_playing:
                    self.play()
                else:
                    self.stop_playing()
            elif e.cmd == "KEY_PREVIOUS":
                self.play_prev()
            elif e.cmd == "KEY_NEXT":
                self.play_next()

    @property
    def is_playing(self):
        """
        Check if the radio is currently playing
        """

        return self.proc is not None

    def stop_playing(self):
        """
        Stop playing
        """

        # terminate a possibly active player process
        if self.is_playing:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)

            self.proc = None

    def play(self, radio_station_id=None):
        """
        Play the given radio station
        """

        if radio_station_id is None:
            radio_station_id = self.current_id

        station_label, station_params = self.stations[radio_station_id]

        self.logger.info("Playing radio station \"{}\"".format(
            station_label))

        # first stop playing
        self.stop_playing()

        # say radio station
        self.say(station_params["name"])

        cmd = "while true; do mpg123 '{}'; sleep 1; done".format(
            station_params["url"])
        self.proc = subprocess.Popen(cmd,
                                     bufsize=1,
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     stdout=subprocess.PIPE,
                                     universal_newlines=True,
                                     preexec_fn=os.setsid)

    def play_prev(self):
        """
        Play the previous station
        """

        if self.is_playing:
            # increment radio station is
            self.current_id = (self.current_id - 1) % len(self.stations)

        self.play(self.current_id)

    def play_next(self):
        """
        Play the next station
        """

        if self.is_playing:
            # increment radio station is
            self.current_id = (self.current_id + 1) % len(self.stations)

        self.play(self.current_id)

    def process_output_thread(self):
        """
        Process the output of the music player process
        """

        import re
        pattern = re.compile(r"\s*ICY-META:\s*StreamTitle='([^']+)'")
        history = []
        MAX_HIST_SIZE = 5

        while True:
            try:
                while True:
                    line = self.proc.stdout.readline()

                    # extract metadata
                    match = re.match(pattern, line)

                    if match:
                        # check if the info is already in the history
                        if line not in history:
                            # append to history
                            history = [line] + history[:MAX_HIST_SIZE - 1]

                            self.logger.info(
                                "Now playing '{}'".format(match.group(1)))
                        else:
                            # push line to top
                            line_index = history.index(line)
                            history = [line] + history[:line_index] + \
                                history[line_index + 1:]
            except AttributeError:
                # the process is not running yet
                # clear history
                history = []

                # sleep some time
                time.sleep(0.2)
                continue
