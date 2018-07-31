from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpenFlowController(Base):
	"""OpenFlow Session (Device) level Configuration
	"""

	_SDM_NAME = 'openFlowController'

	def __init__(self, parent):
		super(OpenFlowController, self).__init__(parent)

	def LearnedInfo(self, State=None, Type=None):
		"""Gets child instances of LearnedInfo from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LearnedInfo will be returned.

		Args:
			State (str): The state of the learned information query
			Type (str): The type of learned information

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo.LearnedInfo))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo import LearnedInfo
		return self._select(LearnedInfo(self), locals())

	def LearnedInfoUpdate(self):
		"""Gets child instances of LearnedInfoUpdate from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LearnedInfoUpdate will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfoupdate.LearnedInfoUpdate))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfoupdate import LearnedInfoUpdate
		return self._select(LearnedInfoUpdate(self), locals())

	def OpenFlowChannel(self, ControllerName=None, DescriptiveName=None, Name=None):
		"""Gets child instances of OpenFlowChannel from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OpenFlowChannel will be returned.

		Args:
			ControllerName (str): Parent Controller Name
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.openflowchannel.OpenFlowChannel))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.openflowchannel import OpenFlowChannel
		return self._select(OpenFlowChannel(self), locals())

	def add_OpenFlowChannel(self, ConnectedVia=None, GroupsPerChannel="0", MetersPerChannel="0", Multiplier="1", Name=None, StackedLayers=None, TablesPerChannel="1"):
		"""Adds a child instance of OpenFlowChannel on the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			GroupsPerChannel (number): Number of Groups per Channel
			MetersPerChannel (number): Number of Meters per Channel
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			TablesPerChannel (number): Number of Tables per Channel

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.openflowchannel.OpenFlowChannel)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.openflowchannel import OpenFlowChannel
		return self._create(OpenFlowChannel(self), locals())

	@property
	def AcceptUnconfiguredChannel(self):
		"""If selected, un-configured channels are accepted for this interface.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acceptUnconfiguredChannel')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AuxConnTimeout(self):
		"""The inactive time in milliseconds after which the auxiliary connection will timeout and close.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxConnTimeout')

	@property
	def AuxNonHelloStartupOption(self):
		"""Specify the action from the following options for non-hello message when connection is established. The options are: 1) Accept Connection 2) Return Error

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxNonHelloStartupOption')

	@property
	def BadVersionErrorAction(self):
		"""Specify the action to be performed when an invalid version error occurs. The options are: 1) Re-send Hello 2) Terminate Connection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('badVersionErrorAction')

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
	def ControllerLocalIp(self):
		"""The local IP address of the interface. This field is auto-populated and cannot be changed.

		Returns:
			list(str)
		"""
		return self._get_attribute('controllerLocalIp')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DelFlowsAtStartup(self):
		"""If selected, Controller sends an OpenFlow delete message (for all wild card entries) at start-up. This deletes all existing flows in the DUT.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delFlowsAtStartup')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DirectoryName(self):
		"""Location of Directory in Client where the Certificate and Key Files are available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('directoryName')

	@property
	def EchoInterval(self):
		"""The periodic interval in seconds at which the Interface sends Echo Request Packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoInterval')

	@property
	def EchoTimeOut(self):
		"""If selected, the echo request times out when they have been sent for a specified number of times, or when the time value specified has lapsed, but no response is received

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoTimeOut')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def FeatRequestTimeout(self):
		"""The inactive time in milliseconds after which the feature request will timeout.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('featRequestTimeout')

	@property
	def FeatureRquestTimeoutAction(self):
		"""Specify the action to be performed when a feature request times out. The options are: 1) Re-send Feature Request 2) Terminate Connection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('featureRquestTimeoutAction')

	@property
	def FileCaCertificate(self):
		"""Browse and upload a CA Certificate file for TLS session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCaCertificate')

	@property
	def FileCertificate(self):
		"""Browse and upload the certificate file for TLS session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCertificate')

	@property
	def FilePrivKey(self):
		"""Browse and upload the private key file for TLS session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filePrivKey')

	@property
	def InstallFlowForLLDP(self):
		"""If selected, the controller sends add flow to each connected switch in such a way that each switch forwards LLDP packet to all other connected switches.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('installFlowForLLDP')

	@property
	def InstallLLDPFlow(self):
		"""If selected, LLDP Flow is installed.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('installLLDPFlow')

	@property
	def LLDPDestinactionMac(self):
		"""Specify the LLDP Destination MAC address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lLDPDestinactionMac')

	@property
	def LldpDstMacAddress(self):
		"""The destination MAC Address for the LLDP packet.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lldpDstMacAddress')

	@property
	def ModeOfConnection(self):
		"""The mode of connection used for the Interface. Options include: 1) Active 2) Passive 3) Mixed

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('modeOfConnection')

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
	def NumberOfChannels(self):
		"""Total number of OpenFlow channels to be added for this protocol interface.

		Returns:
			number
		"""
		return self._get_attribute('numberOfChannels')
	@NumberOfChannels.setter
	def NumberOfChannels(self, value):
		self._set_attribute('numberOfChannels', value)

	@property
	def PeriodicEcho(self):
		"""If selected, the Interface sends echo requests periodically to keep the OpenFlow session connected.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicEcho')

	@property
	def PeriodicLLDP(self):
		"""If selected, the interface sends LLDP packets periodically to discover new links.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicLLDP')

	@property
	def PeriodicLLDPInterval(self):
		"""The periodic interval in milliseconds at which the Interface sends LLDP packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicLLDPInterval')

	@property
	def ResponseTimeout(self):
		"""The time in milliseconds after which the trigger request times out, if no response is received

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('responseTimeout')

	@property
	def SendPortFeatureAtStartup(self):
		"""If selected, port Description request is sent when the connection is established

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendPortFeatureAtStartup')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SetAsyncConfig(self):
		"""Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters

		Returns:
			bool
		"""
		return self._get_attribute('setAsyncConfig')
	@SetAsyncConfig.setter
	def SetAsyncConfig(self, value):
		self._set_attribute('setAsyncConfig', value)

	@property
	def SetSwitchConfig(self):
		"""Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters

		Returns:
			bool
		"""
		return self._get_attribute('setSwitchConfig')
	@SetSwitchConfig.setter
	def SetSwitchConfig(self, value):
		self._set_attribute('setSwitchConfig', value)

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
	def StartupEmptyTableFeatureRequest(self):
		"""If selected, the Table Feature Request is sent at start up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startupEmptyTableFeatureRequest')

	@property
	def StartupFeatureRequest(self):
		"""If selected, port feature request is sent when the connection is established.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startupFeatureRequest')

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
	def TcpPort(self):
		"""Specify the TCP port for this interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tcpPort')

	@property
	def TimeoutOption(self):
		"""The types of timeout options supported. Choose one of the following: 1) Multiplier 2) Timeout Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutOption')

	@property
	def TimeoutOptionValue(self):
		"""The value specified for the selected Timeout option.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutOptionValue')

	@property
	def TlsVersion(self):
		"""TLS version selection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tlsVersion')

	@property
	def TriggerLldp(self):
		"""If selected, LLDP is triggered

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('triggerLldp')

	@property
	def TypeOfConnection(self):
		"""The type of connection used for the Interface. Options include: 1) TCP 2) TLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('typeOfConnection')

	@property
	def Version(self):
		"""Implementation Version

		Returns:
			number
		"""
		return self._get_attribute('version')

	@property
	def VersionSupported(self):
		"""Indicates the supported OpenFlow version number.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('versionSupported')

	def remove(self):
		"""Deletes a child instance of OpenFlowController on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ClearAllLearnedInfo(self, Arg1):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, Arg2):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear OF Channels learnt by this Controller.

		Args:
			Arg2 (list(number)): List of OF Channel into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearAllLearnedInfo', payload=locals(), response_object=None)

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

	def GetOFChannelLearnedInfo(self, Arg1):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Get OF Channel Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Get OF Channel Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Get OF Channel Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self, Arg2):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Gets OF Channels learnt by this Controller.

		Args:
			Arg2 (list(number)): List of OF Channel into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self, Arg1):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Get OF Topology Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getOFTopologyLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Get OF Topology Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getOFTopologyLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Get OF Topology Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getOFTopologyLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self, Arg2):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Gets OF Topology learnt by this Controller.

		Args:
			Arg2 (list(number)): List of OF session into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getOFTopologyLearnedInfo', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def SendLLDPPacketOut(self, Arg1, LldpDestination, EnableLldpFlowAdd, LldpTimeoutVal):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			LldpDestination (str): This parameter requires a lldpDestination of type kString
			EnableLldpFlowAdd (bool): This parameter requires a enableLldpFlowAdd of type kBool
			LldpTimeoutVal (number): This parameter requires a lldpTimeoutVal of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('sendLLDPPacketOut', payload=locals(), response_object=None)

	def SendLLDPPacketOut(self, Arg1, LldpDestination, EnableLldpFlowAdd, LldpTimeoutVal, SessionIndices):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			LldpDestination (str): This parameter requires a lldpDestination of type kString
			EnableLldpFlowAdd (bool): This parameter requires a enableLldpFlowAdd of type kBool
			LldpTimeoutVal (number): This parameter requires a lldpTimeoutVal of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('sendLLDPPacketOut', payload=locals(), response_object=None)

	def SendLLDPPacketOut(self, Arg1, SessionIndices, LldpDestination, EnableLldpFlowAdd, LldpTimeoutVal):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a lldpDestination of type kString
			LldpDestination (str): This parameter requires a enableLldpFlowAdd of type kBool
			EnableLldpFlowAdd (bool): This parameter requires a lldpTimeoutVal of type kInteger
			LldpTimeoutVal (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('sendLLDPPacketOut', payload=locals(), response_object=None)

	def SendLLDPPacketOut(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out to all Switches.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str): LLDP Destination MAC
			Arg4 (bool): Enable LLDP Flow Add in Switch
			Arg5 (number): LLDP Timeout Value

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendLLDPPacketOut', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def StartController(self, Arg1):
		"""Executes the startController operation on the server.

		Start OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startController', payload=locals(), response_object=None)

	def StartController(self, Arg1, SessionIndices):
		"""Executes the startController operation on the server.

		Start OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startController', payload=locals(), response_object=None)

	def StartController(self, Arg1, SessionIndices):
		"""Executes the startController operation on the server.

		Start OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startController', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def StopController(self, Arg1):
		"""Executes the stopController operation on the server.

		Stop OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopController', payload=locals(), response_object=None)

	def StopController(self, Arg1, SessionIndices):
		"""Executes the stopController operation on the server.

		Stop OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopController', payload=locals(), response_object=None)

	def StopController(self, Arg1, SessionIndices):
		"""Executes the stopController operation on the server.

		Stop OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./openFlowController object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopController', payload=locals(), response_object=None)
