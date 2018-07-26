#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from ..tags import TextoutInlineTag as _TextoutInlineTag
import re as _re

__all__ = ["TextoutLabelTag", "TextoutTargetTag"]

_labelexpr = _re.compile('^[a-z0-9-]{1,16}$', _re.I)

class TextoutLabelTag(_TextoutInlineTag):
	""" The label tag, defines an anchor at a point of the post.
		Example uses:
		
		[label=installation]Installation de tel logiciel... (no ending req.)
		[label=compilation][/label] Compilation de tel logiciel...
	"""

	aliases = ('[label]',)

	def prepare(self, name, value):
		if not _labelexpr.match(value):
			raise Exception
		self._label = value

	def begin_html(self):
		#name = 'label-{}'.format(self._label)
		#if _v42compat:
		#	name += ' ' + self._label
		name = self.tweak("label_prefix", "") + self._label
		return '<a name="{}"></a>'.format(name)

class TextoutTargetTag(_TextoutInlineTag):
	""" The goto tag, links to an anchor defined in the post.
		Example uses:
		
		[target=installation]Check out the installation manual[/target]!
	"""

	aliases = ('[target]',)

	def prepare(self, name, value):
		if not _labelexpr.match(value):
			raise Exception
		self._label = value

	def begin_html(self):
		#name = 'label-' + self._label
		name = self.tweak("label_prefix", "") + self._label
		return '<a href="#{}">'.format(name)

	def end_html(self):
		return '</a>'

# End of file.
