from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Parameter(Base):
	"""A TAP paramter that can be used.
	"""

	_SDM_NAME = 'parameter'

	def __init__(self, parent):
		super(Parameter, self).__init__(parent)

	@property
	def AvailableChoices(self):
		"""Available Choices

		Returns:
			list(str)
		"""
		return self._get_attribute('availableChoices')

	@property
	def CurrentValue(self):
		"""Parameter UI Display Value

		Returns:
			str
		"""
		return self._get_attribute('currentValue')
	@CurrentValue.setter
	def CurrentValue(self, value):
		self._set_attribute('currentValue', value)

	@property
	def CustomDefaultValue(self):
		"""Parameter Custom Default Value

		Returns:
			str
		"""
		return self._get_attribute('customDefaultValue')

	@property
	def DefaultValue(self):
		"""Parameter Default Value

		Returns:
			str
		"""
		return self._get_attribute('defaultValue')

	@property
	def IsReadOnly(self):
		"""Parameter value type

		Returns:
			bool
		"""
		return self._get_attribute('isReadOnly')

	@property
	def MaxValue(self):
		"""Parameter Maximum Value

		Returns:
			str
		"""
		return self._get_attribute('maxValue')

	@property
	def MinValue(self):
		"""Parameter Minimum Value

		Returns:
			str
		"""
		return self._get_attribute('minValue')

	@property
	def Name(self):
		"""Parameter Name.

		Returns:
			str
		"""
		return self._get_attribute('name')
