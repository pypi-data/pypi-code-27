#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Functions for the user.
	Really simplifies the thing.
"""

import io as _io
from .translate import Translator as _Translator

__all__ = ["version", "tohtml", "tolightscript"]

version = "0.1.1"

def tohtml(message, **tweaks):
	""" Converts textout BBcode to HTML.
		Receives a string, returns a string. """

	return _Translator(_io.StringIO(message), _io.StringIO(), 'html', \
		tweaks).process().getvalue()

def tolightscript(message, **tweaks):
	""" Converts textout BBcode to Lightscript.
		Receives a string, returns a string. """

	return "" # TODO: real thing one day

	return _Translator(_io.StringIO(message), _io.StringIO(), 'lightscript', \
		tweaks).process().getvalue()

# End of file.
