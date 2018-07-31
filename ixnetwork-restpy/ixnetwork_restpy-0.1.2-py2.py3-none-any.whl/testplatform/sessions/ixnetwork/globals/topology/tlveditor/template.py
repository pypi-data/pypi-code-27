from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Template(Base):
	"""Tlv template container
	"""

	_SDM_NAME = 'template'

	def __init__(self, parent):
		super(Template, self).__init__(parent)

	def Tlv(self, Description=None, Name=None):
		"""Gets child instances of Tlv from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Tlv will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlv.Tlv))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlv import Tlv
		return self._select(Tlv(self), locals())

	def add_Tlv(self, Description=None, IncludeInMessages=None, IsEditable=None, IsRepeatable=None, IsRequired=None, Name=None):
		"""Adds a child instance of Tlv on the server.

		Args:
			Description (str): Description of the tlv
			IncludeInMessages (list(str)): Include the TLV in these protocol messages
			IsEditable (bool): Indicates whether this is editable or not
			IsRepeatable (bool): Indicates whether this can be multiplied in the TLV definition
			IsRequired (bool): Flag indicating whether this is required or not
			Name (str): Name of the tlv

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlv.Tlv)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlv import Tlv
		return self._create(Tlv(self), locals())

	@property
	def Name(self):
		"""The name of the template

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def remove(self):
		"""Deletes a child instance of Template on the server.

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
