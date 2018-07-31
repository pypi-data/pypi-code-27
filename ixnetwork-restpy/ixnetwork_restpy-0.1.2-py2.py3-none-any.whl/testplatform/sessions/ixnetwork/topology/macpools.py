from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MacPools(Base):
	"""Represents an Ethernet device set
	"""

	_SDM_NAME = 'macPools'

	def __init__(self, parent):
		super(MacPools, self).__init__(parent)

	def CMacProperties(self, DescriptiveName=None, Name=None):
		"""Gets child instances of CMacProperties from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of CMacProperties will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties.CMacProperties))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties import CMacProperties
		return self._select(CMacProperties(self), locals())

	def add_CMacProperties(self, Name=None, NoOfASPathSegmentsPerRouteRange="0", NoOfClusters="1", NoOfCommunities="1", NoOfExtendedCommunity="1"):
		"""Adds a child instance of CMacProperties on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExtendedCommunity (number): Number of Extended Communities

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties.CMacProperties)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties import CMacProperties
		return self._create(CMacProperties(self), locals())

	def Connector(self):
		"""Gets child instances of Connector from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Connector will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return self._select(Connector(self), locals())

	def add_Connector(self, ConnectedTo=None):
		"""Adds a child instance of Connector on the server.

		Args:
			ConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): Scenario element this connector is connecting to

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return self._create(Connector(self), locals())

	def EvpnIPv4PrefixRange(self, DescriptiveName=None, Name=None):
		"""Gets child instances of EvpnIPv4PrefixRange from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of EvpnIPv4PrefixRange will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange.EvpnIPv4PrefixRange))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange import EvpnIPv4PrefixRange
		return self._select(EvpnIPv4PrefixRange(self), locals())

	def add_EvpnIPv4PrefixRange(self, Name=None, NoOfASPathSegmentsPerRouteRange="0", NoOfClusters="1", NoOfCommunities="1", NoOfExtendedCommunity="1"):
		"""Adds a child instance of EvpnIPv4PrefixRange on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExtendedCommunity (number): Number of Extended Communities

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange.EvpnIPv4PrefixRange)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange import EvpnIPv4PrefixRange
		return self._create(EvpnIPv4PrefixRange(self), locals())

	def EvpnIPv6PrefixRange(self, DescriptiveName=None, Name=None):
		"""Gets child instances of EvpnIPv6PrefixRange from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of EvpnIPv6PrefixRange will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange.EvpnIPv6PrefixRange))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange import EvpnIPv6PrefixRange
		return self._select(EvpnIPv6PrefixRange(self), locals())

	def add_EvpnIPv6PrefixRange(self, Name=None, NoOfASPathSegmentsPerRouteRange="0", NoOfClusters="1", NoOfCommunities="1", NoOfExtendedCommunity="1"):
		"""Adds a child instance of EvpnIPv6PrefixRange on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExtendedCommunity (number): Number of Extended Communities

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange.EvpnIPv6PrefixRange)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange import EvpnIPv6PrefixRange
		return self._create(EvpnIPv6PrefixRange(self), locals())

	def Ipv4PrefixPools(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ipv4PrefixPools from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ipv4PrefixPools will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4prefixpools.Ipv4PrefixPools))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4prefixpools import Ipv4PrefixPools
		return self._select(Ipv4PrefixPools(self), locals())

	def add_Ipv4PrefixPools(self, AddrStepSupported="False", Name=None, NumberOfAddresses="1"):
		"""Adds a child instance of Ipv4PrefixPools on the server.

		Args:
			AddrStepSupported (bool): Indicates whether the Route Range provider allows route range address increment step of more than one
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfAddresses (number): Number of host/network addresses in the simulated IPv4 host/network range

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4prefixpools.Ipv4PrefixPools)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4prefixpools import Ipv4PrefixPools
		return self._create(Ipv4PrefixPools(self), locals())

	def Ipv6PrefixPools(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ipv6PrefixPools from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ipv6PrefixPools will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6prefixpools.Ipv6PrefixPools))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6prefixpools import Ipv6PrefixPools
		return self._select(Ipv6PrefixPools(self), locals())

	def add_Ipv6PrefixPools(self, AddrStepSupported="False", Name=None, NumberOfAddresses="1"):
		"""Adds a child instance of Ipv6PrefixPools on the server.

		Args:
			AddrStepSupported (bool): Indicates whether the Route Range provider allows address increment step of more than one
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfAddresses (number): Number of host/network addresses in the simulated IPv6 host/network range

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6prefixpools.Ipv6PrefixPools)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6prefixpools import Ipv6PrefixPools
		return self._create(Ipv6PrefixPools(self), locals())

	def IsisSpbMacCloudConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisSpbMacCloudConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisSpbMacCloudConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbmaccloudconfig.IsisSpbMacCloudConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbmaccloudconfig import IsisSpbMacCloudConfig
		return self._select(IsisSpbMacCloudConfig(self), locals())

	def add_IsisSpbMacCloudConfig(self, Name=None):
		"""Adds a child instance of IsisSpbMacCloudConfig on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbmaccloudconfig.IsisSpbMacCloudConfig)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbmaccloudconfig import IsisSpbMacCloudConfig
		return self._create(IsisSpbMacCloudConfig(self), locals())

	def IsisTrillUCastMacConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisTrillUCastMacConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisTrillUCastMacConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillucastmacconfig.IsisTrillUCastMacConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillucastmacconfig import IsisTrillUCastMacConfig
		return self._select(IsisTrillUCastMacConfig(self), locals())

	def Tag(self, Name=None):
		"""Gets child instances of Tag from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Tag will be returned.

		Args:
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._select(Tag(self), locals())

	def add_Tag(self, Enabled="False", Name=None):
		"""Adds a child instance of Tag on the server.

		Args:
			Enabled (bool): Enables/disables tags
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._create(Tag(self), locals())

	def Vlan(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Vlan from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Vlan will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vlan.Vlan))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vlan import Vlan
		return self._select(Vlan(self), locals())

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
	def EnableVlans(self):
		"""Enables VLANs for the sessions

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableVlans')

	@property
	def LastMacAddress(self):
		"""Last Address of network addresses in the simulated MAC network range

		Returns:
			list(str)
		"""
		return self._get_attribute('lastMacAddress')

	@property
	def Mac(self):
		"""MAC addresses of the devices

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mac')

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
	def NumberOfAddresses(self):
		"""Number of MAC addresses in the simulated MAC range

		Returns:
			number
		"""
		return self._get_attribute('numberOfAddresses')
	@NumberOfAddresses.setter
	def NumberOfAddresses(self, value):
		self._set_attribute('numberOfAddresses', value)

	@property
	def PrefixLength(self):
		"""The length (in bits) of the mask to be used in conjunction with all the addresses created in the range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def UseVlans(self):
		"""Flag to determine whether VLANs are enabled

		Returns:
			bool
		"""
		return self._get_attribute('useVlans')
	@UseVlans.setter
	def UseVlans(self, value):
		self._set_attribute('useVlans', value)

	@property
	def VlanCount(self):
		"""Number of active VLANs

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	def remove(self):
		"""Deletes a child instance of MacPools on the server.

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

	def Start(self, Targets):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./macPools object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Targets):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./macPools object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
