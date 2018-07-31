from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MsrpListener(Base):
	"""MSRP Listener level Configuration
	"""

	_SDM_NAME = 'msrpListener'

	def __init__(self, parent):
		super(MsrpListener, self).__init__(parent)

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
	def MsrpListenerDomains(self):
		"""Returns the one and only one MsrpListenerDomains object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrplistenerdomains.MsrpListenerDomains)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrplistenerdomains import MsrpListenerDomains
		return self._read(MsrpListenerDomains(self), None)

	@property
	def SubscribedStreams(self):
		"""Returns the one and only one SubscribedStreams object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.subscribedstreams.SubscribedStreams)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.subscribedstreams import SubscribedStreams
		return self._read(SubscribedStreams(self), None)

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
	def DeclareUnsolicitedVlan(self):
		"""Declare VLAN membership of configured VLAN range using MVRP even before learning any streams

		Returns:
			bool
		"""
		return self._get_attribute('declareUnsolicitedVlan')
	@DeclareUnsolicitedVlan.setter
	def DeclareUnsolicitedVlan(self, value):
		self._set_attribute('declareUnsolicitedVlan', value)

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
	def ListenerDomainCount(self):
		"""Domain Count

		Returns:
			number
		"""
		return self._get_attribute('listenerDomainCount')
	@ListenerDomainCount.setter
	def ListenerDomainCount(self, value):
		self._set_attribute('listenerDomainCount', value)

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
	def StartVlanId(self):
		"""Start VLAN ID of VLAN range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startVlanId')

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
	def SubscribeAll(self):
		"""Send MSRP Listener Ready for all streams advertised in recieved MSRP Talker Advertise

		Returns:
			bool
		"""
		return self._get_attribute('subscribeAll')
	@SubscribeAll.setter
	def SubscribeAll(self, value):
		self._set_attribute('subscribeAll', value)

	@property
	def SubscribedStreamCount(self):
		"""Count of streams Listener want to listen

		Returns:
			number
		"""
		return self._get_attribute('subscribedStreamCount')
	@SubscribedStreamCount.setter
	def SubscribedStreamCount(self, value):
		self._set_attribute('subscribedStreamCount', value)

	@property
	def VlanCount(self):
		"""VLAN count of VLAN range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlanCount')

	def remove(self):
		"""Deletes a child instance of MsrpListener on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ClearListenerDatabasesInClient(self, Arg1):
		"""Executes the clearListenerDatabasesInClient operation on the server.

		Clears ALL databases learnt by this MSRP Listener.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearListenerDatabasesInClient', payload=locals(), response_object=None)

	def ClearListenerDatabasesInClient(self, Arg1, SessionIndices):
		"""Executes the clearListenerDatabasesInClient operation on the server.

		Clears ALL databases learnt by this MSRP Listener.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearListenerDatabasesInClient', payload=locals(), response_object=None)

	def ClearListenerDatabasesInClient(self, Arg1, SessionIndices):
		"""Executes the clearListenerDatabasesInClient operation on the server.

		Clears ALL databases learnt by this MSRP Listener.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearListenerDatabasesInClient', payload=locals(), response_object=None)

	def ClearListenerDatabasesInClient(self, Arg2):
		"""Executes the clearListenerDatabasesInClient operation on the server.

		Clears ALL routes from GUI grid for the selected LDP Router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearListenerDatabasesInClient', payload=locals(), response_object=None)

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

	def GetListenerDatabases(self, Arg1):
		"""Executes the getListenerDatabases operation on the server.

		Gets All databases learnt by this MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getListenerDatabases', payload=locals(), response_object=None)

	def GetListenerDatabases(self, Arg1, SessionIndices):
		"""Executes the getListenerDatabases operation on the server.

		Gets All databases learnt by this MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getListenerDatabases', payload=locals(), response_object=None)

	def GetListenerDatabases(self, Arg1, SessionIndices):
		"""Executes the getListenerDatabases operation on the server.

		Gets All databases learnt by this MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getListenerDatabases', payload=locals(), response_object=None)

	def GetListenerDatabases(self, Arg2):
		"""Executes the getListenerDatabases operation on the server.

		Gets ALL routes learnt and stored by this LDP Router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getListenerDatabases', payload=locals(), response_object=None)

	def GetMsrpListenerDomainDatabase(self, Arg1):
		"""Executes the getMsrpListenerDomainDatabase operation on the server.

		Gets Listener Domain Database Information learnt by this Msrp Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerDomainDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpListenerDomainDatabase operation on the server.

		Gets Listener Domain Database Information learnt by this Msrp Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerDomainDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpListenerDomainDatabase operation on the server.

		Gets Listener Domain Database Information learnt by this Msrp Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerDomainDatabase(self, Arg2):
		"""Executes the getMsrpListenerDomainDatabase operation on the server.

		Gets Listener Domain Database Information learnt by this Msrp Listener.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getMsrpListenerDomainDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerStreamDatabase(self, Arg1):
		"""Executes the getMsrpListenerStreamDatabase operation on the server.

		Gets Listener Stream Database Information learnt by this Msrp Listener.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerStreamDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpListenerStreamDatabase operation on the server.

		Gets Listener Stream Database Information learnt by this Msrp Listener.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerStreamDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpListenerStreamDatabase operation on the server.

		Gets Listener Stream Database Information learnt by this Msrp Listener.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerStreamDatabase(self, Arg2):
		"""Executes the getMsrpListenerStreamDatabase operation on the server.

		Gets Listener Stream Database Information learnt by this Msrp Listener.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getMsrpListenerStreamDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerVlanDatabase(self, Arg1):
		"""Executes the getMsrpListenerVlanDatabase operation on the server.

		Gets Listener VLAN Database Information learnt by this Msrp Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerVlanDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerVlanDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpListenerVlanDatabase operation on the server.

		Gets Listener VLAN Database Information learnt by this Msrp Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerVlanDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerVlanDatabase(self, Arg1, SessionIndices):
		"""Executes the getMsrpListenerVlanDatabase operation on the server.

		Gets Listener VLAN Database Information learnt by this Msrp Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getMsrpListenerVlanDatabase', payload=locals(), response_object=None)

	def GetMsrpListenerVlanDatabase(self, Arg2):
		"""Executes the getMsrpListenerVlanDatabase operation on the server.

		Gets Listener VLAN Database Information learnt by this Msrp Listener.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getMsrpListenerVlanDatabase', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop MSRP Listener

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./msrpListener object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
