from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MsrpTalker(Base):
	"""MSRP Talker level Configuration
	"""

	_SDM_NAME = 'msrpTalker'

	def __init__(self, parent):
		super(MsrpTalker, self).__init__(parent)

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
	def MsrpTalkerDomains(self):
		"""Returns the one and only one MsrpTalkerDomains object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrptalkerdomains.MsrpTalkerDomains)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrptalkerdomains import MsrpTalkerDomains
		return self._read(MsrpTalkerDomains(self), None)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdvertiseAs(self):
		"""Attribute Advertise As Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseAs')

	@property
	def AdvertiseVlanMembership(self):
		"""Advertise VLAN Membership from these talkers

		Returns:
			bool
		"""
		return self._get_attribute('advertiseVlanMembership')
	@AdvertiseVlanMembership.setter
	def AdvertiseVlanMembership(self, value):
		self._set_attribute('advertiseVlanMembership', value)

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
	def JoinTimer(self):
		"""MRP Join Timer in miliseconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('joinTimer')

	@property
	def LeaveAllTimer(self):
		"""MRP Leave All timer in milisecond

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('leaveAllTimer')

	@property
	def LeaveTimer(self):
		"""MRP Leave Timer in milisecond

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('leaveTimer')

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
	def ProtocolVersion(self):
		"""MRP protocol version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protocolVersion')

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
	def StreamCount(self):
		"""number of stream id instances per talker instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('streamCount')
	@StreamCount.setter
	def StreamCount(self, value):
		self._set_attribute('streamCount', value)

	@property
	def TalkerDomainCount(self):
		"""Domain Count

		Returns:
			number
		"""
		return self._get_attribute('talkerDomainCount')
	@TalkerDomainCount.setter
	def TalkerDomainCount(self, value):
		self._set_attribute('talkerDomainCount', value)

	def remove(self):
		"""Deletes a child instance of MsrpTalker on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ClearTalkerDatabasesInClient(self, Arg1):
		"""Executes the clearTalkerDatabasesInClient operation on the server.

		Clears ALL databses learnt by this MSRP Talker.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearTalkerDatabasesInClient', payload=locals(), response_object=None)

	def ClearTalkerDatabasesInClient(self, Arg1, SessionIndices):
		"""Executes the clearTalkerDatabasesInClient operation on the server.

		Clears ALL databses learnt by this MSRP Talker.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearTalkerDatabasesInClient', payload=locals(), response_object=None)

	def ClearTalkerDatabasesInClient(self, Arg1, SessionIndices):
		"""Executes the clearTalkerDatabasesInClient operation on the server.

		Clears ALL databses learnt by this MSRP Talker.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearTalkerDatabasesInClient', payload=locals(), response_object=None)

	def ClearTalkerDatabasesInClient(self, Arg2):
		"""Executes the clearTalkerDatabasesInClient operation on the server.

		Clears ALL databases learnt by this MSRP Talker.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearTalkerDatabasesInClient', payload=locals(), response_object=None)

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

	def GetMsrpTalkerDomainDatabase(self, Arg1):
		"""Executes the getMsrpTalkerDomainDatabase operation on the server.

		Gets Talker Domain Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerDomainDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpTalkerDomainDatabase operation on the server.

		Gets Talker Domain Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerDomainDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpTalkerDomainDatabase operation on the server.

		Gets Talker Domain Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerDomainDatabase(self, Arg2):
		"""Executes the getMsrpTalkerDomainDatabase operation on the server.

		Gets Talker Domain Database Information learnt by this Msrp Talker.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getMsrpTalkerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerStreamDatabase(self, Arg1):
		"""Executes the getMsrpTalkerStreamDatabase operation on the server.

		Gets Talker Stream Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerStreamDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpTalkerStreamDatabase operation on the server.

		Gets Talker Stream Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerStreamDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpTalkerStreamDatabase operation on the server.

		Gets Talker Stream Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerStreamDatabase(self, Arg2):
		"""Executes the getMsrpTalkerStreamDatabase operation on the server.

		Gets Talker Stream Database Information learnt by this Msrp Talker.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getMsrpTalkerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerVlanDatabase(self, Arg1):
		"""Executes the getMsrpTalkerVlanDatabase operation on the server.

		Gets Talker VLAN Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerVlanDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerVlanDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpTalkerVlanDatabase operation on the server.

		Gets Talker VLAN Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerVlanDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerVlanDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpTalkerVlanDatabase operation on the server.

		Gets Talker VLAN Database Information learnt by this Msrp Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpTalkerVlanDatabase', payload=locals(), response_object=None)

	def GetMsrpTalkerVlanDatabase(self, Arg2):
		"""Executes the getMsrpTalkerVlanDatabase operation on the server.

		Gets Talker VLAN Database Information learnt by this Msrp Talker.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getMsrpTalkerVlanDatabase', payload=locals(), response_object=None)

	def GetTalkerDatabases(self, Arg1):
		"""Executes the getTalkerDatabases operation on the server.

		Gets All databses learnt by this MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getTalkerDatabases', payload=locals(), response_object=None)

	def GetTalkerDatabases(self, Arg1, SessionIndices):
		"""Executes the getTalkerDatabases operation on the server.

		Gets All databses learnt by this MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getTalkerDatabases', payload=locals(), response_object=None)

	def GetTalkerDatabases(self, Arg1, SessionIndices):
		"""Executes the getTalkerDatabases operation on the server.

		Gets All databses learnt by this MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getTalkerDatabases', payload=locals(), response_object=None)

	def GetTalkerDatabases(self, Arg2):
		"""Executes the getTalkerDatabases operation on the server.

		Gets ALL databases learnt by this MSRP Talker.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getTalkerDatabases', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop MSRP Talker

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpTalker object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
