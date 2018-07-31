from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Instructions(Base):
	"""Instruction set prototype.
	"""

	_SDM_NAME = 'instructions'

	def __init__(self, parent):
		super(Instructions, self).__init__(parent)

	def Instruction(self, Description=None, Name=None):
		"""Gets child instances of Instruction from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Instruction will be returned.

		Args:
			Description (str): Description of the TLV prototype.
			Name (str): Name of the TLV field.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.instruction.Instruction))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.instruction import Instruction
		return self._select(Instruction(self), locals())

	def add_Instruction(self, Description=None, IsEditable="True", IsRepeatable="False", IsRequired="True", Name=None):
		"""Adds a child instance of Instruction on the server.

		Args:
			Description (str): Description of the TLV prototype.
			IsEditable (bool): Information on the requirement of the field.
			IsRepeatable (bool): Information if the field can be multiplied in the tlv definition.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of the TLV field.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.instruction.Instruction)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.instruction import Instruction
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
		"""Description of the TLV prototype.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

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
	def IsRepeatable(self):
		"""Information if the field can be multiplied in the tlv definition.

		Returns:
			bool
		"""
		return self._get_attribute('isRepeatable')
	@IsRepeatable.setter
	def IsRepeatable(self, value):
		self._set_attribute('isRepeatable', value)

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
		"""Name of the TLV field.

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
