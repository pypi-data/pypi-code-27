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
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object.Object))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object import Object
		return self._select(Object(self), locals())

	def add_Object(self, Name=None):
		"""Adds a child instance of Object on the server.

		Args:
			Name (str): The name of the object

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object.Object)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object import Object
		return self._create(Object(self), locals())

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
