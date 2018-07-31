from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetworkGroup(Base):
	"""Describes a set of network clouds with similar configuration and the same multiplicity for devices behind.
	"""

	_SDM_NAME = 'networkGroup'

	def __init__(self, parent):
		super(NetworkGroup, self).__init__(parent)

	def BgpIPRouteProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpIPRouteProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpIPRouteProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpiprouteproperty.BgpIPRouteProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpiprouteproperty import BgpIPRouteProperty
		return self._select(BgpIPRouteProperty(self), locals())

	def add_BgpIPRouteProperty(self, AdvertiseAsBgp3107="False", AdvertiseAsBgp3107Sr="False", AdvertiseAsRfc8277="False", Name=None, NoOfASPathSegmentsPerRouteRange="1", NoOfClusters="1", NoOfCommunities="1", NoOfExternalCommunities="1", NoOfLabels="1", NoOfTlvs="1"):
		"""Adds a child instance of BgpIPRouteProperty on the server.

		Args:
			AdvertiseAsBgp3107 (bool): Will cause this route to be sent as BGP 3107 MPLS SAFI route
			AdvertiseAsBgp3107Sr (bool): Will cause this route to be sent as BGP 3107 SR MPLS SAFI route
			AdvertiseAsRfc8277 (bool): Will cause this route to be sent as RFC 8277 MPLS SAFI route
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of non-random or manually configured AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExternalCommunities (number): Number of Extended Communities
			NoOfLabels (number): Number of Labels
			NoOfTlvs (number): Number of TLVs

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpiprouteproperty.BgpIPRouteProperty)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpiprouteproperty import BgpIPRouteProperty
		return self._create(BgpIPRouteProperty(self), locals())

	def BgpL3VpnRouteProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpL3VpnRouteProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpL3VpnRouteProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpl3vpnrouteproperty.BgpL3VpnRouteProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpl3vpnrouteproperty import BgpL3VpnRouteProperty
		return self._select(BgpL3VpnRouteProperty(self), locals())

	def add_BgpL3VpnRouteProperty(self, EnableIpv4Receiver="False", EnableIpv4Sender="True", Name=None, NoOfASPathSegmentsPerRouteRange="1", NoOfClusters="1", NoOfCommunities="1", NoOfExternalCommunities="1", UseAsIpv4UmhRoutes="False"):
		"""Adds a child instance of BgpL3VpnRouteProperty on the server.

		Args:
			EnableIpv4Receiver (bool): Enable IPv4 Receiver
			EnableIpv4Sender (bool): Enable IPv4 Sender
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of non-random or manually configured AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExternalCommunities (number): Number of Extended Communities
			UseAsIpv4UmhRoutes (bool): Use As IPv4 UMH Routes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpl3vpnrouteproperty.BgpL3VpnRouteProperty)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpl3vpnrouteproperty import BgpL3VpnRouteProperty
		return self._create(BgpL3VpnRouteProperty(self), locals())

	def BgpMVpnReceiverSitesIpv4(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpMVpnReceiverSitesIpv4 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpMVpnReceiverSitesIpv4 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv4.BgpMVpnReceiverSitesIpv4))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv4 import BgpMVpnReceiverSitesIpv4
		return self._select(BgpMVpnReceiverSitesIpv4(self), locals())

	def add_BgpMVpnReceiverSitesIpv4(self, IncludeBierPtainLeafAd="True", Name=None, WildCardLeafAdForBierPta="False"):
		"""Adds a child instance of BgpMVpnReceiverSitesIpv4 on the server.

		Args:
			IncludeBierPtainLeafAd (bool): Include Bier PTA in Leaf A-D
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			WildCardLeafAdForBierPta (bool): Wildcard Leaf A-D For Bier PTA

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv4.BgpMVpnReceiverSitesIpv4)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv4 import BgpMVpnReceiverSitesIpv4
		return self._create(BgpMVpnReceiverSitesIpv4(self), locals())

	def BgpMVpnReceiverSitesIpv6(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpMVpnReceiverSitesIpv6 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpMVpnReceiverSitesIpv6 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv6.BgpMVpnReceiverSitesIpv6))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv6 import BgpMVpnReceiverSitesIpv6
		return self._select(BgpMVpnReceiverSitesIpv6(self), locals())

	def add_BgpMVpnReceiverSitesIpv6(self, IncludeBierPtainLeafAd="True", Name=None, WildCardLeafAdForBierPta="False"):
		"""Adds a child instance of BgpMVpnReceiverSitesIpv6 on the server.

		Args:
			IncludeBierPtainLeafAd (bool): Include Bier PTA in Leaf A-D
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			WildCardLeafAdForBierPta (bool): Wildcard Leaf A-D For Bier PTA

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv6.BgpMVpnReceiverSitesIpv6)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnreceiversitesipv6 import BgpMVpnReceiverSitesIpv6
		return self._create(BgpMVpnReceiverSitesIpv6(self), locals())

	def BgpMVpnSenderSitesIpv4(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpMVpnSenderSitesIpv4 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpMVpnSenderSitesIpv4 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv4.BgpMVpnSenderSitesIpv4))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv4 import BgpMVpnSenderSitesIpv4
		return self._select(BgpMVpnSenderSitesIpv4(self), locals())

	def add_BgpMVpnSenderSitesIpv4(self, Name=None):
		"""Adds a child instance of BgpMVpnSenderSitesIpv4 on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv4.BgpMVpnSenderSitesIpv4)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv4 import BgpMVpnSenderSitesIpv4
		return self._create(BgpMVpnSenderSitesIpv4(self), locals())

	def BgpMVpnSenderSitesIpv6(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpMVpnSenderSitesIpv6 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpMVpnSenderSitesIpv6 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv6.BgpMVpnSenderSitesIpv6))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv6 import BgpMVpnSenderSitesIpv6
		return self._select(BgpMVpnSenderSitesIpv6(self), locals())

	def add_BgpMVpnSenderSitesIpv6(self, Name=None):
		"""Adds a child instance of BgpMVpnSenderSitesIpv6 on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv6.BgpMVpnSenderSitesIpv6)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpmvpnsendersitesipv6 import BgpMVpnSenderSitesIpv6
		return self._create(BgpMVpnSenderSitesIpv6(self), locals())

	def BgpV6IPRouteProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpV6IPRouteProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpV6IPRouteProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6iprouteproperty.BgpV6IPRouteProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6iprouteproperty import BgpV6IPRouteProperty
		return self._select(BgpV6IPRouteProperty(self), locals())

	def add_BgpV6IPRouteProperty(self, AdvertiseAsBgp3107="False", AdvertiseAsBgp3107Sr="False", AdvertiseAsRfc8277="False", Name=None, NoOfASPathSegmentsPerRouteRange="1", NoOfClusters="1", NoOfCommunities="1", NoOfExternalCommunities="1", NoOfLabels="1", NoOfTlvs="1"):
		"""Adds a child instance of BgpV6IPRouteProperty on the server.

		Args:
			AdvertiseAsBgp3107 (bool): Will cause this route to be sent as BGP 3107 MPLS SAFI route
			AdvertiseAsBgp3107Sr (bool): Will cause this route to be sent as BGP 3107 SR MPLS SAFI route
			AdvertiseAsRfc8277 (bool): Will cause this route to be sent as RFC 8277 MPLS SAFI route
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of non-random or manually configured AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExternalCommunities (number): Number of Extended Communities
			NoOfLabels (number): Number of Labels
			NoOfTlvs (number): Number of TLVs

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6iprouteproperty.BgpV6IPRouteProperty)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6iprouteproperty import BgpV6IPRouteProperty
		return self._create(BgpV6IPRouteProperty(self), locals())

	def BgpV6L3VpnRouteProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpV6L3VpnRouteProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpV6L3VpnRouteProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6l3vpnrouteproperty.BgpV6L3VpnRouteProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6l3vpnrouteproperty import BgpV6L3VpnRouteProperty
		return self._select(BgpV6L3VpnRouteProperty(self), locals())

	def add_BgpV6L3VpnRouteProperty(self, EnableIpv6Receiver="False", EnableIpv6Sender="True", Name=None, NoOfASPathSegmentsPerRouteRange="1", NoOfClusters="1", NoOfCommunities="1", NoOfExternalCommunities="1", UseAsIpv6UmhRoutes="False"):
		"""Adds a child instance of BgpV6L3VpnRouteProperty on the server.

		Args:
			EnableIpv6Receiver (bool): Enable IPv6 Receiver
			EnableIpv6Sender (bool): Enable IPv6 Sender
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of non-random or manually configured AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExternalCommunities (number): Number of Extended Communities
			UseAsIpv6UmhRoutes (bool): Use As IPv6 UMH Routes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6l3vpnrouteproperty.BgpV6L3VpnRouteProperty)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv6l3vpnrouteproperty import BgpV6L3VpnRouteProperty
		return self._create(BgpV6L3VpnRouteProperty(self), locals())

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

	def DeviceGroup(self, DescriptiveName=None, Name=None):
		"""Gets child instances of DeviceGroup from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DeviceGroup will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup.DeviceGroup))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup import DeviceGroup
		return self._select(DeviceGroup(self), locals())

	def add_DeviceGroup(self, Multiplier="10", Name=None):
		"""Adds a child instance of DeviceGroup on the server.

		Args:
			Multiplier (number): Number of device instances per parent device instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup.DeviceGroup)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup import DeviceGroup
		return self._create(DeviceGroup(self), locals())

	def DslPools(self, DescriptiveName=None, Name=None):
		"""Gets child instances of DslPools from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DslPools will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dslpools.DslPools))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dslpools import DslPools
		return self._select(DslPools(self), locals())

	def add_DslPools(self, Name=None):
		"""Adds a child instance of DslPools on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dslpools.DslPools)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dslpools import DslPools
		return self._create(DslPools(self), locals())

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

	def IsisL3RouteProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisL3RouteProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisL3RouteProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3routeproperty.IsisL3RouteProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3routeproperty import IsisL3RouteProperty
		return self._select(IsisL3RouteProperty(self), locals())

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

	def LdpFECProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of LdpFECProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LdpFECProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpfecproperty.LdpFECProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpfecproperty import LdpFECProperty
		return self._select(LdpFECProperty(self), locals())

	def LdpIpv6FECProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of LdpIpv6FECProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LdpIpv6FECProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpipv6fecproperty.LdpIpv6FECProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpipv6fecproperty import LdpIpv6FECProperty
		return self._select(LdpIpv6FECProperty(self), locals())

	def MacPools(self, DescriptiveName=None, Name=None):
		"""Gets child instances of MacPools from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of MacPools will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.macpools.MacPools))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.macpools import MacPools
		return self._select(MacPools(self), locals())

	def add_MacPools(self, Name=None, NumberOfAddresses="1", UseVlans="False", VlanCount="1"):
		"""Adds a child instance of MacPools on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfAddresses (number): Number of MAC addresses in the simulated MAC range
			UseVlans (bool): Flag to determine whether VLANs are enabled
			VlanCount (number): Number of active VLANs

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.macpools.MacPools)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.macpools import MacPools
		return self._create(MacPools(self), locals())

	def NetworkGroup(self, DescriptiveName=None, Name=None):
		"""Gets child instances of NetworkGroup from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetworkGroup will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkgroup.NetworkGroup))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkgroup import NetworkGroup
		return self._select(NetworkGroup(self), locals())

	def add_NetworkGroup(self, Multiplier="1", Name=None):
		"""Adds a child instance of NetworkGroup on the server.

		Args:
			Multiplier (number): Number of device instances per parent device instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkgroup.NetworkGroup)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkgroup import NetworkGroup
		return self._create(NetworkGroup(self), locals())

	def NetworkRangeInfo(self, DescriptiveName=None, Name=None):
		"""Gets child instances of NetworkRangeInfo from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetworkRangeInfo will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkrangeinfo.NetworkRangeInfo))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkrangeinfo import NetworkRangeInfo
		return self._select(NetworkRangeInfo(self), locals())

	def add_NetworkRangeInfo(self, Name=None):
		"""Adds a child instance of NetworkRangeInfo on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkrangeinfo.NetworkRangeInfo)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networkrangeinfo import NetworkRangeInfo
		return self._create(NetworkRangeInfo(self), locals())

	def NetworkTopology(self):
		"""Gets child instances of NetworkTopology from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetworkTopology will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networktopology.NetworkTopology))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networktopology import NetworkTopology
		return self._select(NetworkTopology(self), locals())

	def add_NetworkTopology(self):
		"""Adds a child instance of NetworkTopology on the server.

		Args:

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networktopology.NetworkTopology)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.networktopology import NetworkTopology
		return self._create(NetworkTopology(self), locals())

	def OspfRouteProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfRouteProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfRouteProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfrouteproperty.OspfRouteProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfrouteproperty import OspfRouteProperty
		return self._select(OspfRouteProperty(self), locals())

	def Ospfv3RouteProperty(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ospfv3RouteProperty from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ospfv3RouteProperty will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3routeproperty.Ospfv3RouteProperty))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3routeproperty import Ospfv3RouteProperty
		return self._select(Ospfv3RouteProperty(self), locals())

	def add_Ospfv3RouteProperty(self, Name=None):
		"""Adds a child instance of Ospfv3RouteProperty on the server.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3routeproperty.Ospfv3RouteProperty)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3routeproperty import Ospfv3RouteProperty
		return self._create(Ospfv3RouteProperty(self), locals())

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
	def Enabled(self):
		"""Enables/disables device.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enabled')

	@property
	def Multiplier(self):
		"""Number of device instances per parent device instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

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

	def remove(self):
		"""Deletes a child instance of NetworkGroup on the server.

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
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./networkGroup object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Targets):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./networkGroup object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
