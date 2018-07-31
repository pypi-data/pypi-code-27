from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MldQuerier(Base):
	"""MLD Querier Configuration
	"""

	_SDM_NAME = 'mldQuerier'

	def __init__(self, parent):
		super(MldQuerier, self).__init__(parent)

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
	def DiscardLearntInfo(self):
		"""Discard Learned Info

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardLearntInfo')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def GeneralQueryInterval(self):
		"""General Query Interval in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('generalQueryInterval')

	@property
	def GeneralQueryResponseInterval(self):
		"""General Query Response Interval in milliseconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('generalQueryResponseInterval')

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
	def ProxyQuerier(self):
		"""Enable Proxy Querier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('proxyQuerier')

	@property
	def RobustnessVariable(self):
		"""Robustness Variable

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('robustnessVariable')

	@property
	def RouterAlert(self):
		"""Router Alert

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routerAlert')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[noIfaceUp|up])
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
	def SpecificQueryResponseInterval(self):
		"""Specific Query Response Interval in milliseconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('specificQueryResponseInterval')

	@property
	def SpecificQueryTransmissionCount(self):
		"""Specific Query Transmission Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('specificQueryTransmissionCount')

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
	def StartupQueryCount(self):
		"""Startup Query Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startupQueryCount')

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
	def SupportElection(self):
		"""Support Election

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportElection')

	@property
	def SupportOlderVersionHost(self):
		"""Support Older Version Host

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportOlderVersionHost')

	@property
	def SupportOlderVersionQuerier(self):
		"""Support Older Version Querier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportOlderVersionQuerier')

	@property
	def VersionType(self):
		"""Version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('versionType')

	def remove(self):
		"""Deletes a child instance of MldQuerier on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ClearAllLearnedInfoInClient(self, Arg2):
		"""Executes the clearAllLearnedInfoInClient operation on the server.

		Clears ALL routes from GUI grid for the selected BGP Peers.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearAllLearnedInfoInClient', payload=locals(), response_object=None)

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

	def GetLearnedInfo(self, Arg2):
		"""Executes the getLearnedInfo operation on the server.

		Gets all the LSPs and Topologies learnt by this MLD Querier.

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

	def MldGetLearnedInfo(self, Arg1):
		"""Executes the mldGetLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldGetLearnedInfo', payload=locals(), response_object=None)

	def MldGetLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the mldGetLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldGetLearnedInfo', payload=locals(), response_object=None)

	def MldGetLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the mldGetLearnedInfo operation on the server.

		Get Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldGetLearnedInfo', payload=locals(), response_object=None)

	def MldResumePeriodicGenQuery(self, Arg1):
		"""Executes the mldResumePeriodicGenQuery operation on the server.

		Resume Periodic General Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldResumePeriodicGenQuery', payload=locals(), response_object=None)

	def MldResumePeriodicGenQuery(self, Arg1, SessionIndices):
		"""Executes the mldResumePeriodicGenQuery operation on the server.

		Resume Periodic General Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldResumePeriodicGenQuery', payload=locals(), response_object=None)

	def MldResumePeriodicGenQuery(self, Arg1, SessionIndices):
		"""Executes the mldResumePeriodicGenQuery operation on the server.

		Resume Periodic General Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldResumePeriodicGenQuery', payload=locals(), response_object=None)

	def MldSendSpecificQuery(self, Arg1, Start_group_address, Group_count, Start_source_address, Source_count, Source_increment_step):
		"""Executes the mldSendSpecificQuery operation on the server.

		Send Specific Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			Start_group_address (str): This parameter requires a start_group_address of type kString
			Group_count (number): This parameter requires a group_count of type kInteger
			Start_source_address (str): This parameter requires a start_source_address of type kString
			Source_count (number): This parameter requires a source_count of type kInteger
			Source_increment_step (number): This parameter requires a source_increment_step of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldSendSpecificQuery', payload=locals(), response_object=None)

	def MldSendSpecificQuery(self, Arg1, Start_group_address, Group_count, Start_source_address, Source_count, Source_increment_step, SessionIndices):
		"""Executes the mldSendSpecificQuery operation on the server.

		Send Specific Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			Start_group_address (str): This parameter requires a start_group_address of type kString
			Group_count (number): This parameter requires a group_count of type kInteger
			Start_source_address (str): This parameter requires a start_source_address of type kString
			Source_count (number): This parameter requires a source_count of type kInteger
			Source_increment_step (number): This parameter requires a source_increment_step of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldSendSpecificQuery', payload=locals(), response_object=None)

	def MldSendSpecificQuery(self, Arg1, SessionIndices, Start_group_address, Group_count, Start_source_address, Source_count, Source_increment_step):
		"""Executes the mldSendSpecificQuery operation on the server.

		Send Specific Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a start_group_address of type kString
			Start_group_address (str): This parameter requires a group_count of type kInteger
			Group_count (number): This parameter requires a start_source_address of type kString
			Start_source_address (str): This parameter requires a source_count of type kInteger
			Source_count (number): This parameter requires a source_increment_step of type kInteger
			Source_increment_step (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldSendSpecificQuery', payload=locals(), response_object=None)

	def MldStartQuerier(self, Arg1):
		"""Executes the mldStartQuerier operation on the server.

		Start MLD Querier

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStartQuerier', payload=locals(), response_object=None)

	def MldStartQuerier(self, Arg1, SessionIndices):
		"""Executes the mldStartQuerier operation on the server.

		Start MLD Querier

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStartQuerier', payload=locals(), response_object=None)

	def MldStartQuerier(self, Arg1, SessionIndices):
		"""Executes the mldStartQuerier operation on the server.

		Start MLD Querier

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStartQuerier', payload=locals(), response_object=None)

	def MldStopPeriodicGenQuery(self, Arg1):
		"""Executes the mldStopPeriodicGenQuery operation on the server.

		Stop Periodic General Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStopPeriodicGenQuery', payload=locals(), response_object=None)

	def MldStopPeriodicGenQuery(self, Arg1, SessionIndices):
		"""Executes the mldStopPeriodicGenQuery operation on the server.

		Stop Periodic General Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStopPeriodicGenQuery', payload=locals(), response_object=None)

	def MldStopPeriodicGenQuery(self, Arg1, SessionIndices):
		"""Executes the mldStopPeriodicGenQuery operation on the server.

		Stop Periodic General Query

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStopPeriodicGenQuery', payload=locals(), response_object=None)

	def MldStopQuerier(self, Arg1):
		"""Executes the mldStopQuerier operation on the server.

		Stop MLD Querier

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStopQuerier', payload=locals(), response_object=None)

	def MldStopQuerier(self, Arg1, SessionIndices):
		"""Executes the mldStopQuerier operation on the server.

		Stop MLD Querier

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStopQuerier', payload=locals(), response_object=None)

	def MldStopQuerier(self, Arg1, SessionIndices):
		"""Executes the mldStopQuerier operation on the server.

		Stop MLD Querier

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('mldStopQuerier', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def ResumePeriodicGenQuery(self, Arg2):
		"""Executes the resumePeriodicGenQuery operation on the server.

		Resume Sending Periodic General Query

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('resumePeriodicGenQuery', payload=locals(), response_object=None)

	def SendSpecificQuery(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7):
		"""Executes the sendSpecificQuery operation on the server.

		Send Specific Query

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str): Start Group Address.
			Arg4 (number): Group Count.
			Arg5 (str): Start Source Address.
			Arg6 (number): Source Count.
			Arg7 (number): Source Increment Step.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendSpecificQuery', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def StartMLD(self, Arg1):
		"""Executes the startMLD operation on the server.

		Start MLD protocol on selected interfaces

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startMLD', payload=locals(), response_object=None)

	def StartMLD(self, Arg1, SessionIndices):
		"""Executes the startMLD operation on the server.

		Start MLD protocol on selected interfaces

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startMLD', payload=locals(), response_object=None)

	def StartMLD(self, Arg1, SessionIndices):
		"""Executes the startMLD operation on the server.

		Start MLD protocol on selected interfaces

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startMLD', payload=locals(), response_object=None)

	def StartMLD(self, Arg2, Arg3):
		"""Executes the startMLD operation on the server.

		Start MLD protocol on selected interfaces

		Args:
			Arg2 (str): ID to associate each async action invocation
			Arg3 (list(number)): List of indices into the group range grid An empty list indicates all instances in the plugin.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('startMLD', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def StopMLD(self, Arg1):
		"""Executes the stopMLD operation on the server.

		Stop MLD protocol on selected interfaces

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopMLD', payload=locals(), response_object=None)

	def StopMLD(self, Arg1, SessionIndices):
		"""Executes the stopMLD operation on the server.

		Stop MLD protocol on selected interfaces

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopMLD', payload=locals(), response_object=None)

	def StopMLD(self, Arg1, SessionIndices):
		"""Executes the stopMLD operation on the server.

		Stop MLD protocol on selected interfaces

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./mldQuerier object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopMLD', payload=locals(), response_object=None)

	def StopMLD(self, Arg2, Arg3):
		"""Executes the stopMLD operation on the server.

		Stop MLD protocol on selected interfaces

		Args:
			Arg2 (str): ID to associate each async action invocation
			Arg3 (list(number)): List of indices into the group range grid An empty list indicates all instances in the plugin.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopMLD', payload=locals(), response_object=None)

	def StopPeriodicGenQuery(self, Arg2):
		"""Executes the stopPeriodicGenQuery operation on the server.

		Stop Sending Periodic General Query

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopPeriodicGenQuery', payload=locals(), response_object=None)
