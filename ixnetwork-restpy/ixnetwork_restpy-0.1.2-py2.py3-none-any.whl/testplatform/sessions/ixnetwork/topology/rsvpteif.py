from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RsvpteIf(Base):
	"""Rsvp Neighbor (Device) level Configuration
	"""

	_SDM_NAME = 'rsvpteIf'

	def __init__(self, parent):
		super(RsvpteIf, self).__init__(parent)

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
	def ActualRestartTime(self):
		"""Actual Restart Time (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('actualRestartTime')

	@property
	def AdvertisedRestartTime(self):
		"""Advertised Restart Time (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertisedRestartTime')

	@property
	def AuthenticationAlgorithm(self):
		"""Authentication Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authenticationAlgorithm')

	@property
	def AuthenticationKeyForReceivedPackets(self):
		"""Authentication Key for Received Packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authenticationKeyForReceivedPackets')

	@property
	def AuthenticationKeyForSentPackets(self):
		"""Authentication Key for Sent Packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authenticationKeyForSentPackets')

	@property
	def AuthenticationKeyIdentifier(self):
		"""Authentication Key Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authenticationKeyIdentifier')

	@property
	def AutoGenerateAuthenticationKeyIdentifier(self):
		"""Auto Generate Authentication Key Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoGenerateAuthenticationKeyIdentifier')

	@property
	def BundleMessageThresholdTime(self):
		"""Bundle Message Threshold Time (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bundleMessageThresholdTime')

	@property
	def CheckIntegrityForReceivedPackets(self):
		"""Check Integrity for Received Packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('checkIntegrityForReceivedPackets')

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
	def DutIp(self):
		"""DUT IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dutIp')

	@property
	def EnableBfdRegistration(self):
		"""Enable BFD Registration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBfdRegistration')

	@property
	def EnableBundleMessageSending(self):
		"""Enable Bundle Message Sending

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBundleMessageSending')

	@property
	def EnableBundleMessageThresholdTimer(self):
		"""Enable Bundle Message Threshold Timer

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBundleMessageThresholdTimer')

	@property
	def EnableGracefulRestartHelperMode(self):
		"""Enable Helper-Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableGracefulRestartHelperMode')

	@property
	def EnableGracefulRestartRestartingMode(self):
		"""Enable Restarting-Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableGracefulRestartRestartingMode')

	@property
	def EnableHelloExtension(self):
		"""Enable Hello Extension

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHelloExtension')

	@property
	def EnableRefreshReduction(self):
		"""Enable Refresh Reduction

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRefreshReduction')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def GenerateSequenceNumberBasedOnRealTime(self):
		"""Generate Sequence Number Based on Real Time

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('generateSequenceNumberBasedOnRealTime')

	@property
	def HandshakeRequired(self):
		"""Handshake Required

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('handshakeRequired')

	@property
	def HelloInterval(self):
		"""Hello Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('helloInterval')

	@property
	def HelloTimeoutMultiplier(self):
		"""Hello Timeout Multiplier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('helloTimeoutMultiplier')

	@property
	def InitialSequenceNumber(self):
		"""Initial Sequence Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initialSequenceNumber')

	@property
	def LabelReqRefCount(self):
		"""Number of Label Req in RSVP-TE DG

		Returns:
			number
		"""
		return self._get_attribute('labelReqRefCount')
	@LabelReqRefCount.setter
	def LabelReqRefCount(self, value):
		self._set_attribute('labelReqRefCount', value)

	@property
	def LabelSpaceEnd(self):
		"""Label Space End

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelSpaceEnd')

	@property
	def LabelSpaceStart(self):
		"""Label Space Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelSpaceStart')

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
	def NumberOfRestarts(self):
		"""Number of Restarts

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numberOfRestarts')

	@property
	def OurIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('ourIp')

	@property
	def RecoveryTime(self):
		"""Recovery Time (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('recoveryTime')

	@property
	def RestartStartTime(self):
		"""Restart Start Time (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('restartStartTime')

	@property
	def RestartUpTime(self):
		"""Restart Up Time (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('restartUpTime')

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
	def SummaryRefreshInterval(self):
		"""Summary Refresh Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('summaryRefreshInterval')

	@property
	def UseSameAuthenticationKeyForPeer(self):
		"""Use Same Authentication Key for Peer

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useSameAuthenticationKeyForPeer')

	@property
	def UsingGatewayIp(self):
		"""Using Gateway IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('usingGatewayIp')

	def remove(self):
		"""Deletes a child instance of RsvpteIf on the server.

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

	def GetLearnedInfo(self, Arg1):
		"""Executes the getLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getLearnedInfo', payload=locals(), response_object=None)

	def GetLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
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

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartNeighbor(self, Arg2):
		"""Executes the restartNeighbor operation on the server.

		Restart Neighbor

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('restartNeighbor', payload=locals(), response_object=None)

	def RsvpRestartNeighbor(self, Arg1):
		"""Executes the rsvpRestartNeighbor operation on the server.

		Gracefully restart selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpRestartNeighbor', payload=locals(), response_object=None)

	def RsvpRestartNeighbor(self, Arg1, SessionIndices):
		"""Executes the rsvpRestartNeighbor operation on the server.

		Gracefully restart selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpRestartNeighbor', payload=locals(), response_object=None)

	def RsvpRestartNeighbor(self, Arg1, SessionIndices):
		"""Executes the rsvpRestartNeighbor operation on the server.

		Gracefully restart selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpRestartNeighbor', payload=locals(), response_object=None)

	def RsvpResumeHello(self, Arg1):
		"""Executes the rsvpResumeHello operation on the server.

		Resume sending Hello messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpResumeHello', payload=locals(), response_object=None)

	def RsvpResumeHello(self, Arg1, SessionIndices):
		"""Executes the rsvpResumeHello operation on the server.

		Resume sending Hello messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpResumeHello', payload=locals(), response_object=None)

	def RsvpResumeHello(self, Arg1, SessionIndices):
		"""Executes the rsvpResumeHello operation on the server.

		Resume sending Hello messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpResumeHello', payload=locals(), response_object=None)

	def RsvpStartSRefresh(self, Arg1):
		"""Executes the rsvpStartSRefresh operation on the server.

		Start sending SRefresh messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStartSRefresh', payload=locals(), response_object=None)

	def RsvpStartSRefresh(self, Arg1, SessionIndices):
		"""Executes the rsvpStartSRefresh operation on the server.

		Start sending SRefresh messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStartSRefresh', payload=locals(), response_object=None)

	def RsvpStartSRefresh(self, Arg1, SessionIndices):
		"""Executes the rsvpStartSRefresh operation on the server.

		Start sending SRefresh messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStartSRefresh', payload=locals(), response_object=None)

	def RsvpStopHello(self, Arg1):
		"""Executes the rsvpStopHello operation on the server.

		Stop sending Hello messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStopHello', payload=locals(), response_object=None)

	def RsvpStopHello(self, Arg1, SessionIndices):
		"""Executes the rsvpStopHello operation on the server.

		Stop sending Hello messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStopHello', payload=locals(), response_object=None)

	def RsvpStopHello(self, Arg1, SessionIndices):
		"""Executes the rsvpStopHello operation on the server.

		Stop sending Hello messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStopHello', payload=locals(), response_object=None)

	def RsvpStopSRefresh(self, Arg1):
		"""Executes the rsvpStopSRefresh operation on the server.

		Stop sending SRefresh messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStopSRefresh', payload=locals(), response_object=None)

	def RsvpStopSRefresh(self, Arg1, SessionIndices):
		"""Executes the rsvpStopSRefresh operation on the server.

		Stop sending SRefresh messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStopSRefresh', payload=locals(), response_object=None)

	def RsvpStopSRefresh(self, Arg1, SessionIndices):
		"""Executes the rsvpStopSRefresh operation on the server.

		Stop sending SRefresh messages from selected Neighbors

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('rsvpStopSRefresh', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Activate/Enable selected Neighbor Pairs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable selected Neighbor Pairs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable selected Neighbor Pairs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def StartHello(self, Arg2):
		"""Executes the startHello operation on the server.

		Start Hello

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('startHello', payload=locals(), response_object=None)

	def StartSRefresh(self, Arg2):
		"""Executes the startSRefresh operation on the server.

		Start SRefresh

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('startSRefresh', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Neighbor Pairs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Neighbor Pairs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Neighbor Pairs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpteIf object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def StopHello(self, Arg2):
		"""Executes the stopHello operation on the server.

		Stop Hello

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopHello', payload=locals(), response_object=None)

	def StopSRefresh(self, Arg2):
		"""Executes the stopSRefresh operation on the server.

		Stop SRefresh

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopSRefresh', payload=locals(), response_object=None)
