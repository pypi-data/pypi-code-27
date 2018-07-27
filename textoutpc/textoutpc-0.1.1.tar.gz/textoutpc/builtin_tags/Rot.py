#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from ..tags import TextoutInlineTag as _TextoutInlineTag
import string as _string

__all__ = ["TextoutRotTag"]

class TextoutRotTag(_TextoutInlineTag):
	""" Tag which un-rot13 a content.
		Demonstration tag for content processing.
		Example uses:

		[rot=13]obawbhe[/rot]
		[rot13]Obawbhe[/rot13]
	"""

	aliases = ('[rot]', '[rot13]')
	raw = True

	def prepare(self, name, value):
		if name == "[rot]":
			rot = int(value)
			assert 1 <= rot <= 25
		else:
			rot = int(name[4:-1])

		upr0 = _string.ascii_uppercase
		upr1 = upr0[rot:] + upr0[:rot]
		lwr0 = _string.ascii_lowercase
		lwr1 = lwr0[rot:] + lwr0[:rot]
		self._trans = str.maketrans(upr0 + lwr0, upr1 + lwr1)

	def preprocess(self, content):
		return str.translate(content, self._trans)

# End of file.
