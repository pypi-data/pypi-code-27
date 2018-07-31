from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Pppoxclient(Base):
	"""PPPoX Client
	"""

	_SDM_NAME = 'pppoxclient'

	def __init__(self, parent):
		super(Pppoxclient, self).__init__(parent)

	def Bfdv4Interface(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Bfdv4Interface from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Bfdv4Interface will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv4interface.Bfdv4Interface))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv4interface import Bfdv4Interface
		return self._select(Bfdv4Interface(self), locals())

	def add_Bfdv4Interface(self, AggregateBfdSession="True", ConnectedVia=None, Multiplier="1", Name=None, NoOfSessions="0", StackedLayers=None):
		"""Adds a child instance of Bfdv4Interface on the server.

		Args:
			AggregateBfdSession (bool): If enabled, all interfaces except on VNI 0 will be disabled and grayed-out.
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfSessions (number): The number of configured BFD sessions
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv4interface.Bfdv4Interface)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv4interface import Bfdv4Interface
		return self._create(Bfdv4Interface(self), locals())

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

	def BgpIpv4Peer(self, DescriptiveName=None, Name=None):
		"""Gets child instances of BgpIpv4Peer from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of BgpIpv4Peer will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4peer.BgpIpv4Peer))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4peer import BgpIpv4Peer
		return self._select(BgpIpv4Peer(self), locals())

	def add_BgpIpv4Peer(self, BgpLsNoOfASPathSegments="1", BgpLsNoOfClusters="1", BgpLsNoOfCommunities="1", CapabilityIpv4MplsAddPath="False", CapabilityIpv6MplsAddPath="False", ConnectedVia=None, EnableEPETraffic="False", EthernetSegmentsCountV4="0", IpVrfToIpVrfType="interfacefullWithUnnumberedCorefacingIRB", Ipv4MplsCapability="False", Ipv4MultipleMplsLabelsCapability="False", Ipv6MplsCapability="False", Ipv6MultipleMplsLabelsCapability="False", MplsLabelsCountForIpv4MplsRoute="1", MplsLabelsCountForIpv6MplsRoute="1", Multiplier="1", Name=None, NoOfEPEPeers="0", NoOfExtendedCommunities="1", NoOfPeerSet="0", NoOfUserDefinedAfiSafi="0", NumberFlowSpecRangeV4="0", NumberFlowSpecRangeV6="0", NumberSRTEPolicies="0", SRGBRangeCount="1", StackedLayers=None):
		"""Adds a child instance of BgpIpv4Peer on the server.

		Args:
			BgpLsNoOfASPathSegments (number): Number Of AS Path Segments Per Route Range
			BgpLsNoOfClusters (number): Number of Clusters
			BgpLsNoOfCommunities (number): Number of Communities
			CapabilityIpv4MplsAddPath (bool): IPv4 MPLS Add Path Capability
			CapabilityIpv6MplsAddPath (bool): IPv6 MPLS Add Path Capability
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			EnableEPETraffic (bool): Enable EPE Traffic
			EthernetSegmentsCountV4 (number): Number of Ethernet Segments
			IpVrfToIpVrfType (str(interfacefullWithCorefacingIRB|interfacefullWithUnnumberedCorefacingIRB|interfaceLess)): IP-VRF-to-IP-VRF Model Type
			Ipv4MplsCapability (bool): IPv4 MPLS Capability
			Ipv4MultipleMplsLabelsCapability (bool): IPv4 Multiple MPLS Labels Capability
			Ipv6MplsCapability (bool): IPv6 MPLS Capability
			Ipv6MultipleMplsLabelsCapability (bool): IPv6 Multiple MPLS Labels Capability
			MplsLabelsCountForIpv4MplsRoute (number): MPLS Labels Count For IPv4 MPLS Route
			MplsLabelsCountForIpv6MplsRoute (number): MPLS Labels Count For IPv6 MPLS Route
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfEPEPeers (number): 
			NoOfExtendedCommunities (number): Number of Extended Communities
			NoOfPeerSet (number): 
			NoOfUserDefinedAfiSafi (number): Count of User Defined AFI SAFI
			NumberFlowSpecRangeV4 (number): Number of IPv4 Flow Spec Ranges
			NumberFlowSpecRangeV6 (number): Number of IPv6 Flow Spec Ranges
			NumberSRTEPolicies (number): Count of SR TE Policies
			SRGBRangeCount (number): SRGB Range Count
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4peer.BgpIpv4Peer)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4peer import BgpIpv4Peer
		return self._create(BgpIpv4Peer(self), locals())

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

	def Dhcpv6client(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Dhcpv6client from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Dhcpv6client will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client.Dhcpv6client))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client import Dhcpv6client
		return self._select(Dhcpv6client(self), locals())

	def add_Dhcpv6client(self, ConnectedVia=None, EnableStateless="False", MaxNoPerClient="1", Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of Dhcpv6client on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			EnableStateless (bool): Enables DHCP stateless.
			MaxNoPerClient (number): Maximum number of Addresses/Prefixes accepted by a Client in a negotiation.
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client.Dhcpv6client)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client import Dhcpv6client
		return self._create(Dhcpv6client(self), locals())

	def Geneve(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Geneve from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Geneve will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.geneve.Geneve))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.geneve import Geneve
		return self._select(Geneve(self), locals())

	def add_Geneve(self, ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of Geneve on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.geneve.Geneve)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.geneve import Geneve
		return self._create(Geneve(self), locals())

	def IgmpHost(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IgmpHost from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IgmpHost will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmphost.IgmpHost))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmphost import IgmpHost
		return self._select(IgmpHost(self), locals())

	def add_IgmpHost(self, ConnectedVia=None, JlMultiplier="1", Multiplier="1", Name=None, NoOfGrpRanges="1", StackedLayers=None):
		"""Adds a child instance of IgmpHost on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			JlMultiplier (number): No. of Join/Leave messages to send per opertation
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfGrpRanges (number): Defines the number of group range per host required
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmphost.IgmpHost)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmphost import IgmpHost
		return self._create(IgmpHost(self), locals())

	def IgmpQuerier(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IgmpQuerier from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IgmpQuerier will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpquerier.IgmpQuerier))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpquerier import IgmpQuerier
		return self._select(IgmpQuerier(self), locals())

	def add_IgmpQuerier(self, ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of IgmpQuerier on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpquerier.IgmpQuerier)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpquerier import IgmpQuerier
		return self._create(IgmpQuerier(self), locals())

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

	def MplsOam(self, DescriptiveName=None, Name=None):
		"""Gets child instances of MplsOam from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of MplsOam will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplsoam.MplsOam))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplsoam import MplsOam
		return self._select(MplsOam(self), locals())

	def add_MplsOam(self, ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of MplsOam on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplsoam.MplsOam)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplsoam import MplsOam
		return self._create(MplsOam(self), locals())

	def NetconfClient(self, DescriptiveName=None, Name=None):
		"""Gets child instances of NetconfClient from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetconfClient will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfclient.NetconfClient))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfclient import NetconfClient
		return self._select(NetconfClient(self), locals())

	def add_NetconfClient(self, ConnectedVia=None, Multiplier="1", Name=None, NumberOfCommandSnippetsPerClient="2", StackedLayers=None):
		"""Adds a child instance of NetconfClient on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfCommandSnippetsPerClient (number): Number of Command Snippets per client.Maximum 100 are allowed per client.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfclient.NetconfClient)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfclient import NetconfClient
		return self._create(NetconfClient(self), locals())

	def NetconfServer(self, DescriptiveName=None, Name=None):
		"""Gets child instances of NetconfServer from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetconfServer will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfserver.NetconfServer))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfserver import NetconfServer
		return self._select(NetconfServer(self), locals())

	def add_NetconfServer(self, ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of NetconfServer on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfserver.NetconfServer)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.netconfserver import NetconfServer
		return self._create(NetconfServer(self), locals())

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

	def Ospfv2(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ospfv2 from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ospfv2 will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv2.Ospfv2))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv2 import Ospfv2
		return self._select(Ospfv2(self), locals())

	def add_Ospfv2(self, ConnectedVia=None, EnableFast2wayConvergence="True", Multiplier="1", Name=None, SrlgCount="1", StackedLayers=None):
		"""Adds a child instance of Ospfv2 on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			EnableFast2wayConvergence (bool): Enable 2-way Adj Fast Convergence
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SrlgCount (number): This field value shows how many SRLG Value columns would be there in the GUI.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv2.Ospfv2)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv2 import Ospfv2
		return self._create(Ospfv2(self), locals())

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

	def Pcc(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Pcc from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Pcc will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcc.Pcc))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcc import Pcc
		return self._select(Pcc(self), locals())

	def add_Pcc(self, Active_pre_established_lsps="0", ConnectedVia=None, ExpectedInitiatedLspsForTraffic="0", Multiplier="1", Name=None, NumberOfBackupPCEs="0", PreEstablishedSrLspsPerPcc="0", RequestedLspsPerPcc="0", StackedLayers=None):
		"""Adds a child instance of Pcc on the server.

		Args:
			Active_pre_established_lsps (number): 
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			ExpectedInitiatedLspsForTraffic (number): Based on the value in this control the number of Expected Initiated LSPs for Traffic can be configured. This is used for traffic only.
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfBackupPCEs (number): Number of Backup PCEs
			PreEstablishedSrLspsPerPcc (number): Pre-Established SR LSPs per PCC
			RequestedLspsPerPcc (number): Requested LSPs per PCC
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcc.Pcc)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcc import Pcc
		return self._create(Pcc(self), locals())

	def Pce(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Pce from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Pce will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pce.Pce))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pce import Pce
		return self._select(Pce(self), locals())

	def add_Pce(self, ConnectedVia=None, Multiplier="1", Name=None, PceActionMode="none", StackedLayers=None):
		"""Adds a child instance of Pce on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			PceActionMode (str(none|reset|rsvpPcInitiate|rsvpPcrep|rsvpPcupd|srPcrep)): PCE Mode of Action
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pce.Pce)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pce import Pce
		return self._create(Pce(self), locals())

	def PimV4Interface(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PimV4Interface from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PimV4Interface will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv4interface.PimV4Interface))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv4interface import PimV4Interface
		return self._select(PimV4Interface(self), locals())

	def add_PimV4Interface(self, ConnectedVia=None, CrpRanges="0", JoinPrunes="0", Multiplier="1", Name=None, Sources="0", StackedLayers=None):
		"""Adds a child instance of PimV4Interface on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			CrpRanges (number): Number of C-RP Ranges
			JoinPrunes (number): Number of Join/Prunes
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			Sources (number): Number of Sources
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv4interface.PimV4Interface)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pimv4interface import PimV4Interface
		return self._create(PimV4Interface(self), locals())

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

	def Vxlan(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Vxlan from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Vxlan will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vxlan.Vxlan))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vxlan import Vxlan
		return self._select(Vxlan(self), locals())

	def add_Vxlan(self, ConnectedVia=None, EnableStaticInfo="False", ExternalLearning="False", Multiplier="1", Name=None, OvsdbConnectorMultiplier="1", RunningMode="none", StackedLayers=None, StaticInfoCount="1"):
		"""Adds a child instance of Vxlan on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			EnableStaticInfo (bool): If true, VXLAN will use unicast entries for VTEP information instead of multicast learning.
			ExternalLearning (bool): If true, VXLAN will use information received from another protocol which will handle the learning mechanism.
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			OvsdbConnectorMultiplier (number): Ovsdb to Vxlan multiplier, when part of OVSDB Server stack.
			RunningMode (str(none|ovsdbControllerBfdStack|ovsdbStack)): There will be different behaviours based on role (normal=0, ovsdb controller stack=1, bfd stack=2.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StaticInfoCount (number): number of unicast VTEP

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vxlan.Vxlan)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.vxlan import Vxlan
		return self._create(Vxlan(self), locals())

	@property
	def AcMatchMac(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acMatchMac')

	@property
	def AcMatchName(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acMatchName')

	@property
	def AcOptions(self):
		"""Indicates PPPoE AC retrieval mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acOptions')

	@property
	def ActualRateDownstream(self):
		"""This parameter specifies the value to be included in the vendor specific PPPoE tag. It is the actual downstream data rate (sub-option 0x81), in kbps.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('actualRateDownstream')

	@property
	def ActualRateUpstream(self):
		"""This parameter specifies the value to be included in the vendor specific PPPoE tag. It is the actual upstream data rate (sub-option 0x82), in kbps.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('actualRateUpstream')

	@property
	def AgentAccessAggregationCircuitId(self):
		"""The value to be inserted into the Agent Access-Aggregation-Circuit-ID-ASCII-Value field of the PPPoX tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('agentAccessAggregationCircuitId')

	@property
	def AgentCircuitId(self):
		"""The value to be inserted into the Agent Circuit ID field of the PPPoX tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('agentCircuitId')

	@property
	def AgentRemoteId(self):
		"""The value to be inserted into the Agent Remote ID field of the PPPoX tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('agentRemoteId')

	@property
	def AuthRetries(self):
		"""Number of PPP authentication retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authRetries')

	@property
	def AuthTimeout(self):
		"""Timeout for PPP authentication, in seconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authTimeout')

	@property
	def AuthType(self):
		"""The authentication type to use during link setup.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authType')

	@property
	def ChapName(self):
		"""User name when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapName')

	@property
	def ChapSecret(self):
		"""Secret when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapSecret')

	@property
	def ClientDnsOptions(self):
		"""The client DNS options.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientDnsOptions')

	@property
	def ClientLocalIp(self):
		"""The requested IPv4 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientLocalIp')

	@property
	def ClientLocalIpv6Iid(self):
		"""The requested IPv6 Interface Identifier (IID).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientLocalIpv6Iid')

	@property
	def ClientNcpOptions(self):
		"""The NCP configuration mode for IPv4 addressing.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientNcpOptions')

	@property
	def ClientNetmask(self):
		"""The netmask that the client will use with the assigned IP address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientNetmask')

	@property
	def ClientNetmaskOptions(self):
		"""The client netmask option.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientNetmaskOptions')

	@property
	def ClientPrimaryDnsAddress(self):
		"""This is the primary DNS server address that the client requests from the server when the value of the Client DNS Options field is set to 'Request Primary only' or 'Request Primary and Secondary'.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientPrimaryDnsAddress')

	@property
	def ClientSecondaryDnsAddress(self):
		"""This is the secondary DNS server address that the client requests from the server when the value of the Client DNS Options field is set to 'Request Primary and Secondary'.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSecondaryDnsAddress')

	@property
	def ClientSignalIWF(self):
		"""This parameter enables or disables the insertion of sub-option 0xFE (signaling of interworked sessions) into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalIWF')

	@property
	def ClientSignalLoopChar(self):
		"""This parameter enables or disables the insertion of sub-options 0x81 and 0x82 into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalLoopChar')

	@property
	def ClientSignalLoopEncapsulation(self):
		"""This parameter enables or disables the insertion of sub-option 0x90 into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalLoopEncapsulation')

	@property
	def ClientSignalLoopId(self):
		"""This parameter enables or disables the insertion of sub-options 0x01 , 0x02, 0x03 (Remote ID,Circuit ID and Access Aggregation Circuit ID) into the DSL tag in PADI and PADR packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientSignalLoopId')

	@property
	def ClientV6NcpOptions(self):
		"""The NCP configuration mode for IPv6 addressing.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientV6NcpOptions')

	@property
	def ClientWinsOptions(self):
		"""Specifies the mode in which WINS host addresses are configured.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientWinsOptions')

	@property
	def ClientWinsPrimaryAddress(self):
		"""Specifies the primary WINS address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientWinsPrimaryAddress')

	@property
	def ClientWinsSecondaryAddress(self):
		"""Specifies the secondary WINS address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientWinsSecondaryAddress')

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
	def DataLink(self):
		"""A one-byte field included with sub-option 0x90.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dataLink')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DiscoveredIpv4Addresses(self):
		"""The discovered IPv4 addresses.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredIpv4Addresses')

	@property
	def DiscoveredIpv6Addresses(self):
		"""The discovered IPv6 addresses.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredIpv6Addresses')

	@property
	def DiscoveredMacs(self):
		"""The discovered remote MAC address.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredMacs')

	@property
	def DiscoveredRemoteSessionIds(self):
		"""Remote session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteSessionIds')

	@property
	def DiscoveredRemoteTunnelIds(self):
		"""Remote tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteTunnelIds')

	@property
	def DiscoveredSessionIds(self):
		"""The negotiated session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredSessionIds')

	@property
	def DiscoveredTunnelIPs(self):
		"""The discovered remote tunnel IP.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredTunnelIPs')

	@property
	def DiscoveredTunnelIds(self):
		"""The negotiated tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredTunnelIds')

	@property
	def DomainList(self):
		"""Configure domain group settings

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('domainList')

	@property
	def DslTypeTlv(self):
		"""DSL Type to be advertised in PPPoE VSA Tag. For undefined DSL type user has to select User-defined DSL Type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dslTypeTlv')

	@property
	def EchoReqInterval(self):
		"""Keep alive interval, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoReqInterval')

	@property
	def EnableDomainGroups(self):
		"""Enable domain groups

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDomainGroups')

	@property
	def EnableEchoReq(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableEchoReq')

	@property
	def EnableEchoRsp(self):
		"""?

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableEchoRsp')

	@property
	def EnableHostUniq(self):
		"""Enables PPPoE Host-Uniq tag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHostUniq')

	@property
	def EnableMaxPayload(self):
		"""Enables PPPoE Max Payload tag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableMaxPayload')

	@property
	def EnableRedial(self):
		"""If checked, PPPoE redial is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRedial')

	@property
	def Encaps1(self):
		"""A one-byte field included with sub-option 0x90.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('encaps1')

	@property
	def Encaps2(self):
		"""A one-byte field included with sub-option 0x90.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('encaps2')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def HostUniq(self):
		"""Indicates Host-Uniq Tag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostUniq')

	@property
	def HostUniqLength(self):
		"""Host-Uniq Length, in bytes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostUniqLength')

	@property
	def LcpAccm(self):
		"""Async-Control-Character-Map

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpAccm')

	@property
	def LcpEnableAccm(self):
		"""Enable Async-Control-Character-Map

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpEnableAccm')

	@property
	def LcpMaxFailure(self):
		"""Number of Configure-Nak packets sent without sending a Configure-Ack before assuming that configuration is not converging. Any further Configure-Nak packets for peer requested options are converted to Configure-Reject packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpMaxFailure')

	@property
	def LcpRetries(self):
		"""Number of LCP retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpRetries')

	@property
	def LcpStartDelay(self):
		"""Delay time in milliseconds to wait before sending LCP Config Request packet

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpStartDelay')

	@property
	def LcpTermRetries(self):
		"""Number of LCP Termination Retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpTermRetries')

	@property
	def LcpTimeout(self):
		"""Timeout for LCP phase, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lcpTimeout')

	@property
	def MaxPayload(self):
		"""Max Payload

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxPayload')

	@property
	def MruNegotiation(self):
		"""Enable MRU Negotiation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mruNegotiation')

	@property
	def Mtu(self):
		"""Max Transmit Unit for PPP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mtu')

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
	def NcpRetries(self):
		"""Number of NCP retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ncpRetries')

	@property
	def NcpTimeout(self):
		"""Timeout for NCP phase, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ncpTimeout')

	@property
	def NcpType(self):
		"""IP address type (IPv4 or IPv6) for Network Control Protocol

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ncpType')

	@property
	def PadiRetries(self):
		"""Number of PADI Retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padiRetries')

	@property
	def PadiTimeout(self):
		"""Timeout for PADI no response, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padiTimeout')

	@property
	def PadrRetries(self):
		"""Number of PADR Retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padrRetries')

	@property
	def PadrTimeout(self):
		"""Timeout for PADR no response, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('padrTimeout')

	@property
	def PapPassword(self):
		"""Password when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papPassword')

	@property
	def PapUser(self):
		"""User name when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papUser')

	@property
	def PonTypeTlv(self):
		"""PON Type to be advertised in PPPoE VSA Tag. For undefined PON type user has to select User-defined PON Type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ponTypeTlv')

	@property
	def RedialMax(self):
		"""Maximum number of PPPoE redials

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redialMax')

	@property
	def RedialTimeout(self):
		"""PPPoE redial timeout, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redialTimeout')

	@property
	def ServiceName(self):
		"""Access Concentrator Service Name - this option is only available for PPP servers.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serviceName')

	@property
	def ServiceOptions(self):
		"""Indicates PPPoE service retrieval mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serviceOptions')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[cLS_CFG_REJ_AUTH|cLS_CHAP_PEER_DET_FAIL|cLS_CHAP_PEER_RESP_BAD|cLS_CODE_REJ_IPCP|cLS_CODE_REJ_IPV6CP|cLS_CODE_REJ_LCP|cLS_ERR_PPP_NO_BUF|cLS_ERR_PPP_SEND_PKT|cLS_LINK_DISABLE|cLS_LOC_IPADDR_BROADCAST|cLS_LOC_IPADDR_CLASS_E|cLS_LOC_IPADDR_INVAL_ACKS_0|cLS_LOC_IPADDR_INVAL_ACKS_DIFF|cLS_LOC_IPADDR_LOOPBACK|cLS_LOC_IPADDR_PEER_MATCH_LOC|cLS_LOC_IPADDR_PEER_NO_GIVE|cLS_LOC_IPADDR_PEER_NO_HELP|cLS_LOC_IPADDR_PEER_NO_TAKE|cLS_LOC_IPADDR_PEER_REJ|cLS_LOOPBACK_DETECT|cLS_NO_NCP|cLS_NONE|cLS_PAP_BAD_PASSWD|cLS_PEER_DISCONNECTED|cLS_PEER_DISCONNECTED_NEGO|cLS_PEER_IPADDR_MATCH_LOC|cLS_PEER_IPADDR_PEER_NO_SET|cLS_PPOE_AC_SYSTEM_ERROR|cLS_PPOE_GENERIC_ERROR|cLS_PPP_DISABLE|cLS_PPPOE_NO_HOST_UNIQ|cLS_PPPOE_PADI_TIMEOUT|cLS_PPPOE_PADO_TIMEOUT|cLS_PPPOE_PADR_TIMEOUT|cLS_PROTO_REJ_IPCP|cLS_PROTO_REJ_IPv6CP|cLS_TIMEOUT_CHAP_CHAL|cLS_TIMEOUT_CHAP_RESP|cLS_TIMEOUT_IPCP_CFG_REQ|cLS_TIMEOUT_IPV6CP_CFG_REQ|cLS_TIMEOUT_IPV6CP_RA|cLS_TIMEOUT_LCP_CFG_REQ|cLS_TIMEOUT_LCP_ECHO_REQ|cLS_TIMEOUT_PAP_AUTH_REQ|cLS_TUN_AUTH_FAILED|cLS_TUN_NO_RESOURCES|cLS_TUN_TIMEOUT_ICRQ|cLS_TUN_TIMEOUT_SCCRQ|cLS_TUN_VENDOR_SPECIFIC_ERR])
		"""
		return self._get_attribute('sessionInfo')

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

	@property
	def UnlimitedRedialAttempts(self):
		"""If checked, PPPoE unlimited redial attempts is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unlimitedRedialAttempts')

	@property
	def UserDefinedDslType(self):
		"""User Defined DSL-Type Value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('userDefinedDslType')

	@property
	def UserDefinedPonType(self):
		"""User Defined PON-Type Value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('userDefinedPonType')

	def remove(self):
		"""Deletes a child instance of Pppoxclient on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def CloseIpcp(self):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX items.

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('closeIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX items.

		Args:
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('closeIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX items.

		Args:
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('closeIpcp', payload=locals(), response_object=None)

	def CloseIpv6cp(self):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX items.

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('closeIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX items.

		Args:
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('closeIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX items.

		Args:
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('closeIpv6cp', payload=locals(), response_object=None)

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

	def OpenIpcp(self):
		"""Executes the openIpcp operation on the server.

		Open IPCP for selected PPPoX items.

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('openIpcp', payload=locals(), response_object=None)

	def OpenIpcp(self, SessionIndices):
		"""Executes the openIpcp operation on the server.

		Open IPCP for selected PPPoX items.

		Args:
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('openIpcp', payload=locals(), response_object=None)

	def OpenIpcp(self, SessionIndices):
		"""Executes the openIpcp operation on the server.

		Open IPCP for selected PPPoX items.

		Args:
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('openIpcp', payload=locals(), response_object=None)

	def OpenIpv6cp(self):
		"""Executes the openIpv6cp operation on the server.

		Open IPv6CP for selected PPPoX items.

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('openIpv6cp', payload=locals(), response_object=None)

	def OpenIpv6cp(self, SessionIndices):
		"""Executes the openIpv6cp operation on the server.

		Open IPv6CP for selected PPPoX items.

		Args:
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('openIpv6cp', payload=locals(), response_object=None)

	def OpenIpv6cp(self, SessionIndices):
		"""Executes the openIpv6cp operation on the server.

		Open IPv6CP for selected PPPoX items.

		Args:
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('openIpv6cp', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def SendPing(self, DestIp):
		"""Executes the sendPing operation on the server.

		Send Ping IPv4 for selected PPPoX items.

		Args:
			DestIp (str): This parameter requires a destIp of type kString

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing', payload=locals(), response_object=None)

	def SendPing(self, DestIp, SessionIndices):
		"""Executes the sendPing operation on the server.

		Send Ping IPv4 for selected PPPoX items.

		Args:
			DestIp (str): This parameter requires a destIp of type kString
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing', payload=locals(), response_object=None)

	def SendPing(self, SessionIndices, DestIp):
		"""Executes the sendPing operation on the server.

		Send Ping IPv4 for selected PPPoX items.

		Args:
			SessionIndices (str): This parameter requires a destIp of type kString
			DestIp (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing', payload=locals(), response_object=None)

	def SendPing6(self, DestIp):
		"""Executes the sendPing6 operation on the server.

		Send Ping IPv6 for selected PPPoX items.

		Args:
			DestIp (str): This parameter requires a destIp of type kString

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing6', payload=locals(), response_object=None)

	def SendPing6(self, DestIp, SessionIndices):
		"""Executes the sendPing6 operation on the server.

		Send Ping IPv6 for selected PPPoX items.

		Args:
			DestIp (str): This parameter requires a destIp of type kString
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing6', payload=locals(), response_object=None)

	def SendPing6(self, SessionIndices, DestIp):
		"""Executes the sendPing6 operation on the server.

		Send Ping IPv6 for selected PPPoX items.

		Args:
			SessionIndices (str): This parameter requires a destIp of type kString
			DestIp (str): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPing6', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxclient object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
