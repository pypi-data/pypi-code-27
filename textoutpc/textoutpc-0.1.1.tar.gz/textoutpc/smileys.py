#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Smiley conversion.
	Just convert them™.
"""

import regex as _re
from html import escape as _htmlescape

__all__ = ["htmlsmileys"]

# ---
# List of them.
# ---

_Smileys_prefix = "/images/smileys/"

_Smileys = {
	'>:)':			'twisted.gif',
	'>:(':			'evil.gif',
	':)':			'smile.gif',
	';)':			'wink.gif',
	':(':			'sad.gif',
	':D':			'grin.gif',
	':p': 			'hehe.gif',
	'8-)':			'cool2.gif',
	':@':			'mad.gif',
	'0_0':			'eek.gif',
	':E':			'mrgreen.gif',
	':O':			'shocked.gif',
	':s':			'confused2.gif',
	'^^':			'eyebrows.gif',
	":'(":			'cry.gif',
#	':-°':			('whistle.gif', 'height: 15px;'),

	# Name-based smileys.

	':lol:':		'lol.gif',
	':oops:':		'confused2.gif',
	':grr:':		'evil.gif',
	':sry:':		'redface.gif',
	':mmm:':		'rolleyes.gif',
	':waza:':		'waza.gif',
#	':whistle:':	('whistle.gif', 'height: 15px;'),
	':here:':		'pointer.gif',
	':bow:':		'bow.gif',
	':cool:':		'cool.gif',
	':good:':		'welldone.gif',
	':love:':		'love.gif',
	':aie:':		'banghead2.gif',
	':cry:':		'cry.gif',
	':facepalm:':	'facepalm.gif',
	':argh:':		'insults.gif',
	':?:':			'what.gif',
	':!:':			'excl.gif',
	':arrow:':		'here.gif',
	':grin:':		'grin.gif',
}
_Smileys_html = {_htmlescape(a): _Smileys_prefix + b \
	for a, b in _Smileys.items()}

def _Smiley_sub_html(m):
	return m.group(1) + '<img src="' + _Smileys_html[m.group(2)] \
		+ '">' + m.group(3)

_Smiley_html_re = _re.compile('(^|\\s)(' + '|'.join(map(_re.escape,
	_Smileys_html.keys())) + ')(\\s|$)')

# ---
# Functions.
# ---

def htmlsmileys(text):
	""" HTML smileys """

	text = _Smiley_html_re.sub(_Smiley_sub_html, text)
	text = _Smiley_html_re.sub(_Smiley_sub_html, text)
	return text

# End of file.
