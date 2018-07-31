from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Bool(Base):
	"""This specifies the boolean properties of the parameter.
	"""

	_SDM_NAME = 'bool'

	def __init__(self, parent):
		super(Bool, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter default value.

		Returns:
			bool
		"""
		return self._get_attribute('default')

	@property
	def Value(self):
		"""Parameter bool value.

		Returns:
			bool
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)
