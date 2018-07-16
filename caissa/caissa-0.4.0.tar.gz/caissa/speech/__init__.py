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

import speake3

# TODO: take care of alterations in separate class


class Speech:
    """
    Caissa's speech
    """

    def __init__(self, args):
        """
        Constructor
        """

        # define engine language options
        self.lang_options = {
            "en": {
                "voice": "english-mb-en1+f4",
                "speed": "100",
                "pitch": "60"
            },
            "nl": {
                "voice": "dutch-mbrola-2+f4",
                "speed": "100"
            }
        }

        # instantiate text to speech engines for each language
        self.engines = {lang: speake3.Speake() for lang in self.lang_options}

        # set engine options
        for lang in self.lang_options:
            for option, value in self.lang_options[lang].items():
                self.engines[lang].set(option, value)

            self.engines[lang].set("amplitude", "200")
            self.engines[lang].set("nopause")

        # store default language
        self.default_lang = args.language

        assert self.default_lang in self.engines

    def say(self, message, lang=None):
        """
        Say the given message
        """

        if lang is None:
            lang = self.default_lang

        assert lang in message

        self.engines[lang].say(message[lang])
        self.engines[lang].talkback()
