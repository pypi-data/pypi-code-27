from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisFabricPathRouter(Base):
	"""Fabric Path Configuration
	"""

	_SDM_NAME = 'isisFabricPathRouter'

	def __init__(self, parent):
		super(IsisFabricPathRouter, self).__init__(parent)

	@property
	def DceMCastIpv4GroupList(self):
		"""Returns the one and only one DceMCastIpv4GroupList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcemcastipv4grouplist.DceMCastIpv4GroupList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcemcastipv4grouplist import DceMCastIpv4GroupList
		return self._read(DceMCastIpv4GroupList(self), None)

	@property
	def DceMCastIpv6GroupList(self):
		"""Returns the one and only one DceMCastIpv6GroupList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcemcastipv6grouplist.DceMCastIpv6GroupList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcemcastipv6grouplist import DceMCastIpv6GroupList
		return self._read(DceMCastIpv6GroupList(self), None)

	@property
	def DceMCastMacGroupList(self):
		"""Returns the one and only one DceMCastMacGroupList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcemcastmacgrouplist.DceMCastMacGroupList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcemcastmacgrouplist import DceMCastMacGroupList
		return self._read(DceMCastMacGroupList(self), None)

	@property
	def DceTopologyList(self):
		"""Returns the one and only one DceTopologyList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcetopologylist.DceTopologyList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dcetopologylist import DceTopologyList
		return self._read(DceTopologyList(self), None)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AreaAddresses(self):
		"""Area Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaAddresses')

	@property
	def AreaAuthenticationType(self):
		"""Area Authentication Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaAuthenticationType')

	@property
	def AreaTransmitPasswordOrMD5Key(self):
		"""Area Transmit Password / MD5-Key

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaTransmitPasswordOrMD5Key')

	@property
	def Attached(self):
		"""Attached

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('attached')

	@property
	def CSNPInterval(self):
		"""CSNP Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cSNPInterval')

	@property
	def CapabilityRouterId(self):
		"""Capability Router Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityRouterId')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DceMCastIpv4GroupCount(self):
		"""# Multicast IPv4 Groups(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('dceMCastIpv4GroupCount')
	@DceMCastIpv4GroupCount.setter
	def DceMCastIpv4GroupCount(self, value):
		self._set_attribute('dceMCastIpv4GroupCount', value)

	@property
	def DceMCastIpv6GroupCount(self):
		"""# Multicast IPv6 Groups(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('dceMCastIpv6GroupCount')
	@DceMCastIpv6GroupCount.setter
	def DceMCastIpv6GroupCount(self, value):
		self._set_attribute('dceMCastIpv6GroupCount', value)

	@property
	def DceMCastMacGroupCount(self):
		"""MAC Group Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('dceMCastMacGroupCount')
	@DceMCastMacGroupCount.setter
	def DceMCastMacGroupCount(self, value):
		self._set_attribute('dceMCastMacGroupCount', value)

	@property
	def DceTopologyCount(self):
		"""Topology Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('dceTopologyCount')
	@DceTopologyCount.setter
	def DceTopologyCount(self, value):
		self._set_attribute('dceTopologyCount', value)

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DiscardLSPs(self):
		"""Discard LSPs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardLSPs')

	@property
	def EnableHelloPadding(self):
		"""Enable Hello Padding

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHelloPadding')

	@property
	def EnableHostName(self):
		"""Enable Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHostName')

	@property
	def EnableWideMetric(self):
		"""Enable Wide Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableWideMetric')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def HostName(self):
		"""Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostName')

	@property
	def IgnoreReceiveMD5(self):
		"""Ignore Receive MD5

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignoreReceiveMD5')

	@property
	def InterLSPsOrMGroupPDUBurstGap(self):
		"""Inter LSPs/MGROUP-PDUs Burst Gap (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interLSPsOrMGroupPDUBurstGap')

	@property
	def LSPLifetime(self):
		"""LSP Rifetime (sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPLifetime')

	@property
	def LSPRefreshRate(self):
		"""LSP Refresh Rate (sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPRefreshRate')

	@property
	def LSPorMGroupPDUMinTransmissionInterval(self):
		"""LSP/MGROUP-PDU Min Transmission Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPorMGroupPDUMinTransmissionInterval')

	@property
	def LocalSystemID(self):
		"""System ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localSystemID')

	@property
	def MaxAreaAddresses(self):
		"""Maximum Area Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxAreaAddresses')

	@property
	def MaxLSPSize(self):
		"""Max LSP Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLSPSize')

	@property
	def MaxLSPsOrMGroupPDUsPerBurst(self):
		"""Max LSPs/MGROUP-PDUs Per Burst

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLSPsOrMGroupPDUsPerBurst')

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
	def Overloaded(self):
		"""Overloaded

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('overloaded')

	@property
	def PSNPInterval(self):
		"""PSNP Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pSNPInterval')

	@property
	def PartitionRepair(self):
		"""Partition Repair

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('partitionRepair')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session Information

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

	def IsisStartRouter(self, Arg1):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('isisStartRouter', payload=locals(), response_object=None)

	def IsisStartRouter(self, Arg1, SessionIndices):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('isisStartRouter', payload=locals(), response_object=None)

	def IsisStartRouter(self, Arg1, SessionIndices):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('isisStartRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self, Arg1):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('isisStopRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self, Arg1, SessionIndices):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('isisStopRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self, Arg1, SessionIndices):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('isisStopRouter', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisFabricPathRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
