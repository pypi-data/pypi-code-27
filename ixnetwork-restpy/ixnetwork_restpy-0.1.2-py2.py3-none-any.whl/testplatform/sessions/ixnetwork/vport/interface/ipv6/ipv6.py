from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv6(Base):
	"""Controls the general IPv6 interface properties.
	"""

	_SDM_NAME = 'ipv6'

	def __init__(self, parent):
		super(Ipv6, self).__init__(parent)

	@property
	def Gateway(self):
		"""The IPv6 address of the Gateway to the network,typically an interface on the DUT.

		Returns:
			str
		"""
		return self._get_attribute('gateway')
	@Gateway.setter
	def Gateway(self, value):
		self._set_attribute('gateway', value)

	@property
	def Ip(self):
		"""The 128-bit IPv6 address assigned to this unconnected interface.

		Returns:
			str
		"""
		return self._get_attribute('ip')
	@Ip.setter
	def Ip(self, value):
		self._set_attribute('ip', value)

	@property
	def PrefixLength(self):
		"""A learned/allocated IPv4 address prefix length (mask) for this interface.

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')
	@PrefixLength.setter
	def PrefixLength(self, value):
		self._set_attribute('prefixLength', value)

	@property
	def TargetLinkLayerAddressOption(self):
		"""Tentative Source Link-Layer Address Options for IPv6 Neighbour Discovery. Upon reception of a Tentative Source Link-Layer Address Option in a Neighbour Solicitation for which the receiver has the Target Address configured, a node checks to see if there is a neighbour cache entry with conflicting link-layer address.

		Returns:
			bool
		"""
		return self._get_attribute('targetLinkLayerAddressOption')
	@TargetLinkLayerAddressOption.setter
	def TargetLinkLayerAddressOption(self, value):
		self._set_attribute('targetLinkLayerAddressOption', value)

	@property
	def TrafficClass(self):
		"""This value ,1 byte long, configures the Traffic Class in the IPv6 header for our IPv6 Neighbour Discovery messages. The default value is 0x00 but the user can modify it to any value.

		Returns:
			str
		"""
		return self._get_attribute('trafficClass')
	@TrafficClass.setter
	def TrafficClass(self, value):
		self._set_attribute('trafficClass', value)

	def remove(self):
		"""Deletes a child instance of Ipv6 on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
