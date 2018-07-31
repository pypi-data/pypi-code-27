from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RepeatableContainer(Base):
	"""Tlv repeatable field container used to group multiple fields
	"""

	_SDM_NAME = 'repeatableContainer'

	def __init__(self, parent):
		super(RepeatableContainer, self).__init__(parent)

	def Object(self, Name=None):
		"""Gets child instances of Object from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Object will be returned.

		Args:
			Name (str): The name of the object

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.object.Object))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.object import Object
		return self._select(Object(self), locals())

	@property
	def IsEnabled(self):
		"""Enables/disables this field

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

	@property
	def Name(self):
		"""Name of the tlv

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

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
