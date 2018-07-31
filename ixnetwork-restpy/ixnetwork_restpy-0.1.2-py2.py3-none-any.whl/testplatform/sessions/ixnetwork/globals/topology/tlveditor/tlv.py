from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Tlv(Base):
	"""Tlv container
	"""

	_SDM_NAME = 'tlv'

	def __init__(self, parent):
		super(Tlv, self).__init__(parent)

	@property
	def Length(self):
		"""Returns the one and only one Length object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.length.Length)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.length import Length
		return self._read(Length(self), None)

	@property
	def Type(self):
		"""Returns the one and only one Type object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.type.Type)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.type import Type
		return self._read(Type(self), None)

	@property
	def Value(self):
		"""Returns the one and only one Value object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.value.Value)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.value import Value
		return self._read(Value(self), None)

	@property
	def AvailableIncludeInMessages(self):
		"""A list of available messages which are used in the includeInMessages attribute

		Returns:
			list(str)
		"""
		return self._get_attribute('availableIncludeInMessages')

	@property
	def Description(self):
		"""Description of the tlv

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def IncludeInMessages(self):
		"""Include the TLV in these protocol messages

		Returns:
			list(str)
		"""
		return self._get_attribute('includeInMessages')
	@IncludeInMessages.setter
	def IncludeInMessages(self, value):
		self._set_attribute('includeInMessages', value)

	@property
	def IsEditable(self):
		"""Indicates whether this is editable or not

		Returns:
			bool
		"""
		return self._get_attribute('isEditable')
	@IsEditable.setter
	def IsEditable(self, value):
		self._set_attribute('isEditable', value)

	@property
	def IsRepeatable(self):
		"""Indicates whether this can be multiplied in the TLV definition

		Returns:
			bool
		"""
		return self._get_attribute('isRepeatable')
	@IsRepeatable.setter
	def IsRepeatable(self, value):
		self._set_attribute('isRepeatable', value)

	@property
	def IsRequired(self):
		"""Flag indicating whether this is required or not

		Returns:
			bool
		"""
		return self._get_attribute('isRequired')
	@IsRequired.setter
	def IsRequired(self, value):
		self._set_attribute('isRequired', value)

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

	def remove(self):
		"""Deletes a child instance of Tlv on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

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
