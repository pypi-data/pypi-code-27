#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import InlineTag as _InlineTag
from html import escape as _htmlescape

__all__ = ["LinkTag", "ProfileTag"]

class LinkTag(_InlineTag):
	""" The main link tag.
		Example uses:
		
		[url=https://example.org/hi]Go to example.org[/url]!
		[url=/Fr/index.php][/url]
		[url]https://random.org/randomize.php[/url]
	"""

	aliases = ('[url]',)
	raw = True

	def _validate(self):
		for prefix in ('http://', 'https://', 'ftp://', '/', '#'):
			if self._url.startswith(prefix):
				break
		else:
			raise Exception("No allowed prefix!")

	def prepare(self, name, value):
		self._url = None

		# If there is no value, wait until we have a content to
		# decide if we are valid or not.

		if value == None:
			self.preprocess = self._preprocess_if_no_value
			return

		# Otherwise, get the URL and validate.

		self._url = value
		self._validate()
		self.default = self._default_if_value

	def _default_if_value(self):
		return self._url

	def _preprocess_if_no_value(self, content):
		self._url = content
		self._validate()

	def begin_html(self):
		return '<a href="{}">'.format(_htmlescape(self._url))

	def end_html(self):
		return '</a>'

	def begin_lightscript(self):
		return '['

	def end_lightscript(self):
		url = self._url.replace('(', '%28').replace(')', '%29')
		return ']({})'.format(url)

class ProfileTag(LinkTag):
	""" A special link tag for Planète Casio's profiles.
		Adds the prefix to the content, and sets the value.
		Example uses:
		
		[profil]Cakeisalie5[/profil]
	"""

	aliases = ('[profil]', '[profile]')

	def prepare(self, name, value):
		# Override the TextoutLinkTag's prepare method.

		pass

	def preprocess(self, content):
		# FIXME: check the username content!

		username = content
		self._url = 'https://www.planet-casio.com/Fr/compte/voir_profil.php' \
			'?membre={}'.format(username)
		self._validate()

# End of file.
