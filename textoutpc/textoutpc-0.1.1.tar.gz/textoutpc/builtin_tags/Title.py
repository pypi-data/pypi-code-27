#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from ..tags import TextoutBlockTag as _TextoutBlockTag

__all__ = ["TextoutTitleTag"]

class TextoutTitleTag(_TextoutBlockTag):
	""" The title tag.
		Example uses:
		
		[title]Some title[/title]
		[subtitle]Some subtitle[/subtitle]
	"""

	aliases = ('[title]', '[subtitle]')
	raw = True

	def prepare(self, name, value):
		self._level = name[1:-1]

	def begin_html(self):
		return ('<h5>', '<h4>')[self._level == "title"]

	def end_html(self):
		return ('</h5>', '</h4>')[self._level == "title"]

	def begin_lightscript(self):
		return '#' * ((self._level == "subtitle") + 1) + ' '

# End of file.
