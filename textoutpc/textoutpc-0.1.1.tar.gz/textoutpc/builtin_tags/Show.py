#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from ..tags import TextoutBlockTag as _TextoutBlockTag
from html import escape as _htmlescape

__all__ = ["TextoutShowTag"]

class TextoutShowTag(_TextoutBlockTag):
	""" Tag which shows the HTML code that is produced by textout().
		Example uses:
		
		[show][b]hello world![/show]
	"""

	aliases = ('[show]',)
	notempty = True
	superblock = True
	inlined = True
	generic = False
	raw = False

	def preprocess_html(self, content):
		return _htmlescape(content)

	def begin_html(self):
		return '<span style="font-family: monospace;">'

	def end_html(self):
		return '</span>'

# End of file.
