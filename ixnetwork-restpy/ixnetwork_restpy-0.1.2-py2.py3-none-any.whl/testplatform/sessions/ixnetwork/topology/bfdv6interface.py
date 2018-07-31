from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Bfdv6Interface(Base):
	"""BFDv6 Interface level Configuration
	"""

	_SDM_NAME = 'bfdv6Interface'

	def __init__(self, parent):
		super(Bfdv6Interface, self).__init__(parent)

	@property
	def Bfdv6Session(self):
		"""Returns the one and only one Bfdv6Session object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6session.Bfdv6Session)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bfdv6session import Bfdv6Session
		return self._read(Bfdv6Session(self), None)

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

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AggregateBfdSession(self):
		"""If enabled, all interfaces except on VNI 0 will be disabled and grayed-out.

		Returns:
			bool
		"""
		return self._get_attribute('aggregateBfdSession')
	@AggregateBfdSession.setter
	def AggregateBfdSession(self, value):
		self._set_attribute('aggregateBfdSession', value)

	@property
	def ConfigureEchoSourceIp(self):
		"""Selecting this check box enables the ability to configure the source address IP of echo message

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureEchoSourceIp')

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
	def EchoRxInterval(self):
		"""The minimum interval, in milliseconds, between received BFD Echo packets that this interface is capable of supporting. If this value is zero, the transmitting system does not support the receipt of BFD Echo packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoRxInterval')

	@property
	def EchoTimeOut(self):
		"""The interval, in milliseconds, that the interface waits for a response to the last Echo packet sent out

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoTimeOut')

	@property
	def EchoTxInterval(self):
		"""The minimum interval, in milliseconds, that the interface would like to use when transmitting BFD Echo packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoTxInterval')

	@property
	def EnableControlPlaneIndependent(self):
		"""This check box enables Control Plane Independent Mode. If set, the interface's BFD is implemented in the forwarding plane and can continue to function through disruptions in the control plane

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableControlPlaneIndependent')

	@property
	def EnableDemandMode(self):
		"""This check box enables Demand Mode. In this mode, it is assumed the interface has an independent way of verifying it has connectivity to the other system. Once a BFD session is established, the systems stop sending BFD Control packets, except when either system feels the need to verify connectivity explicitly. In this case, a short sequence of BFD Control packets is sent

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDemandMode')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def FlapTxIntervals(self):
		"""The number of Tx packets sent from device after which session flaps for BFD. A value of zero means no flapping

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flapTxIntervals')

	@property
	def IpDiffServ(self):
		"""IP DiffServ/TOSByte (Dec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipDiffServ')

	@property
	def LocalRouterId(self):
		"""The BFD Router ID value, in IPv4 format.

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterId')

	@property
	def MinRxInterval(self):
		"""The minimum interval, in milliseconds, between received BFD Control packets that this interface is capable of supporting

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minRxInterval')

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
	def NoOfSessions(self):
		"""The number of configured BFD sessions

		Returns:
			number
		"""
		return self._get_attribute('noOfSessions')
	@NoOfSessions.setter
	def NoOfSessions(self, value):
		self._set_attribute('noOfSessions', value)

	@property
	def PollInterval(self):
		"""The interval, in milliseconds, between exchanges of Control Messages in Demand Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pollInterval')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SourceIp6(self):
		"""If Configure Echo Source-IP is selected, the IPv6 source address of the Echo Message

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIp6')

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
	def TimeoutMultiplier(self):
		"""The negotiated transmit interval, multiplied by this value, provides the detection time for the interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutMultiplier')

	@property
	def TxInterval(self):
		"""The minimum interval, in milliseconds, that the interface would like to use when transmitting BFD Control packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('txInterval')

	@property
	def Vni(self):
		"""Corresponding VXLAN Protocol VNI.

		Returns:
			list(number)
		"""
		return self._get_attribute('vni')

	def remove(self):
		"""Deletes a child instance of Bfdv6Interface on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ClearLearnedInfo(self, Arg1):
		"""Executes the clearLearnedInfo operation on the server.

		Clear Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearLearnedInfo', payload=locals(), response_object=None)

	def ClearLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the clearLearnedInfo operation on the server.

		Clear Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearLearnedInfo', payload=locals(), response_object=None)

	def ClearLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the clearLearnedInfo operation on the server.

		Clear Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearLearnedInfo', payload=locals(), response_object=None)

	def ClearLearnedInfo(self, Arg2):
		"""Executes the clearLearnedInfo operation on the server.

		Clear Learned Info

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearLearnedInfo', payload=locals(), response_object=None)

	def DisableDemandMode(self, Arg2, Arg3):
		"""Executes the disableDemandMode operation on the server.

		Disable Demand Mode

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('disableDemandMode', payload=locals(), response_object=None)

	def DisableDemandMode(self, Arg2):
		"""Executes the disableDemandMode operation on the server.

		Disable Demand Mode

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('disableDemandMode', payload=locals(), response_object=None)

	def EnableDemandMode(self, Arg2, Arg3):
		"""Executes the enableDemandMode operation on the server.

		Enable Demand Mode

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('enableDemandMode', payload=locals(), response_object=None)

	def EnableDemandMode(self, Arg2):
		"""Executes the enableDemandMode operation on the server.

		Enable Demand Mode

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('enableDemandMode', payload=locals(), response_object=None)

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

	def GetLearnedInfo(self, Arg1):
		"""Executes the getLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getLearnedInfo', payload=locals(), response_object=None)

	def GetLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getLearnedInfo', payload=locals(), response_object=None)

	def GetLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getLearnedInfo', payload=locals(), response_object=None)

	def GetLearnedInfo(self, Arg2):
		"""Executes the getLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getLearnedInfo', payload=locals(), response_object=None)

	def InitiatePoll(self, Arg2, Arg3):
		"""Executes the initiatePoll operation on the server.

		Initiate Poll

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('initiatePoll', payload=locals(), response_object=None)

	def InitiatePoll(self, Arg2):
		"""Executes the initiatePoll operation on the server.

		Initiate Poll

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('initiatePoll', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def ResumePDU(self, Arg2, Arg3):
		"""Executes the resumePDU operation on the server.

		Resume PDU

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('resumePDU', payload=locals(), response_object=None)

	def ResumePDU(self, Arg2):
		"""Executes the resumePDU operation on the server.

		Resume PDU

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('resumePDU', payload=locals(), response_object=None)

	def SetAdminDown(self, Arg2, Arg3):
		"""Executes the setAdminDown operation on the server.

		Set Admin Down

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('setAdminDown', payload=locals(), response_object=None)

	def SetAdminDown(self, Arg2):
		"""Executes the setAdminDown operation on the server.

		Set Admin Down

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('setAdminDown', payload=locals(), response_object=None)

	def SetAdminUp(self, Arg2, Arg3):
		"""Executes the setAdminUp operation on the server.

		Set Admin Up

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('setAdminUp', payload=locals(), response_object=None)

	def SetAdminUp(self, Arg2):
		"""Executes the setAdminUp operation on the server.

		Set Admin Up

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('setAdminUp', payload=locals(), response_object=None)

	def SetDiagnosticState(self, Arg2, Arg3, Arg4):
		"""Executes the setDiagnosticState operation on the server.

		Set Diagnostic State

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol
			Arg4 (str(administrativelyDown|concatenatedPathDown|controlDetectionTimeExpired|echoFunctionFailed|forwardingPlaneReset|neighbourSignaledSessionDown|pathDown|reserved|reverseConcatenatedPathDown)): Diagnostic Code

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('setDiagnosticState', payload=locals(), response_object=None)

	def SetDiagnosticState(self, Arg2, Arg3):
		"""Executes the setDiagnosticState operation on the server.

		Set Diagnostic State

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol
			Arg3 (str(administrativelyDown|concatenatedPathDown|controlDetectionTimeExpired|echoFunctionFailed|forwardingPlaneReset|neighbourSignaledSessionDown|pathDown|reserved|reverseConcatenatedPathDown)): Diagnostic Code

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('setDiagnosticState', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Activate Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Activate Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Activate Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Deactivate Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./bfdv6Interface object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def StopPDU(self, Arg2, Arg3):
		"""Executes the stopPDU operation on the server.

		Stop PDU

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopPDU', payload=locals(), response_object=None)

	def StopPDU(self, Arg2):
		"""Executes the stopPDU operation on the server.

		Stop PDU

		Args:
			Arg2 (str(bfd|bgp|isis|ldp|ospf|ospfv3|pim|rsvp)): Session used by Protocol

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopPDU', payload=locals(), response_object=None)
