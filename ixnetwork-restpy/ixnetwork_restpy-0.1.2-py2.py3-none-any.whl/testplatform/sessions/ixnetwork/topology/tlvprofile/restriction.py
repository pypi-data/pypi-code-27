from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Restriction(Base):
	"""Choices for field value
	"""

	_SDM_NAME = 'restriction'

	def __init__(self, parent):
		super(Restriction, self).__init__(parent)

	@property
	def Enum(self):
		"""Internal enumeration type to be used as value options

		Returns:
			str
		"""
		return self._get_attribute('enum')
	@Enum.setter
	def Enum(self, value):
		self._set_attribute('enum', value)

	@property
	def SingleValue(self):
		"""Restricts the field to single value pattern without overlays

		Returns:
			bool
		"""
		return self._get_attribute('singleValue')
	@SingleValue.setter
	def SingleValue(self, value):
		self._set_attribute('singleValue', value)

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('fetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
