from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Number(Base):
	"""This specifies the number related properties of the parameter.
	"""

	_SDM_NAME = 'number'

	def __init__(self, parent):
		super(Number, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter default value.

		Returns:
			number
		"""
		return self._get_attribute('default')

	@property
	def MaxValue(self):
		"""(Read only) Maximum supported value for parameter.

		Returns:
			number
		"""
		return self._get_attribute('maxValue')

	@property
	def MinValue(self):
		"""(Read only) Minimum supported value for parameter.

		Returns:
			number
		"""
		return self._get_attribute('minValue')

	@property
	def Value(self):
		"""Parameter integer value.

		Returns:
			number
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)
