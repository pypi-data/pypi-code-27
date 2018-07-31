from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Instructions(Base):
	"""Instruction
	"""

	_SDM_NAME = 'instructions'

	def __init__(self, parent):
		super(Instructions, self).__init__(parent)

	def Instruction(self, Description=None, DisplayName=None, Name=None):
		"""Gets child instances of Instruction from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Instruction will be returned.

		Args:
			Description (str): Description of the field.
			DisplayName (str): Display name used by GUI.
			Name (str): Name of packet field

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction.Instruction))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction import Instruction
		return self._select(Instruction(self), locals())

	def add_Instruction(self, Description=None, IsEditable="True", IsEnabled="True", IsRequired="True", Name=None):
		"""Adds a child instance of Instruction on the server.

		Args:
			Description (str): Description of the field.
			IsEditable (bool): Information on the requirement of the field.
			IsEnabled (bool): Enables disables the field.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of packet field

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction.Instruction)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction import Instruction
		return self._create(Instruction(self), locals())

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Description(self):
		"""Description of the field.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def DisplayName(self):
		"""Display name used by GUI.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def IsEditable(self):
		"""Information on the requirement of the field.

		Returns:
			bool
		"""
		return self._get_attribute('isEditable')
	@IsEditable.setter
	def IsEditable(self, value):
		self._set_attribute('isEditable', value)

	@property
	def IsEnabled(self):
		"""Enables disables the field.

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

	@property
	def IsRequired(self):
		"""Information on the requirement of the field.

		Returns:
			bool
		"""
		return self._get_attribute('isRequired')
	@IsRequired.setter
	def IsRequired(self, value):
		self._set_attribute('isRequired', value)

	@property
	def Name(self):
		"""Name of packet field

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def AddInstruction(self, Arg2):
		"""Executes the addInstruction operation on the server.

		Adds Instruction item in profile.

		Args:
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('addInstruction', payload=locals(), response_object=None)

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
