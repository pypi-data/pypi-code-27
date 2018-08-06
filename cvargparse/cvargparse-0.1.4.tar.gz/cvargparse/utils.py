def factory(func):
	"""
		Returns 'self' at the end
	"""
	def inner(self, *args, **kw):
		func(self, *args, **kw)
		return self
	return inner