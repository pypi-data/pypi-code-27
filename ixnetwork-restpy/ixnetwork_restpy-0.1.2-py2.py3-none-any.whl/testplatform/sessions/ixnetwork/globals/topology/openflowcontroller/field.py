from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Field(Base):
	"""Field prototype.
	"""

	_SDM_NAME = 'field'

	def __init__(self, parent):
		super(Field, self).__init__(parent)

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
	def Encoding(self):
		"""Encoding of the field value.

		Returns:
			str(aTM|bool|debug|decimal|decimalFixed2|decimalSigned8|fCID|float|floatEng|hex|hex8WithColons|hex8WithSpaces|iPv4|iPv6|mAC|mACMAC|mACSiteId|mACVLAN|mACVLANSiteId|string|unknown|varLenHex)
		"""
		return self._get_attribute('encoding')
	@Encoding.setter
	def Encoding(self, value):
		self._set_attribute('encoding', value)

	@property
	def Enum(self):
		"""Internal enumeration type used to restrict possible field values.

		Returns:
			str
		"""
		return self._get_attribute('enum')
	@Enum.setter
	def Enum(self, value):
		self._set_attribute('enum', value)

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

	@property
	def SingleValue(self):
		"""If true the field can only be configured with a single value pattern.

		Returns:
			bool
		"""
		return self._get_attribute('singleValue')
	@SingleValue.setter
	def SingleValue(self, value):
		self._set_attribute('singleValue', value)

	@property
	def Size(self):
		"""The size of the field in bytes. Field size must be greater or equal to 0. For automatic detection set size to 0.

		Returns:
			number
		"""
		return self._get_attribute('size')
	@Size.setter
	def Size(self, value):
		self._set_attribute('size', value)

	@property
	def SizeType(self):
		"""The size types/data unit of the field.

		Returns:
			str(bit|byte)
		"""
		return self._get_attribute('sizeType')
	@SizeType.setter
	def SizeType(self, value):
		self._set_attribute('sizeType', value)

	@property
	def Value(self):
		"""Field value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('value')

	def remove(self):
		"""Deletes a child instance of Field on the server.

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
