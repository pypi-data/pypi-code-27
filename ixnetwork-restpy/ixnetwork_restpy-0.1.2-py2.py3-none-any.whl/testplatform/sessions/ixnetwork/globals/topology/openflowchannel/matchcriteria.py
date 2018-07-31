from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MatchCriteria(Base):
	"""Match Criteria prototype.
	"""

	_SDM_NAME = 'matchCriteria'

	def __init__(self, parent):
		super(MatchCriteria, self).__init__(parent)

	def Field(self, Description=None, Enum=None, Name=None):
		"""Gets child instances of Field from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Field will be returned.

		Args:
			Description (str): Description of the TLV prototype.
			Enum (str): Internal enumeration type used to restrict possible field values.
			Name (str): Name of the TLV field.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.field.Field))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.field import Field
		return self._select(Field(self), locals())

	def add_Field(self, Description=None, Encoding="hex", Enum="", IsEditable="True", IsRepeatable="False", IsRequired="True", Name=None, SingleValue="False", Size="0", SizeType="byte"):
		"""Adds a child instance of Field on the server.

		Args:
			Description (str): Description of the TLV prototype.
			Encoding (str(aTM|bool|debug|decimal|decimalFixed2|decimalSigned8|fCID|float|floatEng|hex|hex8WithColons|hex8WithSpaces|iPv4|iPv6|mAC|mACMAC|mACSiteId|mACVLAN|mACVLANSiteId|string|unknown|varLenHex)): Encoding of the field value.
			Enum (str): Internal enumeration type used to restrict possible field values.
			IsEditable (bool): Information on the requirement of the field.
			IsRepeatable (bool): Information if the field can be multiplied in the tlv definition.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of the TLV field.
			SingleValue (bool): If true the field can only be configured with a single value pattern.
			Size (number): The size of the field in bytes. Field size must be greater or equal to 0. For automatic detection set size to 0.
			SizeType (str(bit|byte)): The size types/data unit of the field.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.field.Field)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.field import Field
		return self._create(Field(self), locals())

	def MatchCriteria(self, Description=None, Name=None):
		"""Gets child instances of MatchCriteria from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of MatchCriteria will be returned.

		Args:
			Description (str): Description of the TLV prototype.
			Name (str): Name of the TLV field.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.matchcriteria.MatchCriteria))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.matchcriteria import MatchCriteria
		return self._select(MatchCriteria(self), locals())

	def add_MatchCriteria(self, Description=None, IsEditable="True", IsRepeatable="False", IsRequired="True", Name=None):
		"""Adds a child instance of MatchCriteria on the server.

		Args:
			Description (str): Description of the TLV prototype.
			IsEditable (bool): Information on the requirement of the field.
			IsRepeatable (bool): Information if the field can be multiplied in the tlv definition.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of the TLV field.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.matchcriteria.MatchCriteria)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.matchcriteria import MatchCriteria
		return self._create(MatchCriteria(self), locals())

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

	def remove(self):
		"""Deletes a child instance of MatchCriteria on the server.

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
