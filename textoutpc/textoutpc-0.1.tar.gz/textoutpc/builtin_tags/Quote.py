#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from ..tags import TextoutBlockTag as _TextoutBlockTag
from html import escape as _htmlescape
from ..smileys import htmlsmileys as _htmlsmileys

__all__ = ["TextoutQuoteTag"]

class TextoutQuoteTag(_TextoutBlockTag):
	""" The main tag for quoting someone.
		Example uses:
		
		[quote]Hey, I said that![/quote]
		[quote=Someone important]I said something important, and it's
		multiline and [b]formatted[/b]!
		[quote=Someone else]Heck, he's even quoting me in his quote![/quote]
		[/quote]
	"""

	aliases = ('[quote]',)
	superblock = True
	notempty = True

	def prepare(self, name, value):
		self._value = value

	def begin_html(self):
		f = '<div class="citation">'
		if self._value:
			f += '<p><b>{} a écrit :</b></p>' \
				.format(_htmlsmileys(_htmlescape(self._value)))
		return f

	def end_html(self):
		return '</div>'

	def begin_lightscript(self):
		text = '<<<'
		if self._value:
			text += ' ' + self._value
		return text + '\n'

	def end_lightscript(self):
		return '<<<\n'

# End of file.
