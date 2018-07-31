from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Pcc(Base):
	"""Pcep Session (Device) level Configuration
	"""

	_SDM_NAME = 'pcc'

	def __init__(self, parent):
		super(Pcc, self).__init__(parent)

	@property
	def ExpectedInitiatedLspList(self):
		"""Returns the one and only one ExpectedInitiatedLspList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.expectedinitiatedlsplist.ExpectedInitiatedLspList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.expectedinitiatedlsplist import ExpectedInitiatedLspList
		return self._read(ExpectedInitiatedLspList(self), None)

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
	def PccLearnedLspDb(self):
		"""Returns the one and only one PccLearnedLspDb object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcclearnedlspdb.PccLearnedLspDb)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcclearnedlspdb import PccLearnedLspDb
		return self._read(PccLearnedLspDb(self), None)

	@property
	def PcepBackupPCEs(self):
		"""Returns the one and only one PcepBackupPCEs object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepbackuppces.PcepBackupPCEs)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepbackuppces import PcepBackupPCEs
		return self._read(PcepBackupPCEs(self), None)

	@property
	def PreEstablishedSrLsps(self):
		"""Returns the one and only one PreEstablishedSrLsps object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.preestablishedsrlsps.PreEstablishedSrLsps)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.preestablishedsrlsps import PreEstablishedSrLsps
		return self._read(PreEstablishedSrLsps(self), None)

	@property
	def RequestedLsps(self):
		"""Returns the one and only one RequestedLsps object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestedlsps.RequestedLsps)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestedlsps import RequestedLsps
		return self._read(RequestedLsps(self), None)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Active_pre_established_lsps(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('active_pre_established_lsps')
	@Active_pre_established_lsps.setter
	def Active_pre_established_lsps(self, value):
		self._set_attribute('active_pre_established_lsps', value)

	@property
	def Authentication(self):
		"""The type of cryptographic authentication to be used on this link interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authentication')

	@property
	def BurstInterval(self):
		"""Interval in milisecond in which desired rate of messages needs to be maintained.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('burstInterval')

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
	def DeadInterval(self):
		"""This is the time interval, after the expiration of which, a PCEP peer declares the session down if no PCEP message has been received.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('deadInterval')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def ErrorValue(self):
		"""To configure the type of error. Editable only if Return Instantiation Error is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorValue')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def ExpectedInitiatedLspsForTraffic(self):
		"""Based on the value in this control the number of Expected Initiated LSPs for Traffic can be configured. This is used for traffic only.

		Returns:
			number
		"""
		return self._get_attribute('expectedInitiatedLspsForTraffic')
	@ExpectedInitiatedLspsForTraffic.setter
	def ExpectedInitiatedLspsForTraffic(self, value):
		self._set_attribute('expectedInitiatedLspsForTraffic', value)

	@property
	def KeepaliveInterval(self):
		"""Frequency/Time Interval of sending PCEP messages to keep the session active.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keepaliveInterval')

	@property
	def MD5Key(self):
		"""A value to be used as the secret MD5 Key.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mD5Key')

	@property
	def MaxLspsPerPcRpt(self):
		"""Controls the maximum LSP information that can be present in a Path report message when the session is stateful session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLspsPerPcRpt')

	@property
	def MaxReconnectInterval(self):
		"""This is the maximum time interval, by which recoonect timer will be increased upto.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxReconnectInterval')

	@property
	def MaxRequestedLspPerInterval(self):
		"""Maximum number of LSP computation request messages can be sent per interval.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxRequestedLspPerInterval')

	@property
	def MaxSyncLspPerInterval(self):
		"""Maximum number of LSP sync can be sent per interval.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxSyncLspPerInterval')

	@property
	def MaximumSidDepth(self):
		"""Maximum SID Depth field (MSD) specifies the maximum number of SIDs that a PCC is capable of imposing on a packet. Editable only if SR PCE Capability is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maximumSidDepth')

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
	def NumberOfBackupPCEs(self):
		"""Number of Backup PCEs

		Returns:
			number
		"""
		return self._get_attribute('numberOfBackupPCEs')
	@NumberOfBackupPCEs.setter
	def NumberOfBackupPCEs(self, value):
		self._set_attribute('numberOfBackupPCEs', value)

	@property
	def PccPpagTLVType(self):
		"""PPAG TLV Type specifies PCC's capability of interpreting this type of PPAG TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pccPpagTLVType')

	@property
	def PceIpv4Address(self):
		"""IPv4 address of the PCE. This column is greyed out in case of PCCv6.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pceIpv4Address')

	@property
	def PreEstablishedSrLspsPerPcc(self):
		"""Pre-Established SR LSPs per PCC

		Returns:
			number
		"""
		return self._get_attribute('preEstablishedSrLspsPerPcc')
	@PreEstablishedSrLspsPerPcc.setter
	def PreEstablishedSrLspsPerPcc(self, value):
		self._set_attribute('preEstablishedSrLspsPerPcc', value)

	@property
	def RateControl(self):
		"""The rate control is an optional feature associated with PCE initiated LSP.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rateControl')

	@property
	def ReconnectInterval(self):
		"""This is the time interval, after the expiration of which, retry to establish the broken session by PCC happen.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reconnectInterval')

	@property
	def RequestedLspsPerPcc(self):
		"""Requested LSPs per PCC

		Returns:
			number
		"""
		return self._get_attribute('requestedLspsPerPcc')
	@RequestedLspsPerPcc.setter
	def RequestedLspsPerPcc(self, value):
		self._set_attribute('requestedLspsPerPcc', value)

	@property
	def ReturnInstantiationError(self):
		"""If enabled, then PCC will reply PCErr upon receiving PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('returnInstantiationError')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SrPceCapability(self):
		"""The SR PCE Capability TLV is an optional TLV associated with the OPEN Object to exchange SR capability of PCEP speakers.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srPceCapability')

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
	def StateTimeoutInterval(self):
		"""This is the time interval, after the expiration of which, LSP is cleaned up by PCC.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('stateTimeoutInterval')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def TcpPort(self):
		"""PCEP operates over TCP using a registered TCP port (default - 4189). This allows the requirements of reliable messaging and flow control to bemet without further protocol work. This control can be configured when user does not want to use the default one.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tcpPort')

	def remove(self):
		"""Deletes a child instance of Pcc on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ClearPccLearnedInfoInClient(self, Arg1):
		"""Executes the clearPccLearnedInfoInClient operation on the server.

		Clears ALL Learned LSP Information of PCC Device.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearPccLearnedInfoInClient', payload=locals(), response_object=None)

	def ClearPccLearnedInfoInClient(self, Arg1, SessionIndices):
		"""Executes the clearPccLearnedInfoInClient operation on the server.

		Clears ALL Learned LSP Information of PCC Device.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearPccLearnedInfoInClient', payload=locals(), response_object=None)

	def ClearPccLearnedInfoInClient(self, Arg1, SessionIndices):
		"""Executes the clearPccLearnedInfoInClient operation on the server.

		Clears ALL Learned LSP Information of PCC Device.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearPccLearnedInfoInClient', payload=locals(), response_object=None)

	def ClearPccLearnedInfoInClient(self, Arg2):
		"""Executes the clearPccLearnedInfoInClient operation on the server.

		Clears ALL Learned LSP Information By PCC Device.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearPccLearnedInfoInClient', payload=locals(), response_object=None)

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

	def GetPccBasicAllSrLspLearnedInfo(self, Arg1):
		"""Executes the getPccBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicAllSrLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicAllSrLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicAllSrLspLearnedInfo(self, Arg2):
		"""Executes the getPccBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCC.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPccBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccRequestedLspLearnedInfo(self, Arg1):
		"""Executes the getPccBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccRequestedLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccRequestedLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccRequestedLspLearnedInfo(self, Arg2):
		"""Executes the getPccBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCC.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPccBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccSyncOrReportLspLearnedInfo(self, Arg1):
		"""Executes the getPccBasicSrPccSyncOrReportLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPccSyncOrReportLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccSyncOrReportLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicSrPccSyncOrReportLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPccSyncOrReportLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccSyncOrReportLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicSrPccSyncOrReportLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPccSyncOrReportLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPccSyncOrReportLspLearnedInfo(self, Arg2):
		"""Executes the getPccBasicSrPccSyncOrReportLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCC.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPccBasicSrPccSyncOrReportLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPceInitiatedLspLearnedInfo(self, Arg1):
		"""Executes the getPccBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPceInitiatedLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPceInitiatedLspLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccBasicSrPceInitiatedLspLearnedInfo(self, Arg2):
		"""Executes the getPccBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCC.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPccBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPccLearnedInfo(self, Arg1):
		"""Executes the getPccLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccLearnedInfo', payload=locals(), response_object=None)

	def GetPccLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccLearnedInfo', payload=locals(), response_object=None)

	def GetPccLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getPccLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCC.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getPccLearnedInfo', payload=locals(), response_object=None)

	def GetPccLearnedInfo(self, Arg2):
		"""Executes the getPccLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCC.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPccLearnedInfo', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcc object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
