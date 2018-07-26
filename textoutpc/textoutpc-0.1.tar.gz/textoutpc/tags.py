#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Base classes to use with tags in textoutpc, with a manager class.

	For your tag to be used as a textoutpc tag, you have to make it
	inherit one of the `TextoutBlockTag` or `TextoutInlineTag` classes.

	Making separate tag modules is possible through the manager class,
	which allows not to hardcode the tags into the module. """

from functools import partial as _p
from inspect import ismodule as _ismod, isclass as _isclass, \
	getargspec as _getargspec, getfullargspec as _getfullargspec, \
	currentframe as _currentframe, getouterframes as _getouterframes
from importlib import import_module as _importmod

__all__ = ["TextoutTags", "TextoutTag", "TextoutBlockTag", "TextoutInlineTag",
	"TextoutParagraphTag"]

def _getargscount(func):
	try:
		return len(_getfullargspec(func).args)
	except:
		return len(_getargspec(func).args)

# ---
# Main base tag class.
# For more about defining a tag, see `/TAGS.md`.
# ---

class TextoutTag:
	""" The textout tag base class.
		Is initialized with these values:
	
		<name><content><name>
			| name: "<name>" (only special chars such as `)
			| value: None
		[<name>]<content>[/<name>]
			| name: "[<name>]"
			| value: None
		[<name>]<content>[/] (when possible)
			| name: "[<name>]"
			| value: None
		[<name>=<value>]<content>[/<name>]
			| name: "[<name>]"
			| value: "<value>"
		[<name>=<value>]<content>[/] (when possible)
			| name: "[<name>]"
			| value: "<value>" """

	aliases = ()

	def __init__(self, name, value, ot, tweaks):
		""" Initialize the textout tag with the documented members. """

		# Store internal data.

		self.__output_type = ot
		self.__tweaks = tweaks

		self.output_type = ot

		# Call both prepare functions.

		if hasattr(self, 'prepare'):
			try:
				assert _getargscount(self.prepare) == 4
				args = (name, value, ot)
			except:
				args = (name, value)
			self.prepare(*args)
		if hasattr(self, 'prepare_' + ot):
			prep = getattr(self, 'prepare_' + ot)
			try:
				assert len(_getargspec(prep).args) == 4
				args = (name, value, ot)
			except:
				args = (name, value)
			prep(*args)

		# Prepare the preprocessing elements.
		if hasattr(self, 'preprocess'):
			if hasattr(self, 'preprocess_' + ot):
				self.__preprocess0 = self.preprocess
				self.preprocess = self.__preprocess_double
		elif hasattr(self, 'preprocess_' + ot):
			self.preprocess = getattr(self, 'preprocess_' + ot)

		if hasattr(self, 'preprocess'):
			self.__preprocess2 = self.preprocess
			self.preprocess = self.__preprocess_and_prepare
		else:
			self.__after_preprocess()

		if hasattr(self, 'default_' + ot):
			self.default = getattr(self, 'default_' + ot)

	def __preprocess_double(self, content):
		""" Preprocess using the two methods. """

		ct = self.__preprocess0(content)
		if ct != None: content = ct; del ct
		ct = self.__preprocess1(content)
		if ct != None: content = ct; del ct
		return content

	def __preprocess_and_prepare(self, content):
		""" Preprocess and do the things after. """

		ret = self.__preprocess2(content)
		self.__after_preprocess()
		return ret

	def __out(self, name):
		""" Generic function to call two output functions of the same
			type. """

		getattr(self, '__' + name)()
		getattr(self, name + '_' + self.__output_type)()

	def __after_preprocess(self):
		""" After preprocessing, check the begin, content and end that may
			have been set by the preprocessing function. """

		ot = self.__output_type

		for otype in ('begin', 'content', 'end'):
			if hasattr(self, otype):
				if hasattr(self, otype + '_' + ot):
					setattr(self, '__' + otype, getattr(self, otype))
					setattr(self, otype, _p(self.__out, otype))
			elif hasattr(self, otype + '_' + ot):
				setattr(self, otype, getattr(self, otype + '_' + ot))

	def tweak(self, key, default = None):
		try:
			return self.__tweaks[key]
		except KeyError:
			return default

# ---
# Role-specific base tag classes.
# ---

class TextoutBlockTag(TextoutTag):
	pass
class TextoutInlineTag(TextoutTag):
	pass

# ---
# Default tag: paragraph.
# ---

class TextoutParagraphTag(TextoutBlockTag):
	""" Main tag for basic paragraphs. """

	notempty = True

	def begin_html(self):
		return '<p>'

	def end_html(self):
		return '</p>'

# ---
# Tag extractor.
# ---

class TextoutTags:
	""" Tag manager.
		Object responsible for getting the tags. """

	def __init__(self, *modules):
		self._aliases = {}
		for mod in modules:
			self.import_tags(mod)

	def __extract_tags(self, module):
		""" Extract tags from a module. """

		tags = []

		# Obtain the list of properties from the module.

		try:
			ds = module.__all__
		except:
			ds = dir(module)

		# Get the submodules from the module (usually different files in the
		# tags module folder).

		for submodule in (obj for name, obj in ((nm, getattr(module, nm)) \
		for nm in ds) if (name == '__init__' or name[0] != '_') \
		and _ismod(obj)):
			obtained = self.__extract_tags(submodule)
			tags += [tag for tag in obtained \
				if not any(tag is x for x in tags)]
			del obtained

		# Extract the tags from the current module.

		for tag in (obj for name, obj in ((nm, getattr(module, nm)) \
			for nm in ds) if name[0] != '_' and _isclass(obj) \
			and issubclass(obj, TextoutTag)):
			tags.append(tag)

		return tags

	def import_tags(self, module):
		""" Import tags from a dedicated module. """

		if not _ismod(module):
			module = _importmod(module,
				_getouterframes(_currentframe(), 1)[0].name)
		for tag in self.__extract_tags(module):
			for alias in tag.aliases:
				self._aliases[alias] = tag

	def get_tag(self, name, value, output_type = 'html', tweaks = {}):
		""" Initialize a tag. """

		try:
			als = self._aliases[name]
			return als(name, value, output_type, tweaks)
		except:
			return None

# End of file.
