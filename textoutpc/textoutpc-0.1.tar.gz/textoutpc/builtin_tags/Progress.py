#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from ..tags import TextoutBlockTag as _TextoutBlockTag

__all__ = ["TextoutProgressTag"]

class TextoutProgressTag(_TextoutBlockTag):
	""" Progress tag, used to display the progress on anything.
		Usage:
		
		[progress=50]My great progress bar[/progress]
		[progress=100][/progress] """

	aliases = ('[progress]',)
	raw = True

	def prepare(self, name, value):
		self._val = int(value)
		if self._val < 0 or self._val > 100:
			raise Exception("progress value should be between 0 and 100 incl.")

	def begin_html(self):
		return '<div>'

	def end_html(self):
		return '' \
		'<div style="background-color: white; border: 1px solid black; ' \
			'width: 50%; margin-top: 2px; text-align: left;">' \
		'<div style="background-color: #FF3E28; color: black; ' \
			'font-weight: bold; max-width: 100%; width: {}%;' \
			'height: 18px;">   {}%' \
		'</div></div></div>'.format(self._val, self._val)

# End of file.
