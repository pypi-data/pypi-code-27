from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Predefined(Base):
	"""Default template and profile for Action Builder.
	"""

	_SDM_NAME = 'predefined'

	def __init__(self, parent):
		super(Predefined, self).__init__(parent)

	def ActionTemplate(self, DescriptiveName=None, Name=None, SavedInVersion=None):
		"""Gets child instances of ActionTemplate from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of ActionTemplate will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SavedInVersion (str): The cpf version of the session

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.actiontemplate.ActionTemplate))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.actiontemplate import ActionTemplate
		return self._select(ActionTemplate(self), locals())

	def add_ActionTemplate(self, Name=None, SavedInVersion=None):
		"""Adds a child instance of ActionTemplate on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SavedInVersion (str): The cpf version of the session

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.actiontemplate.ActionTemplate)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.actiontemplate import ActionTemplate
		return self._create(ActionTemplate(self), locals())

	def remove(self):
		"""Deletes a child instance of Predefined on the server.

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
