from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Traffic(Base):
	"""The traffic object allows the user to create millions of traffic flows for validating emulated networks and hosts. This is the top-level object for traffic configuration.
	"""

	_SDM_NAME = 'traffic'

	def __init__(self, parent):
		super(Traffic, self).__init__(parent)

	def DynamicFrameSize(self, HighLevelStreamName=None, TrafficItemName=None):
		"""Gets child instances of DynamicFrameSize from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DynamicFrameSize will be returned.

		Args:
			HighLevelStreamName (str): The name of the high level stream
			TrafficItemName (str): The name of the parent traffic item.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.dynamicframesize.dynamicframesize.DynamicFrameSize))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.dynamicframesize.dynamicframesize import DynamicFrameSize
		return self._select(DynamicFrameSize(self), locals())

	def DynamicRate(self, HighLevelStreamName=None, TrafficItemName=None):
		"""Gets child instances of DynamicRate from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DynamicRate will be returned.

		Args:
			HighLevelStreamName (str): The name of the high level stream
			TrafficItemName (str): The name of the parent traffic item.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.dynamicrate.dynamicrate.DynamicRate))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.dynamicrate.dynamicrate import DynamicRate
		return self._select(DynamicRate(self), locals())

	def EgressOnlyTracking(self, SignatureValue=None):
		"""Gets child instances of EgressOnlyTracking from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of EgressOnlyTracking will be returned.

		Args:
			SignatureValue (str): Signature value to be placed inside the packet.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.egressonlytracking.egressonlytracking.EgressOnlyTracking))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.egressonlytracking.egressonlytracking import EgressOnlyTracking
		return self._select(EgressOnlyTracking(self), locals())

	def add_EgressOnlyTracking(self, Egress=None, Enabled=None, Port=None, SignatureOffset=None, SignatureValue=None):
		"""Adds a child instance of EgressOnlyTracking on the server.

		Args:
			Egress (list(dict(arg1:number,arg2:str))): Struct contains: egress offset and egress mask
			Enabled (bool): Enables the egress only tracking for the given port.
			Port (str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)): 
			SignatureOffset (number): Offset where the signature value will be placed in the packet.
			SignatureValue (str): Signature value to be placed inside the packet.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.egressonlytracking.egressonlytracking.EgressOnlyTracking)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.egressonlytracking.egressonlytracking import EgressOnlyTracking
		return self._create(EgressOnlyTracking(self), locals())

	def ProtocolTemplate(self, DisplayName=None, StackTypeId=None, TemplateName=None):
		"""Gets child instances of ProtocolTemplate from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of ProtocolTemplate will be returned.

		Args:
			DisplayName (str): The display name of the template.
			StackTypeId (str): 
			TemplateName (str): Indicates the protocol template name that is added to a packet.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.protocoltemplate.ProtocolTemplate))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.protocoltemplate import ProtocolTemplate
		return self._select(ProtocolTemplate(self), locals())

	@property
	def Statistics(self):
		"""Returns the one and only one Statistics object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.statistics.Statistics)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.statistics import Statistics
		return self._read(Statistics(self), None)

	def TrafficGroup(self, Name=None):
		"""Gets child instances of TrafficGroup from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of TrafficGroup will be returned.

		Args:
			Name (str): Name of the traffic item.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficgroup.trafficgroup.TrafficGroup))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficgroup.trafficgroup import TrafficGroup
		return self._select(TrafficGroup(self), locals())

	def add_TrafficGroup(self, Name=""):
		"""Adds a child instance of TrafficGroup on the server.

		Args:
			Name (str): Name of the traffic item.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficgroup.trafficgroup.TrafficGroup)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficgroup.trafficgroup import TrafficGroup
		return self._create(TrafficGroup(self), locals())

	def TrafficItem(self, Name=None, State=None):
		"""Gets child instances of TrafficItem from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of TrafficItem will be returned.

		Args:
			Name (str): The name of the traffic item.
			State (str): (Read only) A read-only field which indicates the current state of the traffic item.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.trafficitem.TrafficItem))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.trafficitem import TrafficItem
		return self._select(TrafficItem(self), locals())

	def add_TrafficItem(self, AllowSelfDestined="False", BiDirectional="False", EgressEnabled="False", EnableDynamicMplsLabelValues="False", Enabled="True", HasOpenFlow="False", HostsPerNetwork="1", InterAsBgpPreference="one", InterAsLdpPreference="two", MaxNumberOfVpnLabelStack="2", MergeDestinations="True", MulticastForwardingMode=None, Name="Traffic Item", NumVlansForMulticastReplication=None, OrdinalNo="0", OriginatorType="endUser", RoundRobinPacketOrdering=None, RouteMesh="oneToOne", SrcDestMesh="oneToOne", Suspend="False", TrafficItemType="l2L3", TrafficType="raw", TransmitMode="interleaved", TransportLdpPreference="two", TransportRsvpTePreference="one", UseControlPlaneFrameSize=None, UseControlPlaneRate=None):
		"""Adds a child instance of TrafficItem on the server.

		Args:
			AllowSelfDestined (bool): If true, this helps to send traffic from routes on an Ixia port to other routes on the same Ixia port.
			BiDirectional (bool): If true, this enables traffic to be sent in forward and reverse destination.
			EgressEnabled (bool): Enables the egress.
			EnableDynamicMplsLabelValues (bool): Enables the dynamic MPLS label values.
			Enabled (bool): If true, this enables the selected traffic item.
			HasOpenFlow (bool): Indicates whether or not this trafficItem has openflow.
			HostsPerNetwork (number): The number of emulated hosts for the traffic stream.
			InterAsBgpPreference (str(one|two)): Signifies the inter as BGP prefence
			InterAsLdpPreference (str(one|two)): Preferences inter as LDP
			MaxNumberOfVpnLabelStack (number): Signifies the maximum number of VPN label stack
			MergeDestinations (bool): If true, merges the traffic flow in the destination ranges.
			MulticastForwardingMode (str(loadBalancing|replication)): 
			Name (str): The name of the traffic item.
			NumVlansForMulticastReplication (number): Set the number of vlans for multicast replication
			OrdinalNo (number): Signifies the ordinal number
			OriginatorType (str(endUser|quickTest)): Indicates who created this trafficItem.
			RoundRobinPacketOrdering (bool): This option enables Round Robin Packet Ordering within endpoints across Rx ports.
			RouteMesh (str(fullMesh|oneToOne)): The traffic flow type between each pair of source route endpoint and destination route endpoint.
			SrcDestMesh (str(fullMesh|manyToMany|none|oneToOne)): Select the options to set the traffic mesh type between the Source Endpoint and Destination endpoint.
			Suspend (bool): Suspends all traffic on this stream.
			TrafficItemType (str(application|applicationLibrary|l2L3|quick)): Helps to configure and edit a traffic item that is sent across Ixia ports.
			TrafficType (str(atm|avb1722|avbRaw|ethernetVlan|fc|fcoe|frameRelay|hdlc|ipv4|ipv4ApplicationTraffic|ipv6|ipv6ApplicationTraffic|ppp|raw)): Helps to select the type of traffic endpoint to be configured.
			TransmitMode (str(interleaved|sequential)): The transmit mode for this traffic item
			TransportLdpPreference (str(one|two)): Transports LDP preference
			TransportRsvpTePreference (str(one|two)): Transports RSVP TE preference
			UseControlPlaneFrameSize (bool): 
			UseControlPlaneRate (bool): 

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.trafficitem.TrafficItem)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.trafficitem import TrafficItem
		return self._create(TrafficItem(self), locals())

	@property
	def AutoCorrectL4HeaderChecksums(self):
		"""This is used for Multis and Xdensity as checksum is not calculated correctly when change on the fly operations are performed. When this option is enabled IxOS uses 2 bytes before CRC, that way ensuring the checksum is correct when change on the fly operations are performed.

		Returns:
			bool
		"""
		return self._get_attribute('autoCorrectL4HeaderChecksums')
	@AutoCorrectL4HeaderChecksums.setter
	def AutoCorrectL4HeaderChecksums(self, value):
		self._set_attribute('autoCorrectL4HeaderChecksums', value)

	@property
	def CycleOffsetForScheduledStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cycleOffsetForScheduledStart')
	@CycleOffsetForScheduledStart.setter
	def CycleOffsetForScheduledStart(self, value):
		self._set_attribute('cycleOffsetForScheduledStart', value)

	@property
	def CycleOffsetUnitForScheduledStart(self):
		"""

		Returns:
			str(microseconds|milliseconds|nanoseconds|seconds)
		"""
		return self._get_attribute('cycleOffsetUnitForScheduledStart')
	@CycleOffsetUnitForScheduledStart.setter
	def CycleOffsetUnitForScheduledStart(self, value):
		self._set_attribute('cycleOffsetUnitForScheduledStart', value)

	@property
	def CycleTimeForScheduledStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cycleTimeForScheduledStart')
	@CycleTimeForScheduledStart.setter
	def CycleTimeForScheduledStart(self, value):
		self._set_attribute('cycleTimeForScheduledStart', value)

	@property
	def CycleTimeUnitForScheduledStart(self):
		"""

		Returns:
			str(microseconds|milliseconds|nanoseconds|seconds)
		"""
		return self._get_attribute('cycleTimeUnitForScheduledStart')
	@CycleTimeUnitForScheduledStart.setter
	def CycleTimeUnitForScheduledStart(self, value):
		self._set_attribute('cycleTimeUnitForScheduledStart', value)

	@property
	def DataPlaneJitterWindow(self):
		"""Indicates the number of packets received during a time interval. This is used forcalculating the rate on the recieve side.

		Returns:
			str(0|10485760|1310720|167772160|20971520|2621440|335544320|41943040|5242880|671088640|83886080)
		"""
		return self._get_attribute('dataPlaneJitterWindow')
	@DataPlaneJitterWindow.setter
	def DataPlaneJitterWindow(self, value):
		self._set_attribute('dataPlaneJitterWindow', value)

	@property
	def DelayTimeForScheduledStart(self):
		"""Delay Time For Scheduled Start Transmit in seconds

		Returns:
			number
		"""
		return self._get_attribute('delayTimeForScheduledStart')
	@DelayTimeForScheduledStart.setter
	def DelayTimeForScheduledStart(self, value):
		self._set_attribute('delayTimeForScheduledStart', value)

	@property
	def DestMacRetryCount(self):
		"""The number of time to attempt to obtain the destination MAC address.

		Returns:
			number
		"""
		return self._get_attribute('destMacRetryCount')
	@DestMacRetryCount.setter
	def DestMacRetryCount(self, value):
		self._set_attribute('destMacRetryCount', value)

	@property
	def DestMacRetryDelay(self):
		"""The number of seconds to wait between attempts to obtain the destination MAC address.

		Returns:
			number
		"""
		return self._get_attribute('destMacRetryDelay')
	@DestMacRetryDelay.setter
	def DestMacRetryDelay(self, value):
		self._set_attribute('destMacRetryDelay', value)

	@property
	def DetectMisdirectedOnAllPorts(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('detectMisdirectedOnAllPorts')
	@DetectMisdirectedOnAllPorts.setter
	def DetectMisdirectedOnAllPorts(self, value):
		self._set_attribute('detectMisdirectedOnAllPorts', value)

	@property
	def DisplayMplsCurrentLabelValue(self):
		"""Displays current label value for LSP Endpoints.

		Returns:
			bool
		"""
		return self._get_attribute('displayMplsCurrentLabelValue')
	@DisplayMplsCurrentLabelValue.setter
	def DisplayMplsCurrentLabelValue(self, value):
		self._set_attribute('displayMplsCurrentLabelValue', value)

	@property
	def ElapsedTransmitTime(self):
		"""Specifies the amount of time traffic is running in milliseconds. If the traffic state is unapplied or errored then the transmit time will be 0.

		Returns:
			number
		"""
		return self._get_attribute('elapsedTransmitTime')

	@property
	def EnableDataIntegrityCheck(self):
		"""If true, enable data integrity check.

		Returns:
			bool
		"""
		return self._get_attribute('enableDataIntegrityCheck')
	@EnableDataIntegrityCheck.setter
	def EnableDataIntegrityCheck(self, value):
		self._set_attribute('enableDataIntegrityCheck', value)

	@property
	def EnableDestMacRetry(self):
		"""If true, enables the destination MAC address retry function.

		Returns:
			bool
		"""
		return self._get_attribute('enableDestMacRetry')
	@EnableDestMacRetry.setter
	def EnableDestMacRetry(self, value):
		self._set_attribute('enableDestMacRetry', value)

	@property
	def EnableEgressOnlyTracking(self):
		"""This flags enables/disables egress only tracking on the quick flow group. In this mode only quick flow groups are supported, user will have only PGID stats and the packets will not contain any instrumentation block.

		Returns:
			bool
		"""
		return self._get_attribute('enableEgressOnlyTracking')
	@EnableEgressOnlyTracking.setter
	def EnableEgressOnlyTracking(self, value):
		self._set_attribute('enableEgressOnlyTracking', value)

	@property
	def EnableInstantaneousStatsSupport(self):
		"""If true, enables instantaneous stats support

		Returns:
			bool
		"""
		return self._get_attribute('enableInstantaneousStatsSupport')
	@EnableInstantaneousStatsSupport.setter
	def EnableInstantaneousStatsSupport(self, value):
		self._set_attribute('enableInstantaneousStatsSupport', value)

	@property
	def EnableLagFlowBalancing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLagFlowBalancing')
	@EnableLagFlowBalancing.setter
	def EnableLagFlowBalancing(self, value):
		self._set_attribute('enableLagFlowBalancing', value)

	@property
	def EnableMinFrameSize(self):
		"""If true, IxNetwork will allow the stream to use smaller packet sizes. (In the case of IPv4 and Ethernet, 64 bytes will be allowed.) This is achieved by reducing the size of the instrumentation tag, which will be identified by receiving ports.

		Returns:
			bool
		"""
		return self._get_attribute('enableMinFrameSize')
	@EnableMinFrameSize.setter
	def EnableMinFrameSize(self, value):
		self._set_attribute('enableMinFrameSize', value)

	@property
	def EnableMulticastScalingFactor(self):
		"""If true, traffic items with the Merged Destination Ranges option selected have be to manually regenerated by the user.

		Returns:
			bool
		"""
		return self._get_attribute('enableMulticastScalingFactor')
	@EnableMulticastScalingFactor.setter
	def EnableMulticastScalingFactor(self, value):
		self._set_attribute('enableMulticastScalingFactor', value)

	@property
	def EnableSequenceChecking(self):
		"""If true, this field enables sequence checking. The default is false.

		Returns:
			bool
		"""
		return self._get_attribute('enableSequenceChecking')
	@EnableSequenceChecking.setter
	def EnableSequenceChecking(self, value):
		self._set_attribute('enableSequenceChecking', value)

	@property
	def EnableStaggeredStartDelay(self):
		"""If checked, enables the staggered start delay function.

		Returns:
			bool
		"""
		return self._get_attribute('enableStaggeredStartDelay')
	@EnableStaggeredStartDelay.setter
	def EnableStaggeredStartDelay(self, value):
		self._set_attribute('enableStaggeredStartDelay', value)

	@property
	def EnableStaggeredTransmit(self):
		"""If true, the start of transmit is staggered across ports. A 25-30 ms delay is introduced between the time one port begins transmitting and the time next port begins transmitting.

		Returns:
			bool
		"""
		return self._get_attribute('enableStaggeredTransmit')
	@EnableStaggeredTransmit.setter
	def EnableStaggeredTransmit(self, value):
		self._set_attribute('enableStaggeredTransmit', value)

	@property
	def EnableStreamOrdering(self):
		"""If true, IxNetwork will allow stream ordering per RFC 2889.

		Returns:
			bool
		"""
		return self._get_attribute('enableStreamOrdering')
	@EnableStreamOrdering.setter
	def EnableStreamOrdering(self, value):
		self._set_attribute('enableStreamOrdering', value)

	@property
	def FrameOrderingMode(self):
		"""If true, enables frame ordering.

		Returns:
			str(flowGroupSetup|none|peakLoading|RFC2889)
		"""
		return self._get_attribute('frameOrderingMode')
	@FrameOrderingMode.setter
	def FrameOrderingMode(self, value):
		self._set_attribute('frameOrderingMode', value)

	@property
	def GlobalStreamControl(self):
		"""The Global Stream Control parameters.

		Returns:
			str(continuous|iterations)
		"""
		return self._get_attribute('globalStreamControl')
	@GlobalStreamControl.setter
	def GlobalStreamControl(self, value):
		self._set_attribute('globalStreamControl', value)

	@property
	def GlobalStreamControlIterations(self):
		"""If true, the user can specify how many times each packet stream will be transmitted.

		Returns:
			number
		"""
		return self._get_attribute('globalStreamControlIterations')
	@GlobalStreamControlIterations.setter
	def GlobalStreamControlIterations(self, value):
		self._set_attribute('globalStreamControlIterations', value)

	@property
	def IsApplicationTrafficRunning(self):
		"""If true, application traffic is running.

		Returns:
			bool
		"""
		return self._get_attribute('isApplicationTrafficRunning')

	@property
	def IsApplyOnTheFlyRequired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isApplyOnTheFlyRequired')

	@property
	def IsTrafficRunning(self):
		"""If true, non-application traffic is running.

		Returns:
			bool
		"""
		return self._get_attribute('isTrafficRunning')

	@property
	def LargeErrorThreshhold(self):
		"""The user-configurable threshold value used to determine error levels for out-of-sequence, received packets.

		Returns:
			number
		"""
		return self._get_attribute('largeErrorThreshhold')
	@LargeErrorThreshhold.setter
	def LargeErrorThreshhold(self, value):
		self._set_attribute('largeErrorThreshhold', value)

	@property
	def LearningFrameSize(self):
		"""Learns frame size

		Returns:
			number
		"""
		return self._get_attribute('learningFrameSize')
	@LearningFrameSize.setter
	def LearningFrameSize(self, value):
		self._set_attribute('learningFrameSize', value)

	@property
	def LearningFramesCount(self):
		"""Learns frames count

		Returns:
			number
		"""
		return self._get_attribute('learningFramesCount')
	@LearningFramesCount.setter
	def LearningFramesCount(self, value):
		self._set_attribute('learningFramesCount', value)

	@property
	def LearningFramesRate(self):
		"""Learns frames rate

		Returns:
			number
		"""
		return self._get_attribute('learningFramesRate')
	@LearningFramesRate.setter
	def LearningFramesRate(self, value):
		self._set_attribute('learningFramesRate', value)

	@property
	def MacChangeOnFly(self):
		"""If true, enables IxNetwork's gratuitous ARP capability. When enabled, IxNetwork listens for gratuitous ARP messages from its neighbors.

		Returns:
			bool
		"""
		return self._get_attribute('macChangeOnFly')
	@MacChangeOnFly.setter
	def MacChangeOnFly(self, value):
		self._set_attribute('macChangeOnFly', value)

	@property
	def MaxTrafficGenerationQueries(self):
		"""The maximum number of traffic generation queries. The default is 500.

		Returns:
			number
		"""
		return self._get_attribute('maxTrafficGenerationQueries')
	@MaxTrafficGenerationQueries.setter
	def MaxTrafficGenerationQueries(self, value):
		self._set_attribute('maxTrafficGenerationQueries', value)

	@property
	def MplsLabelLearningTimeout(self):
		"""The MPLS label learning timeout in seconds. The default is 30 seconds.

		Returns:
			number
		"""
		return self._get_attribute('mplsLabelLearningTimeout')
	@MplsLabelLearningTimeout.setter
	def MplsLabelLearningTimeout(self, value):
		self._set_attribute('mplsLabelLearningTimeout', value)

	@property
	def PeakLoadingReplicationCount(self):
		"""The peak loading replication count

		Returns:
			number
		"""
		return self._get_attribute('peakLoadingReplicationCount')
	@PeakLoadingReplicationCount.setter
	def PeakLoadingReplicationCount(self, value):
		self._set_attribute('peakLoadingReplicationCount', value)

	@property
	def PreventDataPlaneToCpu(self):
		"""Prevent all data plane packets from being forwarded to Port CPU (disabling this option requires Port CPU reboot)

		Returns:
			bool
		"""
		return self._get_attribute('preventDataPlaneToCpu')
	@PreventDataPlaneToCpu.setter
	def PreventDataPlaneToCpu(self, value):
		self._set_attribute('preventDataPlaneToCpu', value)

	@property
	def RefreshLearnedInfoBeforeApply(self):
		"""This field refreshes the learned information from the DUT.

		Returns:
			bool
		"""
		return self._get_attribute('refreshLearnedInfoBeforeApply')
	@RefreshLearnedInfoBeforeApply.setter
	def RefreshLearnedInfoBeforeApply(self, value):
		self._set_attribute('refreshLearnedInfoBeforeApply', value)

	@property
	def State(self):
		"""Denotes the current state of traffic.

		Returns:
			str(error|locked|started|startedWaitingForStats|startedWaitingForStreams|stopped|stoppedWaitingForStats|txStopWatchExpected|unapplied)
		"""
		return self._get_attribute('state')

	@property
	def UseRfc5952(self):
		"""Use RFC 5952 for formatting IPv6 addresses (:ffff:1.2.3.4)

		Returns:
			bool
		"""
		return self._get_attribute('useRfc5952')
	@UseRfc5952.setter
	def UseRfc5952(self, value):
		self._set_attribute('useRfc5952', value)

	@property
	def UseScheduledStartTransmit(self):
		"""Use Scheduled Start Transmit

		Returns:
			bool
		"""
		return self._get_attribute('useScheduledStartTransmit')
	@UseScheduledStartTransmit.setter
	def UseScheduledStartTransmit(self, value):
		self._set_attribute('useScheduledStartTransmit', value)

	@property
	def UseTxRxSync(self):
		"""If true, enables the transmit/receive port synchronization algorithm.

		Returns:
			bool
		"""
		return self._get_attribute('useTxRxSync')
	@UseTxRxSync.setter
	def UseTxRxSync(self, value):
		self._set_attribute('useTxRxSync', value)

	@property
	def WaitTime(self):
		"""The time (in seconds) to wait after Stop Transmit before stopping Latency Measurement.

		Returns:
			number
		"""
		return self._get_attribute('waitTime')
	@WaitTime.setter
	def WaitTime(self, value):
		self._set_attribute('waitTime', value)

	def Apply(self):
		"""Executes the apply operation on the server.

		Apply the traffic configuration.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('apply', payload=locals(), response_object=None)

	def ApplyApplicationTraffic(self):
		"""Executes the applyApplicationTraffic operation on the server.

		Apply the stateful traffic configuration.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('applyApplicationTraffic', payload=locals(), response_object=None)

	def ApplyOnTheFlyTrafficChanges(self):
		"""Executes the applyOnTheFlyTrafficChanges operation on the server.

		Apply on the fly traffic changes.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('applyOnTheFlyTrafficChanges', payload=locals(), response_object=None)

	def ApplyStatefulTraffic(self):
		"""Executes the applyStatefulTraffic operation on the server.

		Apply the traffic configuration for stateful traffic items only.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('applyStatefulTraffic', payload=locals(), response_object=None)

	def GenerateIfRequired(self):
		"""Executes the generateIfRequired operation on the server.

		causes regeneration of dirty traffic items

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('generateIfRequired', payload=locals(), response_object=None)

	def GetFrameCountForDuration(self, Arg2):
		"""Executes the getFrameCountForDuration operation on the server.

		Get the frame count for a specific duration.

		Args:
			Arg2 (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream],arg2:number))): An array of structures. Each structure is one valid highLevelStream object reference and the duration to get the frame count for.

		Returns:
			list(number): An array of frame counts.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getFrameCountForDuration', payload=locals(), response_object=None)

	def MakeStatelessTrafficUnapplied(self):
		"""Executes the makeStatelessTrafficUnapplied operation on the server.

		Move stateless traffic to unapplied state.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('makeStatelessTrafficUnapplied', payload=locals(), response_object=None)

	def SendL2L3Learning(self):
		"""Executes the sendL2L3Learning operation on the server.

		Send L2 and L3 learning frames.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendL2L3Learning', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start the traffic configuration.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('start', payload=locals(), response_object=None)

	def StartApplicationTraffic(self):
		"""Executes the startApplicationTraffic operation on the server.

		Start the stateful traffic configuration.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('startApplicationTraffic', payload=locals(), response_object=None)

	def StartStatefulTraffic(self):
		"""Executes the startStatefulTraffic operation on the server.

		Start stateful traffic items only.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('startStatefulTraffic', payload=locals(), response_object=None)

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

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop the traffic configuration.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stop', payload=locals(), response_object=None)

	def StopApplicationTraffic(self):
		"""Executes the stopApplicationTraffic operation on the server.

		Stop the stateful traffic configuration.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopApplicationTraffic', payload=locals(), response_object=None)

	def StopStatefulTraffic(self):
		"""Executes the stopStatefulTraffic operation on the server.

		Stop stateful traffic items only.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopStatefulTraffic', payload=locals(), response_object=None)

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
