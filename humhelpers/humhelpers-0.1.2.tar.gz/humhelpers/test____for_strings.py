"""
Tests for 'for_strings' module.
"""

from . import for_strings as h


def test ():
	"""
	Main function to launch all tests.
	"""
	test____replace ()


def test____replace ():
	result = h.replace ('aaaa.py.py', '.py', '.js')
	if not result == 'aaaa.js.js': raise ValueError ('wrong replace 1')

	result = h.replace ('aaaa.py.py', '.py', '.js', start_from_right = True)
	if not result == 'aaaa.js.js': raise ValueError ('wrong replace 2')

	result = h.replace ('aaaa.py.py', '.py', '.js', amount = 1)
	if not result == 'aaaa.js.py': raise ValueError ('wrong replace 3')

	result = h.replace ('aaaa.py.py', '.py', '.js', amount = 1, start_from_right = True)
	if not result == 'aaaa.py.js': raise ValueError ('wrong replace 4')

