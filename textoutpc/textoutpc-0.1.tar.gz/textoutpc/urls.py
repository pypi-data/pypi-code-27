#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Autolinking (URL extraction from raw text) in HTML. """

import regex as _re

__all__ = ["htmlurls", "lightscripturls"]

# ---
# Autolinking regex.
# ---

def _sub_html(m):
	sp = m.group('sp')
	url = m.group('url')
	aft = ''

	# Hack for the last comma.
	if url[-1] == ',':
		url, aft = url[:-1], ','

	text = '{}<a href="{}">{}</a>{}' \
		.format(sp, url, url, aft)
	return text

def _sub_lightscript(m):
	sp = m.group('sp')
	url = m.group('url')
	aft = ''

	# Hack for the last comma.
	if url[-1] == ',':
		url, aft = url[:-1], ','

	url = url.replace('<', '%3C')
	url = url.replace('>', '%3E')
	text = '{}<{}>{}'.format(sp, url, aft)
	return text

_reg = _re.compile("""\
	(?P<sp>^|\s|[[:punct:]])
	(?P<url>(https?|ftp):
		(?P<ucore>[^\[\]\(\)\s]* (\[(?&ucore)\]?)* (\((?&ucore)\)?)*)*
	)
""", _re.VERBOSE | _re.M)

# ---
# Main functions.
# ---

def htmlurls(text):
	return _reg.sub(_sub_html, text)

def lightscripturls(text):
	return _reg.sub(_sub_lightscript, text)

# End of file.
