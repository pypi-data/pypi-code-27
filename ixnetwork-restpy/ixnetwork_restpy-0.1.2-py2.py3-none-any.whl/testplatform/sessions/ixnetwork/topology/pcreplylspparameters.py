from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PcReplyLspParameters(Base):
	"""PCReply LSP Parameters
	"""

	_SDM_NAME = 'pcReplyLspParameters'

	def __init__(self, parent):
		super(PcReplyLspParameters, self).__init__(parent)

	def PceXroSubObjectsList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PceXroSubObjectsList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceXroSubObjectsList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcexrosubobjectslist.PceXroSubObjectsList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcexrosubobjectslist import PceXroSubObjectsList
		return self._select(PceXroSubObjectsList(self), locals())

	def PcepEroSubObjectsList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PcepEroSubObjectsList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PcepEroSubObjectsList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceperosubobjectslist.PcepEroSubObjectsList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceperosubobjectslist import PcepEroSubObjectsList
		return self._select(PcepEroSubObjectsList(self), locals())

	def PcepMetricSubObjectsList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PcepMetricSubObjectsList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PcepMetricSubObjectsList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepmetricsubobjectslist.PcepMetricSubObjectsList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepmetricsubobjectslist import PcepMetricSubObjectsList
		return self._select(PcepMetricSubObjectsList(self), locals())

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Bandwidth(self):
		"""Bandwidth (bits/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidth')

	@property
	def BiDirectional(self):
		"""Bi-directional

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('biDirectional')

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
	def EnableCFlag(self):
		"""C Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableCFlag')

	@property
	def EnableEro(self):
		"""Include ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableEro')

	@property
	def EnableLoose(self):
		"""Loose

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLoose')

	@property
	def EnableXro(self):
		"""Include XRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableXro')

	@property
	def ExcludeAny(self):
		"""Exclude Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('excludeAny')

	@property
	def FailBit(self):
		"""Fail Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('failBit')

	@property
	def HoldingPriority(self):
		"""Holding Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('holdingPriority')

	@property
	def IncludeAll(self):
		"""Include All

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAll')

	@property
	def IncludeAny(self):
		"""Include Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAny')

	@property
	def IncludeBandwidth(self):
		"""Include Bandwidth

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeBandwidth')

	@property
	def IncludeLsp(self):
		"""Include LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLsp')

	@property
	def IncludeLspa(self):
		"""Include LSPA

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLspa')

	@property
	def IncludeMetric(self):
		"""Include Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMetric')

	@property
	def IncludeRp(self):
		"""Include RP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeRp')

	@property
	def IncludeSymbolicPathNameTlv(self):
		"""Indicates if Symbolic-Path-Name TLV is to be included in PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSymbolicPathNameTlv')

	@property
	def LocalProtection(self):
		"""Local Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtection')

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
	def NatureOfIssue(self):
		"""Nature Of Issue

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('natureOfIssue')

	@property
	def NumberOfEroSubObjects(self):
		"""Number of ERO Sub Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfEroSubObjects')
	@NumberOfEroSubObjects.setter
	def NumberOfEroSubObjects(self, value):
		self._set_attribute('numberOfEroSubObjects', value)

	@property
	def NumberOfMetricSubObject(self):
		"""Number of Metric

		Returns:
			number
		"""
		return self._get_attribute('numberOfMetricSubObject')
	@NumberOfMetricSubObject.setter
	def NumberOfMetricSubObject(self, value):
		self._set_attribute('numberOfMetricSubObject', value)

	@property
	def NumberOfXroSubObjects(self):
		"""Number of XRO Sub Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfXroSubObjects')
	@NumberOfXroSubObjects.setter
	def NumberOfXroSubObjects(self, value):
		self._set_attribute('numberOfXroSubObjects', value)

	@property
	def PlspId(self):
		"""An identifier for the LSP. A PCC creates a unique PLSP-ID for each LSP that is constant for the lifetime of a PCEP session. The PCC will advertise the same PLSP-ID on all PCEP sessions it maintains at a given time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('plspId')

	@property
	def PriorityValue(self):
		"""Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('priorityValue')

	@property
	def ProcessType(self):
		"""Indicates how the XRO is responded in the Path Request Response.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('processType')

	@property
	def ReceivedPLSPID(self):
		"""Received PLSP-ID in PcRequest

		Returns:
			list(number)
		"""
		return self._get_attribute('receivedPLSPID')

	@property
	def ReceivedSymbolicPath(self):
		"""Received Symbolic Path Name in PcRequest

		Returns:
			list(str)
		"""
		return self._get_attribute('receivedSymbolicPath')

	@property
	def ReflectLSP(self):
		"""Reflect LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectLSP')

	@property
	def ReflectRP(self):
		"""Reflect RP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectRP')

	@property
	def ReflectedObjectNoPath(self):
		"""Reflected Object

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectedObjectNoPath')

	@property
	def RequestId(self):
		"""Request ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requestId')

	@property
	def ResponseOptions(self):
		"""Reply Options

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('responseOptions')

	@property
	def ResponsePathType(self):
		"""Indicates which type of LSP will be responsed in the Path Request Response.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('responsePathType')

	@property
	def SessionInfo(self):
		"""Logs additional information about the LSP state

		Returns:
			list(str[delegatedActive|delegatedDown|delegatedGoingUp|delegatedUp|noLSPObjectInPCRequest|none|notDelegatedActive|notDelegatedDown|notDelegatedGoingUp|notDelegatedUp|pcErrorReceived|removedByPCC|replySentReportNotReceived])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SetupPriority(self):
		"""Setup Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setupPriority')

	@property
	def SymbolicPathName(self):
		"""Each LSP (path) must have a symbolic name that is unique in the PCC. It must remain constant throughout a path's lifetime, which may span across multiple consecutive PCEP sessions and/or PCC restarts.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('symbolicPathName')

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

	def ReturnDelegation(self, Arg1):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Replied LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcReplyLspParameters object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('returnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, Arg1, SessionIndices):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Replied LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcReplyLspParameters object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('returnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, Arg1, SessionIndices):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Replied LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pcReplyLspParameters object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('returnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, Arg2):
		"""Executes the returnDelegation operation on the server.

		Return Delegation helps PCE to return a delegation of LSP/LSPs.

		Args:
			Arg2 (list(number)): Return Delegation.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('returnDelegation', payload=locals(), response_object=None)
