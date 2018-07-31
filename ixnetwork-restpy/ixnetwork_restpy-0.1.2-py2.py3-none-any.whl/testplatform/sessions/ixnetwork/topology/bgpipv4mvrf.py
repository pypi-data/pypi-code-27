from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpIpv4MVrf(Base):
	"""BGP IPv4 Peer mVRF Configuration
	"""

	_SDM_NAME = 'bgpIpv4MVrf'

	def __init__(self, parent):
		super(BgpIpv4MVrf, self).__init__(parent)

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

	def PnTLVList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PnTLVList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PnTLVList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pntlvlist.PnTLVList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pntlvlist import PnTLVList
		return self._select(PnTLVList(self), locals())

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
	def BFRId(self):
		"""BFR-Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRId')

	@property
	def BFRIpv4Prefix(self):
		"""BFR IPv4 Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRIpv4Prefix')

	@property
	def BFRIpv6Prefix(self):
		"""BFR IPv6 Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRIpv6Prefix')

	@property
	def BFRPrefixType(self):
		"""BFR Prefix Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRPrefixType')

	@property
	def BIERSubDomainId(self):
		"""BIER Sub-Domain Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BIERSubDomainId')

	@property
	def BslMismatchHandlingOption(self):
		"""BIER BSL Mismatch Handling Option

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BslMismatchHandlingOption')

	@property
	def LeafInfoRequiredBit(self):
		"""Leaf Info Required Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('LeafInfoRequiredBit')

	@property
	def LeafInfoRequiredPerFlow(self):
		"""Leaf Info Required Per Flow(LIR-PF)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('LeafInfoRequiredPerFlow')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AutoConstructBitString(self):
		"""Use BitString

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoConstructBitString')

	@property
	def BierBitStringLength(self):
		"""Bit String Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierBitStringLength')

	@property
	def BitString(self):
		"""BitString

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bitString')

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
	def Dscp(self):
		"""DSCP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dscp')

	@property
	def DutIpv4(self):
		"""DUT IP

		Returns:
			list(str)
		"""
		return self._get_attribute('dutIpv4')

	@property
	def Entropy(self):
		"""Entropy

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('entropy')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def ImportRtListSameAsExportRtList(self):
		"""Import RT List Same As Export RT List

		Returns:
			bool
		"""
		return self._get_attribute('importRtListSameAsExportRtList')
	@ImportRtListSameAsExportRtList.setter
	def ImportRtListSameAsExportRtList(self, value):
		self._set_attribute('importRtListSameAsExportRtList', value)

	@property
	def IncludeBierPTAinLeafAD(self):
		"""Include Bier PTA in Leaf A-D

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeBierPTAinLeafAD')

	@property
	def IncludePmsiTunnelAttribute(self):
		"""Include PMSI Tunnel Attribute

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includePmsiTunnelAttribute')

	@property
	def LocalIpv4(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIpv4')

	@property
	def LocalRouterID(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterID')

	@property
	def MulticastDistinguisherAs4Number(self):
		"""VMulticast Distinguisher AS4 Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastDistinguisherAs4Number')

	@property
	def MulticastDistinguisherAsNumber(self):
		"""VMulticast Distinguisher AS Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastDistinguisherAsNumber')

	@property
	def MulticastDistinguisherAssignedNumber(self):
		"""Multicast Distinguisher Assigned Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastDistinguisherAssignedNumber')

	@property
	def MulticastDistinguisherIpAddress(self):
		"""Multicast Distinguisher IP Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastDistinguisherIpAddress')

	@property
	def MulticastDistinguisherType(self):
		"""Multicast Distinguisher Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastDistinguisherType')

	@property
	def MulticastTunnelType(self):
		"""Multicast Tunnel Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastTunnelType')

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
	def NextProtocol(self):
		"""Next Protocol

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nextProtocol')

	@property
	def NumRtInExportRouteTargetList(self):
		"""Number of RTs in Export Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInExportRouteTargetList')
	@NumRtInExportRouteTargetList.setter
	def NumRtInExportRouteTargetList(self, value):
		self._set_attribute('numRtInExportRouteTargetList', value)

	@property
	def NumRtInImportRouteTargetList(self):
		"""Number of RTs in Import Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInImportRouteTargetList')
	@NumRtInImportRouteTargetList.setter
	def NumRtInImportRouteTargetList(self, value):
		self._set_attribute('numRtInImportRouteTargetList', value)

	@property
	def NumRtInUmhExportRouteTargetList(self):
		"""Number of RTs in Export Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInUmhExportRouteTargetList')
	@NumRtInUmhExportRouteTargetList.setter
	def NumRtInUmhExportRouteTargetList(self, value):
		self._set_attribute('numRtInUmhExportRouteTargetList', value)

	@property
	def NumRtInUmhImportRouteTargetList(self):
		"""Number of RTs in Import Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInUmhImportRouteTargetList')
	@NumRtInUmhImportRouteTargetList.setter
	def NumRtInUmhImportRouteTargetList(self, value):
		self._set_attribute('numRtInUmhImportRouteTargetList', value)

	@property
	def Oam(self):
		"""OAM

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('oam')

	@property
	def RootAddress(self):
		"""Root Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddress')

	@property
	def Rsv(self):
		"""Rsv

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rsv')

	@property
	def RsvpP2mpId(self):
		"""RSVP P2MP ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rsvpP2mpId')

	@property
	def RsvpP2mpIdAsNumber(self):
		"""RSVP P2MP ID as Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rsvpP2mpIdAsNumber')

	@property
	def RsvpTunnelId(self):
		"""RSVP Tunnel ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rsvpTunnelId')

	@property
	def SameAsExportRT(self):
		"""Same As Export RT Attribute

		Returns:
			bool
		"""
		return self._get_attribute('sameAsExportRT')
	@SameAsExportRT.setter
	def SameAsExportRT(self, value):
		self._set_attribute('sameAsExportRT', value)

	@property
	def SameAsImportRT(self):
		"""Same As Import RT Attribute

		Returns:
			bool
		"""
		return self._get_attribute('sameAsImportRT')
	@SameAsImportRT.setter
	def SameAsImportRT(self, value):
		self._set_attribute('sameAsImportRT', value)

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SiCount(self):
		"""Set Identifier Range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('siCount')

	@property
	def SrLabelStart(self):
		"""SR Label Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srLabelStart')

	@property
	def SrLabelStep(self):
		"""SR Label Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srLabelStep')

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
	def SupportLeafADRoutesSending(self):
		"""Support Leaf A-D Routes Sending

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportLeafADRoutesSending')

	@property
	def TrafficBfrId(self):
		"""Traffic BFR-Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('trafficBfrId')

	@property
	def UpOrDownStreamAssignedLabel(self):
		"""Upstream/Downstream Assigned Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('upOrDownStreamAssignedLabel')

	@property
	def UseSameBfrIdInTraffic(self):
		"""Use Same BFR-Id in Traffic

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useSameBfrIdInTraffic')

	@property
	def UseUpOrDownStreamAssigneLabel(self):
		"""Use Upstream/Downstream Assigned Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useUpOrDownStreamAssigneLabel')

	@property
	def Version(self):
		"""Version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('version')

	def remove(self):
		"""Deletes a child instance of BgpIpv4MVrf on the server.

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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start BGP VRF

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start BGP VRF

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start BGP VRF

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop BGP VRF

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop BGP VRF

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop BGP VRF

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bgpIpv4MVrf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
