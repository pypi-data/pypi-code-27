from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Value(Base):
	"""Tlv value container
	"""

	_SDM_NAME = 'value'

	def __init__(self, parent):
		super(Value, self).__init__(parent)

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
	def Name(self):
		"""The name of the object

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

	def GetMVPropertyCandidatesToSharePatternWith(self):
		"""Executes the getMVPropertyCandidatesToSharePatternWith operation on the server.

		Returns a list of MVProperties this pattern can be shared with.

		Returns:
			list(list[str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*]]): list of MVProperties this pattern can be shared with

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getMVPropertyCandidatesToSharePatternWith', payload=locals(), response_object=None)

	def GetSharedPatternCandidates(self):
		"""Executes the getSharedPatternCandidates operation on the server.

		Returns a list of shared pattern candidates.

		Returns:
			list(list[str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*]]): list of patterns may be shared

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getSharedPatternCandidates', payload=locals(), response_object=None)
