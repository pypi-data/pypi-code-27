from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv6PrefixPools(Base):
	"""Represents an IPv6 address
	"""

	_SDM_NAME = 'ipv6PrefixPools'

	def __init__(self, parent):
		super(Ipv6PrefixPools, self).__init__(parent)

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

	@property
	def AddrStepSupported(self):
		"""Indicates whether the Route Range provider allows address increment step of more than one

		Returns:
			bool
		"""
		return self._get_attribute('addrStepSupported')
	@AddrStepSupported.setter
	def AddrStepSupported(self, value):
		self._set_attribute('addrStepSupported', value)

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
	def LastNetworkAddress(self):
		"""Last Address of host/network address pool in the simulated IPv6 host/network range

		Returns:
			list(str)
		"""
		return self._get_attribute('lastNetworkAddress')

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
	def NetworkAddress(self):
		"""First address of host/network address pool in the simulated IPv6 host/network range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkAddress')

	@property
	def NumberOfAddresses(self):
		"""Number of host/network addresses in the simulated IPv6 host/network range

		Returns:
			number
		"""
		return self._get_attribute('numberOfAddresses')
	@NumberOfAddresses.setter
	def NumberOfAddresses(self, value):
		self._set_attribute('numberOfAddresses', value)

	@property
	def PrefixAddrStep(self):
		"""The difference between each address, and its next, in the IPv6 host/network range.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixAddrStep')

	@property
	def PrefixLength(self):
		"""The length (in bits) of the mask to be used in conjunction with all the addresses created in the range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	def remove(self):
		"""Deletes a child instance of Ipv6PrefixPools on the server.

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
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6PrefixPools object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Targets):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6PrefixPools object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
