from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ovsdbcontroller(Base):
	"""
	"""

	_SDM_NAME = 'ovsdbcontroller'

	def __init__(self, parent):
		super(Ovsdbcontroller, self).__init__(parent)

	@property
	def ClusterData(self):
		"""Returns the one and only one ClusterData object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.clusterdata.ClusterData)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.clusterdata import ClusterData
		return self._read(ClusterData(self), None)

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

	@property
	def ClearDumpDbFiles(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clearDumpDbFiles')

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
	def ConnectionType(self):
		"""Connection should use TCP or TLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('connectionType')

	@property
	def ControllerTcpPort(self):
		"""Specify the TCP port for the Controller

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('controllerTcpPort')

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
	def DirectoryName(self):
		"""Location of Directory in Client where the Certificate and Key Files are available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('directoryName')

	@property
	def DumpdbDirectoryName(self):
		"""Location of Directory in Client where the DumpDb Files are available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dumpdbDirectoryName')

	@property
	def EnableLogging(self):
		"""If true, Port debug logs will be recorded, Maximum recording will be upto 500 MB .

		Returns:
			bool
		"""
		return self._get_attribute('enableLogging')
	@EnableLogging.setter
	def EnableLogging(self, value):
		self._set_attribute('enableLogging', value)

	@property
	def EnableOvsdbServerIp(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableOvsdbServerIp')

	@property
	def ErrorCode(self):
		"""Error Code

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorDesc(self):
		"""Description of Error occured

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorDesc')

	@property
	def ErrorLogDirectoryName(self):
		"""Location of Directory in Client where the ErrorLog Files are available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorLogDirectoryName')

	@property
	def ErrorLogicalSwitchName(self):
		"""Error occured for this Logical Switch Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorLogicalSwitchName')

	@property
	def ErrorPhysicalSwitchName(self):
		"""Error occured for this Physical Switch Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorPhysicalSwitchName')

	@property
	def ErrorTimeStamp(self):
		"""Time Stamp at which Last Error occurred

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorTimeStamp')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def FileCaCertificate(self):
		"""CA Certificate File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCaCertificate')

	@property
	def FileCertificate(self):
		"""Certificate File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCertificate')

	@property
	def FileHWGatewayCertificate(self):
		"""HW Gateway Certificate File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileHWGatewayCertificate')

	@property
	def FilePrivKey(self):
		"""Private Key File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filePrivKey')

	@property
	def HSCConfiguration(self):
		"""Each VTEP has its own Hardware Switch Controller.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hSCConfiguration')

	@property
	def LatestDumpDbFileNames(self):
		"""Api to fetch latest DumpDb Files

		Returns:
			str
		"""
		return self._get_attribute('latestDumpDbFileNames')
	@LatestDumpDbFileNames.setter
	def LatestDumpDbFileNames(self, value):
		self._set_attribute('latestDumpDbFileNames', value)

	@property
	def LatestErrorFileNames(self):
		"""Api to fetch latest Error Files

		Returns:
			str
		"""
		return self._get_attribute('latestErrorFileNames')
	@LatestErrorFileNames.setter
	def LatestErrorFileNames(self, value):
		self._set_attribute('latestErrorFileNames', value)

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
	def OvsdbSchema(self):
		"""Database schema

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ovsdbSchema')

	@property
	def OvsdbServerIp(self):
		"""The IP address of the DUT or Ovs Server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ovsdbServerIp')

	@property
	def PseudoConnectedTo(self):
		"""GUI-only connection

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('pseudoConnectedTo')
	@PseudoConnectedTo.setter
	def PseudoConnectedTo(self, value):
		self._set_attribute('pseudoConnectedTo', value)

	@property
	def PseudoConnectedToBfd(self):
		"""GUI-only connection

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('pseudoConnectedToBfd')
	@PseudoConnectedToBfd.setter
	def PseudoConnectedToBfd(self, value):
		self._set_attribute('pseudoConnectedToBfd', value)

	@property
	def PseudoConnectedToVxlanReplicator(self):
		"""GUI-only connection

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('pseudoConnectedToVxlanReplicator')
	@PseudoConnectedToVxlanReplicator.setter
	def PseudoConnectedToVxlanReplicator(self, value):
		self._set_attribute('pseudoConnectedToVxlanReplicator', value)

	@property
	def PseudoMultiplier(self):
		"""Multiplier for GUI-only connection

		Returns:
			number
		"""
		return self._get_attribute('pseudoMultiplier')

	@property
	def PseudoMultiplierBfd(self):
		"""Multiplier for GUI-only connection

		Returns:
			number
		"""
		return self._get_attribute('pseudoMultiplierBfd')

	@property
	def PseudoMultiplierVxlanReplicator(self):
		"""Multiplier for GUI-only connection

		Returns:
			number
		"""
		return self._get_attribute('pseudoMultiplierVxlanReplicator')

	@property
	def Role(self):
		"""The role of the OVSDB Controller.

		Returns:
			list(str[master|none|slave])
		"""
		return self._get_attribute('role')

	@property
	def ServerAddDeleteConnectionError(self):
		"""API to retrieve error occured while Adding/ Deleting Server

		Returns:
			str
		"""
		return self._get_attribute('serverAddDeleteConnectionError')
	@ServerAddDeleteConnectionError.setter
	def ServerAddDeleteConnectionError(self, value):
		self._set_attribute('serverAddDeleteConnectionError', value)

	@property
	def ServerAddDeleteStatus(self):
		"""Status of all servers Added/Deleted to Controller. Use Get Server Add/Delete Status, right click action to get current status

		Returns:
			str
		"""
		return self._get_attribute('serverAddDeleteStatus')

	@property
	def ServerConnectionIp(self):
		"""The IP address of the DUT or Ovs Server which needs to be Added/Deleted.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serverConnectionIp')

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
	def TableNames(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tableNames')

	@property
	def TimeOut(self):
		"""Transact request Time Out in seconds. For scale scenarios increase this Timeout value.

		Returns:
			number
		"""
		return self._get_attribute('timeOut')
	@TimeOut.setter
	def TimeOut(self, value):
		self._set_attribute('timeOut', value)

	@property
	def VerifyHWGatewayCertificate(self):
		"""Verify HW Gateway Certificate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('verifyHWGatewayCertificate')

	@property
	def VerifyPeerCertificate(self):
		"""Verify Peer Certificate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('verifyPeerCertificate')

	@property
	def Vxlan(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('vxlan')
	@Vxlan.setter
	def Vxlan(self, value):
		self._set_attribute('vxlan', value)

	@property
	def VxlanReplicator(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('vxlanReplicator')
	@VxlanReplicator.setter
	def VxlanReplicator(self, value):
		self._set_attribute('vxlanReplicator', value)

	def remove(self):
		"""Deletes a child instance of Ovsdbcontroller on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def AddServer(self, Arg2):
		"""Executes the addServer operation on the server.

		Add Server.

		Args:
			Arg2 (list(number)): List of indices for which to Add Server.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('addServer', payload=locals(), response_object=None)

	def ClearLastErrors(self, Arg2):
		"""Executes the clearLastErrors operation on the server.

		Clear Error Messages reported due to Last Action.

		Args:
			Arg2 (list(number)): List of indices for which to clear last reported error messages.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearLastErrors', payload=locals(), response_object=None)

	def ClearPortLogs(self, Arg2):
		"""Executes the clearPortLogs operation on the server.

		Add Server.

		Args:
			Arg2 (list(number)): List of indices for which to Add Server.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearPortLogs', payload=locals(), response_object=None)

	def ControllerDumpDB(self, Arg2):
		"""Executes the controllerDumpDB operation on the server.

		Command to fetch Tor Information stored internally.

		Args:
			Arg2 (list(number)): List of indices into the device group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('controllerDumpDB', payload=locals(), response_object=None)

	def DeleteServer(self, Arg2):
		"""Executes the deleteServer operation on the server.

		Delete Server.

		Args:
			Arg2 (list(number)): List of indices for which to Delete Server.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('deleteServer', payload=locals(), response_object=None)

	def DumpDB(self, Arg2):
		"""Executes the dumpDB operation on the server.

		Attach.

		Args:
			Arg2 (list(number)): List of indices into the device group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('dumpDB', payload=locals(), response_object=None)

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

	def GetServerAddDeleteStatus(self, Arg2):
		"""Executes the getServerAddDeleteStatus operation on the server.

		Get Server Status.

		Args:
			Arg2 (list(number)): List of indices for which to get Server Status.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getServerAddDeleteStatus', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ovsdbcontroller object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
