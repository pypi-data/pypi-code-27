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


class TestSpeech:
    """
    Tests for speech module
    """

    def no_test_speech(self):
        """
        Test the speech class
        """

        from collections import namedtuple
        from caissa.speech import Speech

        Args = namedtuple('Args', 'language')

        args = Args(language="en")
        speech = Speech(args)
        speech.say({"en": "Hello, my name is Caiissa."})
        speech.say({"en": "How are you doing?"})

        args = Args(language="nl")
        speech = Speech(args)
        speech.say({"nl": "Hallo, ik heet Caïissa."})
        speech.say({"nl": "Hoe gaat het met U?"})
