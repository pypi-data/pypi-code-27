from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ActionTemplate(Base):
	"""Action Builder Template.
	"""

	_SDM_NAME = 'actionTemplate'

	def __init__(self, parent):
		super(ActionTemplate, self).__init__(parent)

	def Action(self, Description=None, Name=None):
		"""Gets child instances of Action from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Action will be returned.

		Args:
			Description (str): Description of the TLV prototype.
			Name (str): Name of the TLV field.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.action.Action))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.action import Action
		return self._select(Action(self), locals())

	def add_Action(self, Description=None, IsEditable="True", IsRepeatable="False", IsRequired="True", Name=None):
		"""Adds a child instance of Action on the server.

		Args:
			Description (str): Description of the TLV prototype.
			IsEditable (bool): Information on the requirement of the field.
			IsRepeatable (bool): Information if the field can be multiplied in the tlv definition.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of the TLV field.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.action.Action)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.action import Action
		return self._create(Action(self), locals())

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def SavedInVersion(self):
		"""The cpf version of the session

		Returns:
			str
		"""
		return self._get_attribute('savedInVersion')
	@SavedInVersion.setter
	def SavedInVersion(self, value):
		self._set_attribute('savedInVersion', value)

	def remove(self):
		"""Deletes a child instance of ActionTemplate on the server.

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
