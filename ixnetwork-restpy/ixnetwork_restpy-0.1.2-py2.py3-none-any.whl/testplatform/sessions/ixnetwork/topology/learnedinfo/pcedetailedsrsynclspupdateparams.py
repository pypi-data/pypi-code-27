from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceDetailedSrSyncLspUpdateParams(Base):
	"""PCE Learned LSPs Information Database
	"""

	_SDM_NAME = 'pceDetailedSrSyncLspUpdateParams'

	def __init__(self, parent):
		super(PceDetailedSrSyncLspUpdateParams, self).__init__(parent)

	def PceUpdateSrEroSubObjectList(self):
		"""Gets child instances of PceUpdateSrEroSubObjectList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceUpdateSrEroSubObjectList will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrerosubobjectlist.PceUpdateSrEroSubObjectList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrerosubobjectlist import PceUpdateSrEroSubObjectList
		return self._select(PceUpdateSrEroSubObjectList(self), locals())

	def PceUpdateSrMetricSubObjectList(self):
		"""Gets child instances of PceUpdateSrMetricSubObjectList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceUpdateSrMetricSubObjectList will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrmetricsubobjectlist.PceUpdateSrMetricSubObjectList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrmetricsubobjectlist import PceUpdateSrMetricSubObjectList
		return self._select(PceUpdateSrMetricSubObjectList(self), locals())

	@property
	def Bandwidth(self):
		"""Bandwidth (bps)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidth')

	@property
	def ConfigureBandwidth(self):
		"""Configure Bandwidth

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureBandwidth')

	@property
	def ConfigureEro(self):
		"""Configure ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureEro')

	@property
	def ConfigureLsp(self):
		"""Configure LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureLsp')

	@property
	def ConfigureLspa(self):
		"""Configure LSPA

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureLspa')

	@property
	def ConfigureMetric(self):
		"""Configure Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureMetric')

	@property
	def ExcludeAny(self):
		"""Exclude Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('excludeAny')

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
	def IncludeSrp(self):
		"""Indicates whether SRP object will be included in a PCInitiate message. All other attributes in sub-tab-SRP would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSrp')

	@property
	def IncludeSymbolicPathName(self):
		"""Indicates if Symbolic-Path-Name TLV is to be included in PCUpate trigger message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSymbolicPathName')

	@property
	def LocalProtection(self):
		"""Local Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtection')

	@property
	def NumberOfEroSubObjects(self):
		"""Value that indicates the number of ERO Sub Objects to be configured.

		Returns:
			number
		"""
		return self._get_attribute('numberOfEroSubObjects')
	@NumberOfEroSubObjects.setter
	def NumberOfEroSubObjects(self, value):
		self._set_attribute('numberOfEroSubObjects', value)

	@property
	def NumberOfMetricSubObjects(self):
		"""Value that indicates the number of Metric Objects to be configured.

		Returns:
			number
		"""
		return self._get_attribute('numberOfMetricSubObjects')
	@NumberOfMetricSubObjects.setter
	def NumberOfMetricSubObjects(self, value):
		self._set_attribute('numberOfMetricSubObjects', value)

	@property
	def OverrideSrpId(self):
		"""Indicates whether SRP object will be included in a PCUpdate trigger parameters. All other attributes in sub-tab-SRP would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('overrideSrpId')

	@property
	def PceTriggersChoiceList(self):
		"""Based on options selected, IxNetwork sends information to PCPU and refreshes the statistical data in the corresponding tab of Learned Information

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pceTriggersChoiceList')

	@property
	def SetupPriority(self):
		"""Setup Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setupPriority')

	@property
	def SrpId(self):
		"""The SRP object is used to correlate between initiation requests sent by the PCE and the error reports and state reports sent by the PCC. This number is unique per PCEP session and is incremented per initiation.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srpId')

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

	def SendPcUpdate(self, Arg2):
		"""Executes the sendPcUpdate operation on the server.

		Counts property changes created by the user.

		Args:
			Arg2 (list(number)): List of indices into the learned information corresponding to trigger data.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPcUpdate', payload=locals(), response_object=None)
