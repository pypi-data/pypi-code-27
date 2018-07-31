from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Field(Base):
	"""This object contains the attributes related to stack field.
	"""

	_SDM_NAME = 'field'

	def __init__(self, parent):
		super(Field, self).__init__(parent)

	@property
	def __id__(self):
		"""An alphanumeric string that defines the internal field ID.

		Returns:
			str
		"""
		return self._get_attribute('__id__')

	@property
	def ActiveFieldChoice(self):
		"""It is used to select a particular option out of multiple field choice options. The activeFieldChoice will be true only for the fields of the option which is active in GUI.

		Returns:
			bool
		"""
		return self._get_attribute('activeFieldChoice')
	@ActiveFieldChoice.setter
	def ActiveFieldChoice(self, value):
		self._set_attribute('activeFieldChoice', value)

	@property
	def Auto(self):
		"""If true, value for the particular field is considered automatically. If false, user can set values for the particular field.

		Returns:
			bool
		"""
		return self._get_attribute('auto')
	@Auto.setter
	def Auto(self, value):
		self._set_attribute('auto', value)

	@property
	def CountValue(self):
		"""It is used to get the count value of the field.

		Returns:
			str
		"""
		return self._get_attribute('countValue')
	@CountValue.setter
	def CountValue(self, value):
		self._set_attribute('countValue', value)

	@property
	def DefaultValue(self):
		"""It is used to get the default value of the field.

		Returns:
			str
		"""
		return self._get_attribute('defaultValue')

	@property
	def DisplayName(self):
		"""It is used to get the name of the particular field as available in Packet/Qos

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def EnumValues(self):
		"""If the field has string options, then each string is associated with a particular integer value. This attribute is used to get the mapping of integer value with the corresponding string option.

		Returns:
			list(str)
		"""
		return self._get_attribute('enumValues')

	@property
	def FieldChoice(self):
		"""It is true for all the field options active in the GUI.

		Returns:
			bool
		"""
		return self._get_attribute('fieldChoice')

	@property
	def FieldTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fieldTypeId')

	@property
	def FieldValue(self):
		"""An alphanumeric string that returns the value of the field.

		Returns:
			str
		"""
		return self._get_attribute('fieldValue')
	@FieldValue.setter
	def FieldValue(self, value):
		self._set_attribute('fieldValue', value)

	@property
	def FixedBits(self):
		"""Sets all the fields to a constant specified size.

		Returns:
			str
		"""
		return self._get_attribute('fixedBits')
	@FixedBits.setter
	def FixedBits(self, value):
		self._set_attribute('fixedBits', value)

	@property
	def FullMesh(self):
		"""If true, Full Mesh is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('fullMesh')
	@FullMesh.setter
	def FullMesh(self, value):
		self._set_attribute('fullMesh', value)

	@property
	def Length(self):
		"""It is used to get the length of the field in bits.

		Returns:
			number
		"""
		return self._get_attribute('length')

	@property
	def Level(self):
		"""It is used to get the level of the field in bits.

		Returns:
			bool
		"""
		return self._get_attribute('level')

	@property
	def MaxValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('maxValue')
	@MaxValue.setter
	def MaxValue(self, value):
		self._set_attribute('maxValue', value)

	@property
	def MinValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('minValue')
	@MinValue.setter
	def MinValue(self, value):
		self._set_attribute('minValue', value)

	@property
	def Name(self):
		"""An alphanumeric string that returns the name of the field.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def Offset(self):
		"""It is used to get the position of the field in terms of number of bits.

		Returns:
			number
		"""
		return self._get_attribute('offset')

	@property
	def OffsetFromRoot(self):
		"""It is used to get the position of the field in terms of number of bits from the root packet.

		Returns:
			number
		"""
		return self._get_attribute('offsetFromRoot')

	@property
	def OnTheFlyMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('onTheFlyMask')
	@OnTheFlyMask.setter
	def OnTheFlyMask(self, value):
		self._set_attribute('onTheFlyMask', value)

	@property
	def Optional(self):
		"""A read-only field that accepts true/false to make the field optional.

		Returns:
			bool
		"""
		return self._get_attribute('optional')

	@property
	def OptionalEnabled(self):
		"""If true, the optional field can accept values.

		Returns:
			bool
		"""
		return self._get_attribute('optionalEnabled')
	@OptionalEnabled.setter
	def OptionalEnabled(self, value):
		self._set_attribute('optionalEnabled', value)

	@property
	def RandomMask(self):
		"""Select to use random mask bit values.

		Returns:
			str
		"""
		return self._get_attribute('randomMask')
	@RandomMask.setter
	def RandomMask(self, value):
		self._set_attribute('randomMask', value)

	@property
	def RateVaried(self):
		"""It is used to get the varied rate of packet field.

		Returns:
			bool
		"""
		return self._get_attribute('rateVaried')

	@property
	def ReadOnly(self):
		"""It is used to check whether particular field is readOnly or otherwise.

		Returns:
			bool
		"""
		return self._get_attribute('readOnly')

	@property
	def RequiresUdf(self):
		"""It is used to check whether UDF is required.

		Returns:
			bool
		"""
		return self._get_attribute('requiresUdf')

	@property
	def Seed(self):
		"""Select to use seed.

		Returns:
			str
		"""
		return self._get_attribute('seed')
	@Seed.setter
	def Seed(self, value):
		self._set_attribute('seed', value)

	@property
	def SingleValue(self):
		"""If valueType is to be set as singleValue, then after setting the valueType to singleValue, the singleValue is set to a particular value.

		Returns:
			str
		"""
		return self._get_attribute('singleValue')
	@SingleValue.setter
	def SingleValue(self, value):
		self._set_attribute('singleValue', value)

	@property
	def StartValue(self):
		"""Specifies the initial value of increment or decrement.

		Returns:
			str
		"""
		return self._get_attribute('startValue')
	@StartValue.setter
	def StartValue(self, value):
		self._set_attribute('startValue', value)

	@property
	def StepValue(self):
		"""Specifies the value by which value will keep incrementing or decrementing.

		Returns:
			str
		"""
		return self._get_attribute('stepValue')
	@StepValue.setter
	def StepValue(self, value):
		self._set_attribute('stepValue', value)

	@property
	def SupportsNonRepeatableRandom(self):
		"""Indicates whether or not this type of stack supports non-repeatable random

		Returns:
			bool
		"""
		return self._get_attribute('supportsNonRepeatableRandom')

	@property
	def SupportsOnTheFlyMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportsOnTheFlyMask')

	@property
	def TrackingEnabled(self):
		"""If true, tracking is enabled on the particular field in flowTracking.

		Returns:
			bool
		"""
		return self._get_attribute('trackingEnabled')
	@TrackingEnabled.setter
	def TrackingEnabled(self, value):
		self._set_attribute('trackingEnabled', value)

	@property
	def ValueFormat(self):
		"""It is used to get the format of the field like whether format is mac, hex, integer, ipv4 and ipv6.

		Returns:
			str(aTM|bool|debug|decimal|decimalFixed2|decimalSigned8|fCID|float|floatEng|hex|hex8WithColons|hex8WithSpaces|iPv4|iPv6|mAC|mACMAC|mACSiteId|mACVLAN|mACVLANSiteId|string|unknown|varLenHex)
		"""
		return self._get_attribute('valueFormat')

	@property
	def ValueList(self):
		"""If valueType is set as valueList, then after setting valueType to valueList a, list of values can be provided using this attribute.

		Returns:
			list(str)
		"""
		return self._get_attribute('valueList')
	@ValueList.setter
	def ValueList(self, value):
		self._set_attribute('valueList', value)

	@property
	def ValueType(self):
		"""It is used to select a particular value type.

		Returns:
			str(decrement|increment|nonRepeatableRandom|random|repeatableRandomRange|singleValue|valueList)
		"""
		return self._get_attribute('valueType')
	@ValueType.setter
	def ValueType(self, value):
		self._set_attribute('valueType', value)

	def AddLevel(self):
		"""Executes the addLevel operation on the server.

		Add a level to the current field.

		Returns:
			str: The new level that has been added.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('addLevel', payload=locals(), response_object=None)

	def GetLearntInfo(self):
		"""Executes the getLearntInfo operation on the server.

		Get the learned information for a field.

		Returns:
			list(str): A list of learned information.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getLearntInfo', payload=locals(), response_object=None)

	def RemoveLevel(self):
		"""Executes the removeLevel operation on the server.

		Remove a level.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('removeLevel', payload=locals(), response_object=None)
