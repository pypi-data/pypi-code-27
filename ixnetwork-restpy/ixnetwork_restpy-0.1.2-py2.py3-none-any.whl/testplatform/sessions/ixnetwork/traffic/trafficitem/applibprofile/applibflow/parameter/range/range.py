from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Range(Base):
	"""This specifies the range parameter of the properties.
	"""

	_SDM_NAME = 'range'

	def __init__(self, parent):
		super(Range, self).__init__(parent)

	@property
	def From(self):
		"""Start range value.

		Returns:
			number
		"""
		return self._get_attribute('from')
	@From.setter
	def From(self, value):
		self._set_attribute('from', value)

	@property
	def MaxValue(self):
		"""(Read only) Maximum supported value for parameter range.

		Returns:
			number
		"""
		return self._get_attribute('maxValue')

	@property
	def MinValue(self):
		"""(Read only) Minimum supported value for parameter range.

		Returns:
			number
		"""
		return self._get_attribute('minValue')

	@property
	def To(self):
		"""End range value.

		Returns:
			number
		"""
		return self._get_attribute('to')
	@To.setter
	def To(self, value):
		self._set_attribute('to', value)
