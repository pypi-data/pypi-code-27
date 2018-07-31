from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Hex(Base):
	"""This specifies the hexadecimal properties related to the parameter.
	"""

	_SDM_NAME = 'hex'

	def __init__(self, parent):
		super(Hex, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter default value.

		Returns:
			str
		"""
		return self._get_attribute('default')

	@property
	def Value(self):
		"""Parameter hex value.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)
