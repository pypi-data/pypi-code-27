from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv6Loopback(Base):
	"""IPV6 Loopback
	"""

	_SDM_NAME = 'ipv6Loopback'

	def __init__(self, parent):
		super(Ipv6Loopback, self).__init__(parent)

	def Bfdv6Interface(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Bfdv6Interface from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Bfdv6Interface will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6interface.Bfdv6Interface))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6interface import Bfdv6Interface
		return self._select(Bfdv6Interface(self), locals())

	def add_Bfdv6Interface(self, AggregateBfdSession="True", ConnectedVia=None, Multiplier="1", Name=None, NoOfSessions="0", StackedLayers=None):
		"""Adds a child instance of Bfdv6Interface on the server.

		Args:
			AggregateBfdSession (bool): If enabled, all interfaces except on VNI 0 will be disabled and grayed-out.
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfSessions (number): The number of configured BFD sessions
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6interface.Bfdv6Interface)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6interface import Bfdv6Interface
		return self._create(Bfdv6Interface(self), locals())

	def BgpIpv6Peer(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpIpv6Peer from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpIpv6Peer will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv6peer.BgpIpv6Peer))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv6peer import BgpIpv6Peer
		return self._select(BgpIpv6Peer(self), locals())

	def add_BgpIpv6Peer(self, BgpLsNoOfASPathSegments="1", BgpLsNoOfClusters="1", BgpLsNoOfCommunities="1", CapabilityIpv4MplsAddPath="False", CapabilityIpv6MplsAddPath="False", ConnectedVia=None, CopyTtl="False", EnSRv6DataPlane="False", EnableEPETraffic="False", EnableReducedEncapsulation="True", EthernetSegmentsCountV6="0", IpVrfToIpVrfType="interfacefullWithUnnumberedCorefacingIRB", Ipv4MplsCapability="False", Ipv4MultipleMplsLabelsCapability="False", Ipv6MplsCapability="False", Ipv6MultipleMplsLabelsCapability="False", MaxSidPerSrh="3", MplsLabelsCountForIpv4MplsRoute="1", MplsLabelsCountForIpv6MplsRoute="1", Multiplier="1", Name=None, NoOfEPEPeers="0", NoOfExtendedCommunities="1", NoOfPeerSet="0", NoOfUserDefinedAfiSafi="0", NumberFlowSpecRangeV4="0", NumberFlowSpecRangeV6="0", NumberSRTEPolicies="0", SRGBRangeCount="1", Srv6Ttl="62", StackedLayers=None, UseStaticPolicy="True"):
		"""Adds a child instance of BgpIpv6Peer on the server.

		Args:
			BgpLsNoOfASPathSegments (number): Number Of AS Path Segments Per Route Range
			BgpLsNoOfClusters (number): Number of Clusters
			BgpLsNoOfCommunities (number): Number of Communities
			CapabilityIpv4MplsAddPath (bool): IPv4 MPLS Add Path Capability
			CapabilityIpv6MplsAddPath (bool): IPv6 MPLS Add Path Capability
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			CopyTtl (bool): Copy TTL from customer packet to outer IPv6 header
			EnSRv6DataPlane (bool): Ingress Peer Supports SRv6 VPN
			EnableEPETraffic (bool): Enable EPE Traffic
			EnableReducedEncapsulation (bool): Enable Reduced Encapsulation in Data-Plane for SRv6
			EthernetSegmentsCountV6 (number): Number of Ethernet Segments
			IpVrfToIpVrfType (str(interfacefullWithCorefacingIRB|interfacefullWithUnnumberedCorefacingIRB|interfaceLess)): IP-VRF-to-IP-VRF Model Type
			Ipv4MplsCapability (bool): IPv4 MPLS Capability
			Ipv4MultipleMplsLabelsCapability (bool): IPv4 Multiple MPLS Labels Capability
			Ipv6MplsCapability (bool): IPv6 MPLS Capability
			Ipv6MultipleMplsLabelsCapability (bool): IPv6 Multiple MPLS Labels Capability
			MaxSidPerSrh (number): Max number of SIDs a SRH can have
			MplsLabelsCountForIpv4MplsRoute (number): MPLS Labels Count For IPv4 MPLS Route
			MplsLabelsCountForIpv6MplsRoute (number): MPLS Labels Count For IPv6 MPLS Route
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfEPEPeers (number): 
			NoOfExtendedCommunities (number): Number of Extended Communities
			NoOfPeerSet (number): 
			NoOfUserDefinedAfiSafi (number): Count of User defined AFI SAFI
			NumberFlowSpecRangeV4 (number): Number of IPv4 Flow Spec Ranges
			NumberFlowSpecRangeV6 (number): Number of IPv6 Flow Spec Ranges
			NumberSRTEPolicies (number): Count of SR TE Policies
			SRGBRangeCount (number): SRGB Range Count
			Srv6Ttl (number): TTL value to be used in outer IPv6 header
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			UseStaticPolicy (bool): If enabled then SRTE policy will be advertised

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv6peer.BgpIpv6Peer)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv6peer import BgpIpv6Peer
		return self._create(BgpIpv6Peer(self), locals())

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

	def Greoipv6(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Greoipv6 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Greoipv6 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.greoipv6.Greoipv6))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.greoipv6 import Greoipv6
		return self._select(Greoipv6(self), locals())

	def add_Greoipv6(self, ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of Greoipv6 on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.greoipv6.Greoipv6)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.greoipv6 import Greoipv6
		return self._create(Greoipv6(self), locals())

	def LdpTargetedRouterV6(self, DescriptiveName=None, Name=None):
		"""Gets child instances of LdpTargetedRouterV6 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LdpTargetedRouterV6 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouterv6.LdpTargetedRouterV6))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouterv6 import LdpTargetedRouterV6
		return self._select(LdpTargetedRouterV6(self), locals())

	def add_LdpTargetedRouterV6(self, ConnectedVia=None, Ipv6peerCount="0", LdpVersion="version1", LeafRangesCountV6="0", Multiplier="1", Name=None, PeerCount="0", RootRangesCountV6="0", StackedLayers=None):
		"""Adds a child instance of LdpTargetedRouterV6 on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Ipv6peerCount (number): The number of ipv6 Target Peers configured for this LDP router
			LdpVersion (str(version1|version2)): Version of LDP. When RFC 5036 is chosen, LDP version is version 1. When draft-pdutta-mpls-ldp-adj-capability-00 is chosen, LDP version is version 2
			LeafRangesCountV6 (number): The number of Leaf Ranges configured for this LDP router
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			PeerCount (number): The number of Target Peers configured for this LDP router
			RootRangesCountV6 (number): The number of Root Ranges configured for this LDP router
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouterv6.LdpTargetedRouterV6)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouterv6 import LdpTargetedRouterV6
		return self._create(LdpTargetedRouterV6(self), locals())

	def MldHost(self, DescriptiveName=None, Name=None):
		"""Gets child instances of MldHost from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of MldHost will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldhost.MldHost))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldhost import MldHost
		return self._select(MldHost(self), locals())

	def add_MldHost(self, ConnectedVia=None, JlMultiplier="1", Multiplier="1", Name=None, NoOfGrpRanges="1", StackedLayers=None):
		"""Adds a child instance of MldHost on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			JlMultiplier (number): No. of Join/Leave messages to send per opertation
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfGrpRanges (number): Defines the number of group range per host required
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldhost.MldHost)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldhost import MldHost
		return self._create(MldHost(self), locals())

	def MldQuerier(self, DescriptiveName=None, Name=None):
		"""Gets child instances of MldQuerier from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of MldQuerier will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldquerier.MldQuerier))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldquerier import MldQuerier
		return self._select(MldQuerier(self), locals())

	def add_MldQuerier(self, ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of MldQuerier on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldquerier.MldQuerier)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mldquerier import MldQuerier
		return self._create(MldQuerier(self), locals())

	def Ntpclock(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ntpclock from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ntpclock will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ntpclock.Ntpclock))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ntpclock import Ntpclock
		return self._select(Ntpclock(self), locals())

	def add_Ntpclock(self, AcceptNTPPacketswithCryptoNAK="False", ConnectedVia=None, IsParentV6="True", Multiplier="1", Name=None, NtpServerCount="1", StackedLayers=None):
		"""Adds a child instance of Ntpclock on the server.

		Args:
			AcceptNTPPacketswithCryptoNAK (bool): Accept NTP Packets with Crypto-NAK
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			IsParentV6 (bool): Parent v6
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NtpServerCount (number): NTP server Count
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ntpclock.Ntpclock)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ntpclock import Ntpclock
		return self._create(Ntpclock(self), locals())

	def Ospfv3(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ospfv3 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ospfv3 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3.Ospfv3))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3 import Ospfv3
		return self._select(Ospfv3(self), locals())

	def add_Ospfv3(self, ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of Ospfv3 on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3.Ospfv3)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3 import Ospfv3
		return self._create(Ospfv3(self), locals())

	def PimV6Interface(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PimV6Interface from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PimV6Interface will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv6interface.PimV6Interface))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv6interface import PimV6Interface
		return self._select(PimV6Interface(self), locals())

	def add_PimV6Interface(self, ConnectedVia=None, CrpRanges="0", JoinPrunes="0", Multiplier="1", Name=None, Sources="0", StackedLayers=None):
		"""Adds a child instance of PimV6Interface on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			CrpRanges (number): Number of C-RP Ranges
			JoinPrunes (number): Number of Join/Prunes
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			Sources (number): Number of Sources
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv6interface.PimV6Interface)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv6interface import PimV6Interface
		return self._create(PimV6Interface(self), locals())

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
	def Address(self):
		"""IPv6 addresses of the devices

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('address')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

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
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

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

	@property
	def Prefix(self):
		"""The length (in bits) of the mask to be used in conjunction with all the addresses created in the range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefix')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	def remove(self):
		"""Deletes a child instance of Ipv6Loopback on the server.

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

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def SendPing(self, DestIP):
		"""Executes the sendPing operation on the server.

		Send ping for selected IPv6 Loopback items.

		Args:
			DestIP (str): This parameter requires a destIP of type kString

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing', payload=locals(), response_object=None)

	def SendPing(self, DestIP, SessionIndices):
		"""Executes the sendPing operation on the server.

		Send ping for selected IPv6 Loopback items.

		Args:
			DestIP (str): This parameter requires a destIP of type kString
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing', payload=locals(), response_object=None)

	def SendPing(self, SessionIndices, DestIP):
		"""Executes the sendPing operation on the server.

		Send ping for selected IPv6 Loopback items.

		Args:
			SessionIndices (str): This parameter requires a destIP of type kString
			DestIP (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ipv6Loopback object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
