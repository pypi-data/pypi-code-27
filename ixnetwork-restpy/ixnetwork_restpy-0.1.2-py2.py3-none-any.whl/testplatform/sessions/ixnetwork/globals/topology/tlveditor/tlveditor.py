from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TlvEditor(Base):
	"""Tlv template functionality is contained under this node
	"""

	_SDM_NAME = 'tlvEditor'

	def __init__(self, parent):
		super(TlvEditor, self).__init__(parent)

	def Defaults(self):
		"""Gets child instances of Defaults from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Defaults will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.defaults.Defaults))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.defaults import Defaults
		return self._select(Defaults(self), locals())

	def Template(self, Name=None):
		"""Gets child instances of Template from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Template will be returned.

		Args:
			Name (str): The name of the template

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.template.Template))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.template import Template
		return self._select(Template(self), locals())

	def add_Template(self, Name=None):
		"""Adds a child instance of Template on the server.

		Args:
			Name (str): The name of the template

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.template.Template)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.template import Template
		return self._create(Template(self), locals())

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
