from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Choice(Base):
	"""This specifies the particular choice related properties for the parameter.
	"""

	_SDM_NAME = 'choice'

	def __init__(self, parent):
		super(Choice, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter choice default value.

		Returns:
			str
		"""
		return self._get_attribute('default')

	@property
	def SupportedValues(self):
		"""(Read only) Parameter supported choice values.

		Returns:
			list(str)
		"""
		return self._get_attribute('supportedValues')

	@property
	def Value(self):
		"""Parameter choice selected value.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)
