from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Interface(Base):
	"""List of interfaces that can be configured on ports. Multiple protocol interfaces can be configured for Ixia ports that support this capability, with the number of protocol interfaces being dependent on the amount of memory available on the Ixia port.
	"""

	_SDM_NAME = 'interface'

	def __init__(self, parent):
		super(Interface, self).__init__(parent)

	@property
	def Atm(self):
		"""Returns the one and only one Atm object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.atm.atm.Atm)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.atm.atm import Atm
		return self._read(Atm(self), None)

	@property
	def DhcpV4DiscoveredInfo(self):
		"""Returns the one and only one DhcpV4DiscoveredInfo object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv4discoveredinfo.dhcpv4discoveredinfo.DhcpV4DiscoveredInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv4discoveredinfo.dhcpv4discoveredinfo import DhcpV4DiscoveredInfo
		return self._read(DhcpV4DiscoveredInfo(self), None)

	@property
	def DhcpV4Properties(self):
		"""Returns the one and only one DhcpV4Properties object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv4properties.dhcpv4properties.DhcpV4Properties)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv4properties.dhcpv4properties import DhcpV4Properties
		return self._read(DhcpV4Properties(self), None)

	@property
	def DhcpV6DiscoveredInfo(self):
		"""Returns the one and only one DhcpV6DiscoveredInfo object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv6discoveredinfo.dhcpv6discoveredinfo.DhcpV6DiscoveredInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv6discoveredinfo.dhcpv6discoveredinfo import DhcpV6DiscoveredInfo
		return self._read(DhcpV6DiscoveredInfo(self), None)

	@property
	def DhcpV6Properties(self):
		"""Returns the one and only one DhcpV6Properties object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv6properties.dhcpv6properties.DhcpV6Properties)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.dhcpv6properties.dhcpv6properties import DhcpV6Properties
		return self._read(DhcpV6Properties(self), None)

	@property
	def Ethernet(self):
		"""Returns the one and only one Ethernet object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ethernet.ethernet.Ethernet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ethernet.ethernet import Ethernet
		return self._read(Ethernet(self), None)

	@property
	def Gre(self):
		"""Returns the one and only one Gre object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.gre.gre.Gre)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.gre.gre import Gre
		return self._read(Gre(self), None)

	def Ipv4(self, Gateway=None, Ip=None):
		"""Gets child instances of Ipv4 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ipv4 will be returned.

		Args:
			Gateway (str): The IPv4 address of the Gateway to the network, typically an interface on the DUT.
			Ip (str): The 32-bit IPv4 address assigned to this unconnected interface.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv4.ipv4.Ipv4))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv4.ipv4 import Ipv4
		return self._select(Ipv4(self), locals())

	def add_Ipv4(self, Gateway="0.0.0.0", Ip="0.0.0.0", MaskWidth="24"):
		"""Adds a child instance of Ipv4 on the server.

		Args:
			Gateway (str): The IPv4 address of the Gateway to the network, typically an interface on the DUT.
			Ip (str): The 32-bit IPv4 address assigned to this unconnected interface.
			MaskWidth (number): The number of bits in the mask used with the IPv4 address. The default is 24 bits.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv4.ipv4.Ipv4)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv4.ipv4 import Ipv4
		return self._create(Ipv4(self), locals())

	def Ipv6(self, Gateway=None, Ip=None, TrafficClass=None):
		"""Gets child instances of Ipv6 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ipv6 will be returned.

		Args:
			Gateway (str): The IPv6 address of the Gateway to the network,typically an interface on the DUT.
			Ip (str): The 128-bit IPv6 address assigned to this unconnected interface.
			TrafficClass (str): This value ,1 byte long, configures the Traffic Class in the IPv6 header for our IPv6 Neighbour Discovery messages. The default value is 0x00 but the user can modify it to any value.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv6.ipv6.Ipv6))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv6.ipv6 import Ipv6
		return self._select(Ipv6(self), locals())

	def add_Ipv6(self, Gateway=None, Ip=None, PrefixLength="64", TargetLinkLayerAddressOption="False", TrafficClass="0x00"):
		"""Adds a child instance of Ipv6 on the server.

		Args:
			Gateway (str): The IPv6 address of the Gateway to the network,typically an interface on the DUT.
			Ip (str): The 128-bit IPv6 address assigned to this unconnected interface.
			PrefixLength (number): A learned/allocated IPv4 address prefix length (mask) for this interface.
			TargetLinkLayerAddressOption (bool): Tentative Source Link-Layer Address Options for IPv6 Neighbour Discovery. Upon reception of a Tentative Source Link-Layer Address Option in a Neighbour Solicitation for which the receiver has the Target Address configured, a node checks to see if there is a neighbour cache entry with conflicting link-layer address.
			TrafficClass (str): This value ,1 byte long, configures the Traffic Class in the IPv6 header for our IPv6 Neighbour Discovery messages. The default value is 0x00 but the user can modify it to any value.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv6.ipv6.Ipv6)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.ipv6.ipv6 import Ipv6
		return self._create(Ipv6(self), locals())

	@property
	def Unconnected(self):
		"""Returns the one and only one Unconnected object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.unconnected.unconnected.Unconnected)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.unconnected.unconnected import Unconnected
		return self._read(Unconnected(self), None)

	@property
	def Vlan(self):
		"""Returns the one and only one Vlan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.vlan.vlan.Vlan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.vlan.vlan import Vlan
		return self._read(Vlan(self), None)

	@property
	def Description(self):
		"""The identifier for the port including card and port numbers, and the port type.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def Enabled(self):
		"""Enables the selected protocol interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Eui64Id(self):
		"""This is the 64-bit IEEE Modified EUI ID value for the Interface Identifier portion of the IPv6 address.

		Returns:
			str
		"""
		return self._get_attribute('eui64Id')
	@Eui64Id.setter
	def Eui64Id(self, value):
		self._set_attribute('eui64Id', value)

	@property
	def Mtu(self):
		"""The maximum transmission unit for the interfaces created with this range.

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def Type(self):
		"""The identifier or 'tag' for this DHCP option.

		Returns:
			str(default|gre|routed)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def remove(self):
		"""Deletes a child instance of Interface on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def SendArp(self):
		"""Executes the sendArp operation on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendArp', payload=locals(), response_object=None)

	def SendArpAndNS(self):
		"""Executes the sendArpAndNS operation on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendArpAndNS', payload=locals(), response_object=None)

	def SendNs(self):
		"""Executes the sendNs operation on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendNs', payload=locals(), response_object=None)

	def SendPing(self, Arg2):
		"""Executes the sendPing operation on the server.

		Args:
			Arg2 (str): 

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing', payload=locals(), response_object=None)

	def SendRs(self):
		"""Executes the sendRs operation on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendRs', payload=locals(), response_object=None)
