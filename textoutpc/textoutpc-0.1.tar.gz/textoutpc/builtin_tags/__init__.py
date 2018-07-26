#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Built-in tags for the `textoutpc` module.
	Some of these tags will probably have to move to a separate module
	Planète Casio-specific, but still, here we are.
"""

_names = ["Align", "Code", "Image", "Label", "Link", "Progress",
	"Quote", "Rot", "Show", "Spoiler", "Text", "Title", "Video"]
for name in _names:
	__import__(name, globals(), level=1)

# End of file.
