"""
Functions with shortcuts to help with work with strings.
"""


def reverse (source_text):
	"""
	Reverse a string.
	"""
	text = ''
	for i in source_text:
		text = i + text
	return text


def replace (source_string, text_before, text_after, amount = None, start_from_right = False):
	"""
	Replaces one substring in string to another.
	Analog to string method with same name,
	but also adds ability to change direction, from which to replace substring.
	"""
	if not start_from_right:
		if amount:
			return str.replace(source_string, text_before, text_after, amount)
		else:
			return str.replace(source_string, text_before, text_after)
	else:
		reversed_string	= reverse (source_string)
		reversed_before	= reverse (text_before)
		reversed_after	= reverse (text_after)
		if amount:
			reversed_replaced = str.replace (reversed_string, reversed_before, reversed_after, amount)
		else:
			reversed_replaced = str.replace (reversed_string, reversed_before, reversed_after)
		return reverse (reversed_replaced)
