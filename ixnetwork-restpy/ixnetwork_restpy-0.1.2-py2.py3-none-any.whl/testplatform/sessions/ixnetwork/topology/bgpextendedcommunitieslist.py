from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpExtendedCommunitiesList(Base):
	"""Bgp Non VPN RR External Communities
	"""

	_SDM_NAME = 'bgpExtendedCommunitiesList'

	def __init__(self, parent):
		super(BgpExtendedCommunitiesList, self).__init__(parent)

	@property
	def AsNumber2Bytes(self):
		"""AS 2-Bytes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber2Bytes')

	@property
	def AsNumber4Bytes(self):
		"""AS 4-Bytes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber4Bytes')

	@property
	def AssignedNumber2Bytes(self):
		"""Assigned Number(2 Octets)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('assignedNumber2Bytes')

	@property
	def AssignedNumber4Bytes(self):
		"""Assigned Number(4 Octets)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('assignedNumber4Bytes')

	@property
	def ColorCOBits(self):
		"""Color CO Bits

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('colorCOBits')

	@property
	def ColorReservedBits(self):
		"""Color Reserved Bits

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('colorReservedBits')

	@property
	def ColorValue(self):
		"""Color Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('colorValue')

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
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def LinkBandwidth(self):
		"""Link Bandwidth

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkBandwidth')

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
	def OpaqueData(self):
		"""Opaque Data

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('opaqueData')

	@property
	def SubType(self):
		"""SubType

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subType')

	@property
	def Type(self):
		"""Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

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
