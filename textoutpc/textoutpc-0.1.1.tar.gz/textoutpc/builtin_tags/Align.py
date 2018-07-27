#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from ..tags import TextoutBlockTag as _TextoutBlockTag

__all__ = ["TextoutAlignTag"]

class TextoutAlignTag(_TextoutBlockTag):
	""" Main tag for aligning paragraphs.
		Example uses:
		
		[align=center]This text is centered horizontally.[/align]
		[justify]This text is justified.[/justify]
	"""

	aliases = ('[align]', '[center]', '[left]', '[right]', '[justify]')
	superblock = True
	notempty = True

	def prepare(self, name, value):
		align = None
		if not name: pass
		elif name == 'align' and value != None:
			align = value
		elif name[1:-1] in ('center', 'left', 'right', 'justify'):
			align = name[1:-1]

		self._align = align

	def begin_html(self):
		cl = []
		if self._align:
			cl.append('align-' + self._align)

		return '<div{}>'.format(' class="' + ' '.join(cl) + '"' if cl else '')

	def end_html(self):
		return '</div>'

# End of file.
