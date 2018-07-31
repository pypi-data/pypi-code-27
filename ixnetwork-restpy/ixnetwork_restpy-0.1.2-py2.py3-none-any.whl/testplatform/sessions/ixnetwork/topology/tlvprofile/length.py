from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Length(Base):
	"""Tlv length container
	"""

	_SDM_NAME = 'length'

	def __init__(self, parent):
		super(Length, self).__init__(parent)

	def Restriction(self, Enum=None):
		"""Gets child instances of Restriction from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Restriction will be returned.

		Args:
			Enum (str): Internal enumeration type to be used as value options

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.restriction.Restriction))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.restriction import Restriction
		return self._select(Restriction(self), locals())

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
	def Encoding(self):
		"""Encoding of the tlv value, any change will result in the value being reset

		Returns:
			str(bool|decimal|fcid|float|hex|ipv4|ipv6|mac|string|varLenHex)
		"""
		return self._get_attribute('encoding')
	@Encoding.setter
	def Encoding(self, value):
		self._set_attribute('encoding', value)

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
	def IsEnabled(self):
		"""Enables/disables this field

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

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

	@property
	def Size(self):
		"""Size of the tlv value in bits/bytes based on sizeType, any change will result in the value being reset

		Returns:
			number
		"""
		return self._get_attribute('size')
	@Size.setter
	def Size(self, value):
		self._set_attribute('size', value)

	@property
	def SizeType(self):
		"""Size type of the tlv value, any change will result in the value being reset

		Returns:
			str(bit|byte)
		"""
		return self._get_attribute('sizeType')
	@SizeType.setter
	def SizeType(self, value):
		self._set_attribute('sizeType', value)

	@property
	def Value(self):
		"""Value represented as a multivalue object

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('value')

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
