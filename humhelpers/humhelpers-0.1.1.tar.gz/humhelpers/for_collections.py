"""
Functions with shortcuts to help dealing with lists.
"""


def get (collection, index):
	"""
	Returns or element from collection by index (key), or None if not found.
	"""
	try:
		return collection [index]
	except (IndexError, KeyError):
		return None
