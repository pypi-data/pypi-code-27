from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistics(Base):
	"""Generates test statistics for IxNetwork.
	"""

	_SDM_NAME = 'statistics'

	def __init__(self, parent):
		super(Statistics, self).__init__(parent)

	@property
	def AutoRefresh(self):
		"""Returns the one and only one AutoRefresh object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.autorefresh.autorefresh.AutoRefresh)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.autorefresh.autorefresh import AutoRefresh
		return self._read(AutoRefresh(self), None)

	@property
	def CsvSnapshot(self):
		"""Returns the one and only one CsvSnapshot object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.csvsnapshot.csvsnapshot.CsvSnapshot)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.csvsnapshot.csvsnapshot import CsvSnapshot
		return self._read(CsvSnapshot(self), None)

	@property
	def Ixreporter(self):
		"""Returns the one and only one Ixreporter object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.ixreporter.Ixreporter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.ixreporter import Ixreporter
		return self._read(Ixreporter(self), None)

	@property
	def MeasurementMode(self):
		"""Returns the one and only one MeasurementMode object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.measurementmode.measurementmode.MeasurementMode)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.measurementmode.measurementmode import MeasurementMode
		return self._read(MeasurementMode(self), None)

	@property
	def RawData(self):
		"""Returns the one and only one RawData object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.rawdata.rawdata.RawData)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.rawdata.rawdata import RawData
		return self._read(RawData(self), None)

	def StatRequest(self):
		"""Gets child instances of StatRequest from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of StatRequest will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.statrequest.StatRequest))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.statrequest import StatRequest
		return self._select(StatRequest(self), locals())

	def add_StatRequest(self, Filter=None, FilterItems=None, MaxWaitTime="0", Source=None, Stats=None):
		"""Adds a child instance of StatRequest on the server.

		Args:
			Filter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=*)): The Statistics filter
			FilterItems (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])): A list of filter items.
			MaxWaitTime (number): Value indicates the maximum wait time.
			Source (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=*)): The source for the statistical data.
			Stats (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=*],arg2:str[average|averageRate|countDistinct|delta|divSum|first|intervalAverage|max|maxRate|min|minRate|none|positiveAverageRate|positiveMaxRate|positiveMinRate|positiveRate|rate|runStateAgg|runStateAggIgnoreRamp|standardDeviation|sum|vectorMax|vectorMin|weightedAverage]))): The statistics displayed.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.statrequest.StatRequest)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.statrequest import StatRequest
		return self._create(StatRequest(self), locals())

	def View(self, Caption=None, CsvFileName=None, TreeViewNodeName=None, TypeDescription=None):
		"""Gets child instances of View from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of View will be returned.

		Args:
			Caption (str): This is the name that will appear in the GUI stats view window header or in the added view tree from tcl. The caption must be unique.
			CsvFileName (str): Specifies the file name which is used by the CSV Logging feature. The default value is the caption of the view.
			TreeViewNodeName (str): Displays the name of the tree view node.
			TypeDescription (str): If true, desribes the type

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.view.View))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.view import View
		return self._select(View(self), locals())

	def add_View(self, AutoRefresh="False", AutoUpdate="True", Caption="", CsvFileName="", EnableCsvLogging="False", Enabled="False", EnabledStatsSelectorColumns=None, PageTimeout="25000", TimeSeries="False", TreeViewNodeName="views\tcl views", Type="sVReadOnly", Visible="False"):
		"""Adds a child instance of View on the server.

		Args:
			AutoRefresh (bool): If true, automatically refreshes the statistics values. Default = true
			AutoUpdate (bool): If true, automatically refreshes the statistics values. Default = true
			Caption (str): This is the name that will appear in the GUI stats view window header or in the added view tree from tcl. The caption must be unique.
			CsvFileName (str): Specifies the file name which is used by the CSV Logging feature. The default value is the caption of the view.
			EnableCsvLogging (bool): If the CSV Logging feature is enabled the statistics values from a view will be written in a comma separated value format.
			Enabled (bool): If true, enables the view that is created from the tcl script.
			EnabledStatsSelectorColumns (list(str)): NOT DEFINED
			PageTimeout (number): The statistics view page is timed out based on the time specified. default = 25,000 ms
			TimeSeries (bool): If false, then it displays non-timeseries grid views. If true, displays, timeseries line chart view. default = false (non-timeseries)
			TreeViewNodeName (str): Displays the name of the tree view node.
			Type (str(layer23NextGenProtocol|layer23ProtocolAuthAccess|layer23ProtocolPort|layer23ProtocolRouting|layer23ProtocolStack|layer23TrafficFlow|layer23TrafficFlowDetective|layer23TrafficItem|layer23TrafficPort|layer47AppLibraryTraffic|sVReadOnly)): The type of view the user wants to create from tcl.
			Visible (bool): If true, displays the custom created tcl SVs in the SV tree under TCL Views node.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.view.View)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.view import View
		return self._create(View(self), locals())

	@property
	def AdditionalFcoeStat1(self):
		"""Signifies additional FCOE stat 1

		Returns:
			str(fcoeInvalidDelimiter|fcoeInvalidFrames|fcoeInvalidSize|fcoeNormalSizeBadFcCRC|fcoeNormalSizeGoodFcCRC|fcoeUndersizeBadFcCRC|fcoeUndersizeGoodFcCRC|fcoeValidFrames)
		"""
		return self._get_attribute('additionalFcoeStat1')
	@AdditionalFcoeStat1.setter
	def AdditionalFcoeStat1(self, value):
		self._set_attribute('additionalFcoeStat1', value)

	@property
	def AdditionalFcoeStat2(self):
		"""Sets the additional FCoE shared stats.

		Returns:
			str(fcoeInvalidDelimiter|fcoeInvalidFrames|fcoeInvalidSize|fcoeNormalSizeBadFcCRC|fcoeNormalSizeGoodFcCRC|fcoeUndersizeBadFcCRC|fcoeUndersizeGoodFcCRC|fcoeValidFrames)
		"""
		return self._get_attribute('additionalFcoeStat2')
	@AdditionalFcoeStat2.setter
	def AdditionalFcoeStat2(self, value):
		self._set_attribute('additionalFcoeStat2', value)

	@property
	def CsvFilePath(self):
		"""Sets the CSV file path.

		Returns:
			str
		"""
		return self._get_attribute('csvFilePath')
	@CsvFilePath.setter
	def CsvFilePath(self, value):
		self._set_attribute('csvFilePath', value)

	@property
	def CsvLogPollIntervalMultiplier(self):
		"""Used to specify the time interval between log polling events.

		Returns:
			number
		"""
		return self._get_attribute('csvLogPollIntervalMultiplier')
	@CsvLogPollIntervalMultiplier.setter
	def CsvLogPollIntervalMultiplier(self, value):
		self._set_attribute('csvLogPollIntervalMultiplier', value)

	@property
	def DataStorePollingIntervalMultiplier(self):
		"""The data store polling interval value is the result of the data store polling interval multiplier value multiplied by the polling interval value set for the test.

		Returns:
			number
		"""
		return self._get_attribute('dataStorePollingIntervalMultiplier')
	@DataStorePollingIntervalMultiplier.setter
	def DataStorePollingIntervalMultiplier(self, value):
		self._set_attribute('dataStorePollingIntervalMultiplier', value)

	@property
	def EnableAutoDataStore(self):
		"""If this option is enabled, StatViewer writes the statistical values in binary format for all test results in a view. The test results is converted into a binary array and written to a file.

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoDataStore')
	@EnableAutoDataStore.setter
	def EnableAutoDataStore(self, value):
		self._set_attribute('enableAutoDataStore', value)

	@property
	def EnableCsvLogging(self):
		"""If this option is enabled, StatViewer writes the statistical values in comma separated value format for all test results in a view.

		Returns:
			bool
		"""
		return self._get_attribute('enableCsvLogging')
	@EnableCsvLogging.setter
	def EnableCsvLogging(self, value):
		self._set_attribute('enableCsvLogging', value)

	@property
	def EnableDataCenterSharedStats(self):
		"""If true, enables statistics for Data Center.

		Returns:
			bool
		"""
		return self._get_attribute('enableDataCenterSharedStats')
	@EnableDataCenterSharedStats.setter
	def EnableDataCenterSharedStats(self, value):
		self._set_attribute('enableDataCenterSharedStats', value)

	@property
	def GuardrailEnabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('guardrailEnabled')
	@GuardrailEnabled.setter
	def GuardrailEnabled(self, value):
		self._set_attribute('guardrailEnabled', value)

	@property
	def MaxNumberOfStatsPerCustomGraph(self):
		"""The data store polling interval value is the result of the data store polling interval multiplier value multiplied by the polling interval value set for the test.

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfStatsPerCustomGraph')
	@MaxNumberOfStatsPerCustomGraph.setter
	def MaxNumberOfStatsPerCustomGraph(self, value):
		self._set_attribute('maxNumberOfStatsPerCustomGraph', value)

	@property
	def PollInterval(self):
		"""The multiplier used with the frequency (2 seconds), to set the time interval between polling events. The default is 1 (1 times 2 seconds = 2 seconds).

		Returns:
			number
		"""
		return self._get_attribute('pollInterval')
	@PollInterval.setter
	def PollInterval(self, value):
		self._set_attribute('pollInterval', value)

	@property
	def TimeSynchronization(self):
		"""The statistics polling time can be configured to get synchronized with the system clock or reset it to 0 when the test starts. The time synchronization behavior can be changed only before the test starts and does not apply during test run.

		Returns:
			str(syncTimeToSystemClock|syncTimeToTestStart)
		"""
		return self._get_attribute('timeSynchronization')
	@TimeSynchronization.setter
	def TimeSynchronization(self, value):
		self._set_attribute('timeSynchronization', value)

	@property
	def TimestampPrecision(self):
		"""The timestamp precision allows you to change the timestamp precision from microseconds to nanoseconds for specific StatViewer statistics and features. The timestamp precision can be set to have the fstatistics display values with decimals ranging from 0 to 9.

		Returns:
			number
		"""
		return self._get_attribute('timestampPrecision')
	@TimestampPrecision.setter
	def TimestampPrecision(self, value):
		self._set_attribute('timestampPrecision', value)

	@property
	def UgsTcpPort(self):
		"""Used to specify the UGS TCP port.

		Returns:
			number
		"""
		return self._get_attribute('ugsTcpPort')

	def CheckViewTreeGroupExists(self, Arg2):
		"""Executes the checkViewTreeGroupExists operation on the server.

		This command verifies that the specified group name exists in the StatViewer tree.

		Args:
			Arg2 (str): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('checkViewTreeGroupExists', payload=locals(), response_object=None)

	def DockStatViewer(self):
		"""Executes the dockStatViewer operation on the server.

		NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('dockStatViewer', payload=locals(), response_object=None)

	def GetPGIDList(self, Arg2, Arg3):
		"""Executes the getPGIDList operation on the server.

		NOT DEFINED

		Args:
			Arg2 (str): NOT DEFINED
			Arg3 (str): NOT DEFINED

		Returns:
			list(str): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPGIDList', payload=locals(), response_object=None)

	def GetStatsFooters(self, Arg2, Arg3, Arg4):
		"""Executes the getStatsFooters operation on the server.

		This command retrieves Stats Footers from traffic stats.

		Args:
			Arg2 (str): NOT DEFINED
			Arg3 (str): NOT DEFINED
			Arg4 (str): NOT DEFINED

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getStatsFooters', payload=locals(), response_object=None)
