from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Object(Base):
	"""Tlv object container which can contain one of a field, sub tlv or container
	"""

	_SDM_NAME = 'object'

	def __init__(self, parent):
		super(Object, self).__init__(parent)

	def Container(self, Description=None, Name=None):
		"""Gets child instances of Container from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Container will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.container.Container))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.container import Container
		return self._select(Container(self), locals())

	def add_Container(self, Description=None, IsEditable=None, IsRepeatable=None, IsRequired=None, Name=None):
		"""Adds a child instance of Container on the server.

		Args:
			Description (str): Description of the tlv
			IsEditable (bool): Indicates whether this is editable or not
			IsRepeatable (bool): Flag indicating whether this is repeatable or not
			IsRequired (bool): Flag indicating whether this is required or not
			Name (str): Name of the tlv

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.container.Container)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.container import Container
		return self._create(Container(self), locals())

	def Field(self, Description=None, Name=None):
		"""Gets child instances of Field from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Field will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.field.Field))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.field import Field
		return self._select(Field(self), locals())

	def add_Field(self, Description=None, Encoding=None, IsEditable=None, IsRepeatable=None, IsRequired=None, Name=None, Size=None, SizeType=None):
		"""Adds a child instance of Field on the server.

		Args:
			Description (str): Description of the tlv
			Encoding (str(bool|decimal|fcid|float|hex|ipv4|ipv6|mac|string|varLenHex)): Encoding of the tlv value, any change will result in the value being reset
			IsEditable (bool): Indicates whether this is editable or not
			IsRepeatable (bool): Flag indicating whether this is repeatable or not
			IsRequired (bool): Flag indicating whether this is required or not
			Name (str): Name of the tlv
			Size (number): Size of the tlv value in bits/bytes based on sizeType, any change will result in the value being reset
			SizeType (str(bit|byte)): Size type of the tlv value, any change will result in the value being reset

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.field.Field)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.field import Field
		return self._create(Field(self), locals())

	def SubTlv(self, Description=None, Name=None):
		"""Gets child instances of SubTlv from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of SubTlv will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.subtlv.SubTlv))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.subtlv import SubTlv
		return self._select(SubTlv(self), locals())

	def add_SubTlv(self, Description=None, IsEditable=None, IsRepeatable=None, IsRequired=None, Name=None):
		"""Adds a child instance of SubTlv on the server.

		Args:
			Description (str): Description of the tlv
			IsEditable (bool): Indicates whether this is editable or not
			IsRepeatable (bool): Indicates whether this can be multiplied in the TLV definition
			IsRequired (bool): Flag indicating whether this is required or not
			Name (str): Name of the tlv

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.subtlv.SubTlv)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.subtlv import SubTlv
		return self._create(SubTlv(self), locals())

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

	def remove(self):
		"""Deletes a child instance of Object on the server.

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
