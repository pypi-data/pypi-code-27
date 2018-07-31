from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrafficItem(Base):
	"""This object specifies the particular traffic item related properties.
	"""

	_SDM_NAME = 'trafficItem'

	def __init__(self, parent):
		super(TrafficItem, self).__init__(parent)

	def AppLibProfile(self):
		"""Gets child instances of AppLibProfile from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AppLibProfile will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibprofile.AppLibProfile))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibprofile import AppLibProfile
		return self._select(AppLibProfile(self), locals())

	def add_AppLibProfile(self, ConfiguredFlows=None, EnablePerIPStats=None, ObjectiveDistribution=None, ObjectiveType="simulatedUsers", ObjectiveValue="100"):
		"""Adds a child instance of AppLibProfile on the server.

		Args:
			ConfiguredFlows (list(str[])): Configured application library flows within profile.
			EnablePerIPStats (bool): Enable Per IP Stats. When true then Per IP statistic drilldown is available.
			ObjectiveDistribution (str(applyFullObjectiveToEachPort|splitObjectiveEvenlyAmongPorts)): Objective distribution value.
			ObjectiveType (str(simulatedUsers|throughputGbps|throughputKbps|throughputMbps)): The objective type of the test.A Test Objective is the way the user sets the actual rate of the Application Library Traffic transmission.
			ObjectiveValue (number): The absolute value of either simulated users or throughput in its measure unit.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibprofile.AppLibProfile)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibprofile import AppLibProfile
		return self._create(AppLibProfile(self), locals())

	def ConfigElement(self, EncapsulationName=None):
		"""Gets child instances of ConfigElement from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of ConfigElement will be returned.

		Args:
			EncapsulationName (str): Indicates the name of the encapsulation set.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.configelement.ConfigElement))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.configelement import ConfigElement
		return self._select(ConfigElement(self), locals())

	def DynamicUpdate(self):
		"""Gets child instances of DynamicUpdate from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DynamicUpdate will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.dynamicupdate.dynamicupdate.DynamicUpdate))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.dynamicupdate.dynamicupdate import DynamicUpdate
		return self._select(DynamicUpdate(self), locals())

	def EgressTracking(self, Encapsulation=None, Offset=None):
		"""Gets child instances of EgressTracking from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of EgressTracking will be returned.

		Args:
			Encapsulation (str): Specifies the Encapsulation for Egress Tracking.
			Offset (str): Specifies the Offset for Egress Tracking.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.egresstracking.EgressTracking))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.egresstracking import EgressTracking
		return self._select(EgressTracking(self), locals())

	def add_EgressTracking(self, CustomOffsetBits="0", CustomWidthBits="0", Encapsulation="Ethernet", Offset="Outer VLAN Priority (3 bits)"):
		"""Adds a child instance of EgressTracking on the server.

		Args:
			CustomOffsetBits (number): Specifies the Custom Offset in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .
			CustomWidthBits (number): Specifies the Custom Width in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .
			Encapsulation (str): Specifies the Encapsulation for Egress Tracking.
			Offset (str): Specifies the Offset for Egress Tracking.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.egresstracking.EgressTracking)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.egresstracking import EgressTracking
		return self._create(EgressTracking(self), locals())

	def EndpointSet(self, DestinationFilter=None, Name=None, SourceFilter=None):
		"""Gets child instances of EndpointSet from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of EndpointSet will be returned.

		Args:
			DestinationFilter (str): The list of conditions used for filtering destinations endpoints.
			Name (str): The name of the endpoint set.
			SourceFilter (str): The list of conditions used for filtering source endpoints.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.endpointset.endpointset.EndpointSet))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.endpointset.endpointset import EndpointSet
		return self._select(EndpointSet(self), locals())

	def add_EndpointSet(self, AllowEmptyTopologySets="False", DestinationFilter="", Destinations=None, MulticastDestinations=None, MulticastReceivers=None, Name="", NgpfFilters=None, ScalableDestinations=None, ScalableSources=None, SourceFilter="", Sources=None, TrafficGroups=None):
		"""Adds a child instance of EndpointSet on the server.

		Args:
			AllowEmptyTopologySets (bool): Enable this to allow the setting of sources and destinations without throwing an error even if the combination produces an empty topology set.
			DestinationFilter (str): The list of conditions used for filtering destinations endpoints.
			Destinations (list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])): Indicates the number of destination endpoints configured.
			MulticastDestinations (list(dict(arg1:bool,arg2:str[igmp|mld|none],arg3:str,arg4:str,arg5:number))): A compact representation of many virtual multicast destinations. Each list item consists of 5 values where the first two, a bool value and enum value, can be defaulted to false and none. The next two values are a starting address and step address which can be either an ipv4, ipv6 or streamId and the last value is a count of addresses.
			MulticastReceivers (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number))): A list of virtual multicast receivers. Each list item consists of a multicast receiver object reference, port index, host index and group or join/prune index depending on the type of object reference.
			Name (str): The name of the endpoint set.
			NgpfFilters (list(dict(arg1:str,arg2:list[number]))): The list of next generation structures used to filter endpoints. The structure consists of a string tag and list of integer indexes.
			ScalableDestinations (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))): A list of scalable destination structures
			ScalableSources (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*],arg2:number,arg3:number,arg4:number,arg5:number))): A list of scalable source structures.
			SourceFilter (str): The list of conditions used for filtering source endpoints.
			Sources (list(str[None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])): Indicates the number of source endpoints configured.
			TrafficGroups (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=*])): Indicates the traffic groups selected in the source/destination endpoint set.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.endpointset.endpointset.EndpointSet)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.endpointset.endpointset import EndpointSet
		return self._create(EndpointSet(self), locals())

	def HighLevelStream(self, AppliedFrameSize=None, EncapsulationName=None, Name=None, State=None, TxPortName=None):
		"""Gets child instances of HighLevelStream from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of HighLevelStream will be returned.

		Args:
			AppliedFrameSize (str): (Read only) Indicates the applied frame size of the high level stream.
			EncapsulationName (str): Name of the configured encapsulation type.
			Name (str): An alphanumeric string that returns the name of the field.
			State (str): (Read only) Denotes the current state of the stream.
			TxPortName (str): The name of the virtual port that is the transmitting port.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.highlevelstream.HighLevelStream))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.highlevelstream import HighLevelStream
		return self._select(HighLevelStream(self), locals())

	def Tracking(self, ProtocolOffset=None):
		"""Gets child instances of Tracking from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Tracking will be returned.

		Args:
			ProtocolOffset (str): Specifies the Protocol Offset when flows of a Traffic Item are tracked by Custom Override.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.tracking.Tracking))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.tracking import Tracking
		return self._select(Tracking(self), locals())

	def TransmissionDistribution(self):
		"""Gets child instances of TransmissionDistribution from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of TransmissionDistribution will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.transmissiondistribution.transmissiondistribution.TransmissionDistribution))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.transmissiondistribution.transmissiondistribution import TransmissionDistribution
		return self._select(TransmissionDistribution(self), locals())

	@property
	def AllowSelfDestined(self):
		"""If true, this helps to send traffic from routes on an Ixia port to other routes on the same Ixia port.

		Returns:
			bool
		"""
		return self._get_attribute('allowSelfDestined')
	@AllowSelfDestined.setter
	def AllowSelfDestined(self, value):
		self._set_attribute('allowSelfDestined', value)

	@property
	def BiDirectional(self):
		"""If true, this enables traffic to be sent in forward and reverse destination.

		Returns:
			bool
		"""
		return self._get_attribute('biDirectional')
	@BiDirectional.setter
	def BiDirectional(self, value):
		self._set_attribute('biDirectional', value)

	@property
	def EgressEnabled(self):
		"""Enables the egress.

		Returns:
			bool
		"""
		return self._get_attribute('egressEnabled')
	@EgressEnabled.setter
	def EgressEnabled(self, value):
		self._set_attribute('egressEnabled', value)

	@property
	def EnableDynamicMplsLabelValues(self):
		"""Enables the dynamic MPLS label values.

		Returns:
			bool
		"""
		return self._get_attribute('enableDynamicMplsLabelValues')
	@EnableDynamicMplsLabelValues.setter
	def EnableDynamicMplsLabelValues(self, value):
		self._set_attribute('enableDynamicMplsLabelValues', value)

	@property
	def Enabled(self):
		"""If true, this enables the selected traffic item.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Errors(self):
		"""Displays the errors.

		Returns:
			list(str)
		"""
		return self._get_attribute('errors')

	@property
	def FlowGroupCount(self):
		"""Indicates the number of flow groups.

		Returns:
			number
		"""
		return self._get_attribute('flowGroupCount')

	@property
	def HasOpenFlow(self):
		"""Indicates whether or not this trafficItem has openflow.

		Returns:
			bool
		"""
		return self._get_attribute('hasOpenFlow')
	@HasOpenFlow.setter
	def HasOpenFlow(self, value):
		self._set_attribute('hasOpenFlow', value)

	@property
	def HostsPerNetwork(self):
		"""The number of emulated hosts for the traffic stream.

		Returns:
			number
		"""
		return self._get_attribute('hostsPerNetwork')
	@HostsPerNetwork.setter
	def HostsPerNetwork(self, value):
		self._set_attribute('hostsPerNetwork', value)

	@property
	def InterAsBgpPreference(self):
		"""Signifies the inter as BGP prefence

		Returns:
			str(one|two)
		"""
		return self._get_attribute('interAsBgpPreference')
	@InterAsBgpPreference.setter
	def InterAsBgpPreference(self, value):
		self._set_attribute('interAsBgpPreference', value)

	@property
	def InterAsLdpPreference(self):
		"""Preferences inter as LDP

		Returns:
			str(one|two)
		"""
		return self._get_attribute('interAsLdpPreference')
	@InterAsLdpPreference.setter
	def InterAsLdpPreference(self, value):
		self._set_attribute('interAsLdpPreference', value)

	@property
	def MaxNumberOfVpnLabelStack(self):
		"""Signifies the maximum number of VPN label stack

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfVpnLabelStack')
	@MaxNumberOfVpnLabelStack.setter
	def MaxNumberOfVpnLabelStack(self, value):
		self._set_attribute('maxNumberOfVpnLabelStack', value)

	@property
	def MergeDestinations(self):
		"""If true, merges the traffic flow in the destination ranges.

		Returns:
			bool
		"""
		return self._get_attribute('mergeDestinations')
	@MergeDestinations.setter
	def MergeDestinations(self, value):
		self._set_attribute('mergeDestinations', value)

	@property
	def MulticastForwardingMode(self):
		"""

		Returns:
			str(loadBalancing|replication)
		"""
		return self._get_attribute('multicastForwardingMode')
	@MulticastForwardingMode.setter
	def MulticastForwardingMode(self, value):
		self._set_attribute('multicastForwardingMode', value)

	@property
	def Name(self):
		"""The name of the traffic item.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NumVlansForMulticastReplication(self):
		"""Set the number of vlans for multicast replication

		Returns:
			number
		"""
		return self._get_attribute('numVlansForMulticastReplication')
	@NumVlansForMulticastReplication.setter
	def NumVlansForMulticastReplication(self, value):
		self._set_attribute('numVlansForMulticastReplication', value)

	@property
	def OrdinalNo(self):
		"""Signifies the ordinal number

		Returns:
			number
		"""
		return self._get_attribute('ordinalNo')
	@OrdinalNo.setter
	def OrdinalNo(self, value):
		self._set_attribute('ordinalNo', value)

	@property
	def OriginatorType(self):
		"""Indicates who created this trafficItem.

		Returns:
			str(endUser|quickTest)
		"""
		return self._get_attribute('originatorType')
	@OriginatorType.setter
	def OriginatorType(self, value):
		self._set_attribute('originatorType', value)

	@property
	def RoundRobinPacketOrdering(self):
		"""This option enables Round Robin Packet Ordering within endpoints across Rx ports.

		Returns:
			bool
		"""
		return self._get_attribute('roundRobinPacketOrdering')
	@RoundRobinPacketOrdering.setter
	def RoundRobinPacketOrdering(self, value):
		self._set_attribute('roundRobinPacketOrdering', value)

	@property
	def RouteMesh(self):
		"""The traffic flow type between each pair of source route endpoint and destination route endpoint.

		Returns:
			str(fullMesh|oneToOne)
		"""
		return self._get_attribute('routeMesh')
	@RouteMesh.setter
	def RouteMesh(self, value):
		self._set_attribute('routeMesh', value)

	@property
	def SrcDestMesh(self):
		"""Select the options to set the traffic mesh type between the Source Endpoint and Destination endpoint.

		Returns:
			str(fullMesh|manyToMany|none|oneToOne)
		"""
		return self._get_attribute('srcDestMesh')
	@SrcDestMesh.setter
	def SrcDestMesh(self, value):
		self._set_attribute('srcDestMesh', value)

	@property
	def State(self):
		"""(Read only) A read-only field which indicates the current state of the traffic item.

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def Suspend(self):
		"""Suspends all traffic on this stream.

		Returns:
			bool
		"""
		return self._get_attribute('suspend')
	@Suspend.setter
	def Suspend(self, value):
		self._set_attribute('suspend', value)

	@property
	def TrafficItemType(self):
		"""Helps to configure and edit a traffic item that is sent across Ixia ports.

		Returns:
			str(application|applicationLibrary|l2L3|quick)
		"""
		return self._get_attribute('trafficItemType')
	@TrafficItemType.setter
	def TrafficItemType(self, value):
		self._set_attribute('trafficItemType', value)

	@property
	def TrafficType(self):
		"""Helps to select the type of traffic endpoint to be configured.

		Returns:
			str(atm|avb1722|avbRaw|ethernetVlan|fc|fcoe|frameRelay|hdlc|ipv4|ipv4ApplicationTraffic|ipv6|ipv6ApplicationTraffic|ppp|raw)
		"""
		return self._get_attribute('trafficType')
	@TrafficType.setter
	def TrafficType(self, value):
		self._set_attribute('trafficType', value)

	@property
	def TransmitMode(self):
		"""The transmit mode for this traffic item

		Returns:
			str(interleaved|sequential)
		"""
		return self._get_attribute('transmitMode')
	@TransmitMode.setter
	def TransmitMode(self, value):
		self._set_attribute('transmitMode', value)

	@property
	def TransportLdpPreference(self):
		"""Transports LDP preference

		Returns:
			str(one|two)
		"""
		return self._get_attribute('transportLdpPreference')
	@TransportLdpPreference.setter
	def TransportLdpPreference(self, value):
		self._set_attribute('transportLdpPreference', value)

	@property
	def TransportRsvpTePreference(self):
		"""Transports RSVP TE preference

		Returns:
			str(one|two)
		"""
		return self._get_attribute('transportRsvpTePreference')
	@TransportRsvpTePreference.setter
	def TransportRsvpTePreference(self, value):
		self._set_attribute('transportRsvpTePreference', value)

	@property
	def UseControlPlaneFrameSize(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useControlPlaneFrameSize')
	@UseControlPlaneFrameSize.setter
	def UseControlPlaneFrameSize(self, value):
		self._set_attribute('useControlPlaneFrameSize', value)

	@property
	def UseControlPlaneRate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useControlPlaneRate')
	@UseControlPlaneRate.setter
	def UseControlPlaneRate(self, value):
		self._set_attribute('useControlPlaneRate', value)

	@property
	def Warnings(self):
		"""Displays the warnings.

		Returns:
			list(str)
		"""
		return self._get_attribute('warnings')

	def remove(self):
		"""Deletes a child instance of TrafficItem on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ConvertToRaw(self):
		"""Executes the convertToRaw operation on the server.

		Converts a non-raw traffic item to a raw traffic item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('convertToRaw', payload=locals(), response_object=None)

	def Duplicate(self, Arg2):
		"""Executes the duplicate operation on the server.

		Duplicates a specific traffic item.

		Args:
			Arg2 (number): The number of times to duplicate the traffic item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('duplicate', payload=locals(), response_object=None)

	def DuplicateItems(self, Arg1):
		"""Executes the duplicateItems operation on the server.

		Duplicates a list of traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('duplicateItems', payload=locals(), response_object=None)

	def Generate(self, Arg1):
		"""Executes the generate operation on the server.

		Generate traffic for specific traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('generate', payload=locals(), response_object=None)

	def Generate(self):
		"""Executes the generate operation on the server.

		Generate traffic for a specific traffic item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('generate', payload=locals(), response_object=None)

	def ResolveAptixiaEndpoints(self, Arg1):
		"""Executes the resolveAptixiaEndpoints operation on the server.

		Resolves /vport/protocolStack/. endpoints being used by a specific traffic item.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): An array of valid object references.

		Returns:
			str: This exec returns a string containing the resolved endpoints.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resolveAptixiaEndpoints', payload=locals(), response_object=None)

	def StartDefaultLearning(self, Arg1):
		"""Executes the startDefaultLearning operation on the server.

		Starts default learning for a list of traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startDefaultLearning', payload=locals(), response_object=None)

	def StartDefaultLearning(self):
		"""Executes the startDefaultLearning operation on the server.

		Starts default learning for a specific traffic item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('startDefaultLearning', payload=locals(), response_object=None)

	def StartLearning(self, Arg1, Arg2, Arg3, Arg4):
		"""Executes the startLearning operation on the server.

		Sends learning frames.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): An array of valid object references.
			Arg2 (number): The framesize of the learning frame.
			Arg3 (number): The framecount of the learning frames.
			Arg4 (number): The frames per second of the learning frames.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startLearning', payload=locals(), response_object=None)

	def StartLearning(self, Arg1, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7):
		"""Executes the startLearning operation on the server.

		Sends learning frames.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): An array of valid object references.
			Arg2 (number): The framesize of the learning frame.
			Arg3 (number): The framecount of the learning frames.
			Arg4 (number): The frames per second of the learning frames.
			Arg5 (bool): Send gratuitous ARP frames.
			Arg6 (bool): Send MAC frames.
			Arg7 (bool): Send Fast Path frames.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startLearning', payload=locals(), response_object=None)

	def StartLearning(self, Arg1, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7, Arg8):
		"""Executes the startLearning operation on the server.

		Sends learning frames.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): An array of valid object references.
			Arg2 (number): The framesize of the learning frame.
			Arg3 (number): The framecount of the learning frames.
			Arg4 (number): The frames per second of the learning frames.
			Arg5 (bool): Send gratuitous ARP frames.
			Arg6 (bool): Send MAC frames.
			Arg7 (bool): Send Fast Path frames.
			Arg8 (bool): Send full mesh.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startLearning', payload=locals(), response_object=None)

	def StartStatelessTraffic(self, Arg1):
		"""Executes the startStatelessTraffic operation on the server.

		Start the traffic configuration for stateless traffic items only.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startStatelessTraffic', payload=locals(), response_object=None)

	def StartStatelessTrafficBlocking(self, Arg1):
		"""Executes the startStatelessTrafficBlocking operation on the server.

		Start the traffic configuration for stateless traffic items only. This will block until traffic is fully started.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startStatelessTrafficBlocking', payload=locals(), response_object=None)

	def StopStatelessTraffic(self, Arg1):
		"""Executes the stopStatelessTraffic operation on the server.

		Stop the stateless traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopStatelessTraffic', payload=locals(), response_object=None)

	def StopStatelessTrafficBlocking(self, Arg1):
		"""Executes the stopStatelessTrafficBlocking operation on the server.

		Stop the traffic configuration for stateless traffic items only. This will block until traffic is fully stopped.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopStatelessTrafficBlocking', payload=locals(), response_object=None)
