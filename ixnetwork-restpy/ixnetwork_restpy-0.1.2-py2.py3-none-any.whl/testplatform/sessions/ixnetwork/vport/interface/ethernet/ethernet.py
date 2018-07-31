from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ethernet(Base):
	"""Controls the general Ethernet interface properties.
	"""

	_SDM_NAME = 'ethernet'

	def __init__(self, parent):
		super(Ethernet, self).__init__(parent)

	@property
	def MacAddress(self):
		"""A 48-bit hardware address that uniquely identifies each node of a network.

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def Mtu(self):
		"""The maximum packet size, in bytes, that a particular interface can handle.

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def UidFromMac(self):
		"""The interface identifier is derived from the MAC address. The interface identifier u (universal/local) bit will be set to zero to indicate global scope.

		Returns:
			bool
		"""
		return self._get_attribute('uidFromMac')
	@UidFromMac.setter
	def UidFromMac(self, value):
		self._set_attribute('uidFromMac', value)
