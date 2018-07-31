from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class View(Base):
	"""The root node for all statistics view per 5.40 SV API.
	"""

	_SDM_NAME = 'view'

	def __init__(self, parent):
		super(View, self).__init__(parent)

	def AdvancedCVFilters(self, AvailableFilterOptions=None, AvailableGroupingOptions=None, Caption=None, Expression=None, Grouping=None, Protocol=None, SortingStats=None):
		"""Gets child instances of AdvancedCVFilters from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AdvancedCVFilters will be returned.

		Args:
			AvailableFilterOptions (str): Returns a list of all the statistics and the operations available for filtering. Note- A protocol and a grouping must be set in order for this to work.
			AvailableGroupingOptions (str): Returns all the grouping options available. Note - A protocol must be set in order for this to work.
			Caption (str): Sets a name for the filter.
			Expression (str): Specifies the filter body. This is a string that must have the specific format. This can be empty or no filter.The available operations and statistics can be obtained from availableFilterOptions.
			Grouping (str): Sets a grouping for the filter.
			Protocol (str): Sets a protocol for the filter.
			SortingStats (str): Specifies the list of statistics by which the view is sorted.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.advancedcvfilters.advancedcvfilters.AdvancedCVFilters))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.advancedcvfilters.advancedcvfilters import AdvancedCVFilters
		return self._select(AdvancedCVFilters(self), locals())

	def add_AdvancedCVFilters(self, Caption="", Expression="", Grouping="", Protocol="", SortingStats=""):
		"""Adds a child instance of AdvancedCVFilters on the server.

		Args:
			Caption (str): Sets a name for the filter.
			Expression (str): Specifies the filter body. This is a string that must have the specific format. This can be empty or no filter.The available operations and statistics can be obtained from availableFilterOptions.
			Grouping (str): Sets a grouping for the filter.
			Protocol (str): Sets a protocol for the filter.
			SortingStats (str): Specifies the list of statistics by which the view is sorted.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.advancedcvfilters.advancedcvfilters.AdvancedCVFilters)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.advancedcvfilters.advancedcvfilters import AdvancedCVFilters
		return self._create(AdvancedCVFilters(self), locals())

	def AvailableAdvancedFilters(self, Expression=None, Name=None):
		"""Gets child instances of AvailableAdvancedFilters from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailableAdvancedFilters will be returned.

		Args:
			Expression (str): Allows you to get the filter expression or the body from the id.
			Name (str): Allows you to get the filter name from the id.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableadvancedfilters.availableadvancedfilters.AvailableAdvancedFilters))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableadvancedfilters.availableadvancedfilters import AvailableAdvancedFilters
		return self._select(AvailableAdvancedFilters(self), locals())

	def AvailablePortFilter(self, Name=None):
		"""Gets child instances of AvailablePortFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailablePortFilter will be returned.

		Args:
			Name (str): The name of the port filter.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableportfilter.availableportfilter.AvailablePortFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableportfilter.availableportfilter import AvailablePortFilter
		return self._select(AvailablePortFilter(self), locals())

	def AvailableProtocolFilter(self, Name=None):
		"""Gets child instances of AvailableProtocolFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailableProtocolFilter will be returned.

		Args:
			Name (str): The unique identifier of the object.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolfilter.availableprotocolfilter.AvailableProtocolFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolfilter.availableprotocolfilter import AvailableProtocolFilter
		return self._select(AvailableProtocolFilter(self), locals())

	def AvailableProtocolStackFilter(self, Name=None):
		"""Gets child instances of AvailableProtocolStackFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailableProtocolStackFilter will be returned.

		Args:
			Name (str): The name of the protocol stack ranges.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolstackfilter.availableprotocolstackfilter.AvailableProtocolStackFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolstackfilter.availableprotocolstackfilter import AvailableProtocolStackFilter
		return self._select(AvailableProtocolStackFilter(self), locals())

	def AvailableStatisticFilter(self, Caption=None):
		"""Gets child instances of AvailableStatisticFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailableStatisticFilter will be returned.

		Args:
			Caption (str): Name of the statistic.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availablestatisticfilter.availablestatisticfilter.AvailableStatisticFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availablestatisticfilter.availablestatisticfilter import AvailableStatisticFilter
		return self._select(AvailableStatisticFilter(self), locals())

	def AvailableTrackingFilter(self, Name=None, TrackingType=None, ValueType=None):
		"""Gets child instances of AvailableTrackingFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailableTrackingFilter will be returned.

		Args:
			Name (str): Displays the name of the tracking filter.
			TrackingType (str): Indicates the tracking type.
			ValueType (str): Value of tracking to be matched based on operator.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrackingfilter.availabletrackingfilter.AvailableTrackingFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrackingfilter.availabletrackingfilter import AvailableTrackingFilter
		return self._select(AvailableTrackingFilter(self), locals())

	def AvailableTrafficItemFilter(self, Name=None):
		"""Gets child instances of AvailableTrafficItemFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailableTrafficItemFilter will be returned.

		Args:
			Name (str): Displays the name of the traffic item filter.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrafficitemfilter.availabletrafficitemfilter.AvailableTrafficItemFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrafficitemfilter.availabletrafficitemfilter import AvailableTrafficItemFilter
		return self._select(AvailableTrafficItemFilter(self), locals())

	@property
	def Data(self):
		"""Returns the one and only one Data object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.data.Data)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.data import Data
		return self._read(Data(self), None)

	def DrillDown(self, TargetDrillDownOption=None):
		"""Gets child instances of DrillDown from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DrillDown will be returned.

		Args:
			TargetDrillDownOption (str): Sets the drill down option attribute to the drilldown object. It is one of the items in the list returned at 2.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.drilldown.DrillDown))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.drilldown import DrillDown
		return self._select(DrillDown(self), locals())

	def add_DrillDown(self, TargetDrillDownOption="", TargetRowFilter=None, TargetRowIndex="-1"):
		"""Adds a child instance of DrillDown on the server.

		Args:
			TargetDrillDownOption (str): Sets the drill down option attribute to the drilldown object. It is one of the items in the list returned at 2.
			TargetRowFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTargetRowFilters)): Sets the row (from the view) that will be used to perform the drill-down. This is done by using one of the filters provided by availableTargetRowFilters
			TargetRowIndex (number): Sets the attribute targetRowIndex to the drill down object. This is the row (from the view) that will be used to perform the drill-down.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.drilldown.DrillDown)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.drilldown import DrillDown
		return self._create(DrillDown(self), locals())

	@property
	def FormulaCatalog(self):
		"""Returns the one and only one FormulaCatalog object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacatalog.FormulaCatalog)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacatalog import FormulaCatalog
		return self._read(FormulaCatalog(self), None)

	@property
	def InnerGlobalStats(self):
		"""Returns the one and only one InnerGlobalStats object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.innerglobalstats.innerglobalstats.InnerGlobalStats)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.innerglobalstats.innerglobalstats import InnerGlobalStats
		return self._read(InnerGlobalStats(self), None)

	def Layer23NextGenProtocolFilter(self, AdvancedFilterName=None):
		"""Gets child instances of Layer23NextGenProtocolFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23NextGenProtocolFilter will be returned.

		Args:
			AdvancedFilterName (str): Selects an advanced filter from the ones available in the selected drill down view.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.layer23nextgenprotocolfilter.Layer23NextGenProtocolFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.layer23nextgenprotocolfilter import Layer23NextGenProtocolFilter
		return self._select(Layer23NextGenProtocolFilter(self), locals())

	def add_Layer23NextGenProtocolFilter(self, AdvancedCVFilter=None, AdvancedFilterName="", AggregationType="perPort", PortFilterIds=None, ProtocolFilterIds=None):
		"""Adds a child instance of Layer23NextGenProtocolFilter on the server.

		Args:
			AdvancedCVFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=advancedCVFilters)): Sets the advanced filter for a custom view. Note: To change the filter on an existing view, you must first disable it.
			AdvancedFilterName (str): Selects an advanced filter from the ones available in the selected drill down view.
			AggregationType (str(perPort|perSession)): Signifies the type of aggregation of next gen protocols
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Filters the port IDs
			ProtocolFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])): Filters the protocol IDs

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.layer23nextgenprotocolfilter.Layer23NextGenProtocolFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.layer23nextgenprotocolfilter import Layer23NextGenProtocolFilter
		return self._create(Layer23NextGenProtocolFilter(self), locals())

	def Layer23ProtocolAuthAccessFilter(self):
		"""Gets child instances of Layer23ProtocolAuthAccessFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23ProtocolAuthAccessFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolauthaccessfilter.layer23protocolauthaccessfilter.Layer23ProtocolAuthAccessFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolauthaccessfilter.layer23protocolauthaccessfilter import Layer23ProtocolAuthAccessFilter
		return self._select(Layer23ProtocolAuthAccessFilter(self), locals())

	def add_Layer23ProtocolAuthAccessFilter(self, PortFilterIds=None, ProtocolFilterIds=None):
		"""Adds a child instance of Layer23ProtocolAuthAccessFilter on the server.

		Args:
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Ports that have been filtered.
			ProtocolFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])): Protocols that have been filtered.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolauthaccessfilter.layer23protocolauthaccessfilter.Layer23ProtocolAuthAccessFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolauthaccessfilter.layer23protocolauthaccessfilter import Layer23ProtocolAuthAccessFilter
		return self._create(Layer23ProtocolAuthAccessFilter(self), locals())

	def Layer23ProtocolPortFilter(self):
		"""Gets child instances of Layer23ProtocolPortFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23ProtocolPortFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolportfilter.layer23protocolportfilter.Layer23ProtocolPortFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolportfilter.layer23protocolportfilter import Layer23ProtocolPortFilter
		return self._select(Layer23ProtocolPortFilter(self), locals())

	def add_Layer23ProtocolPortFilter(self, PortFilterIds=None):
		"""Adds a child instance of Layer23ProtocolPortFilter on the server.

		Args:
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolportfilter.layer23protocolportfilter.Layer23ProtocolPortFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolportfilter.layer23protocolportfilter import Layer23ProtocolPortFilter
		return self._create(Layer23ProtocolPortFilter(self), locals())

	def Layer23ProtocolRoutingFilter(self):
		"""Gets child instances of Layer23ProtocolRoutingFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23ProtocolRoutingFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolroutingfilter.layer23protocolroutingfilter.Layer23ProtocolRoutingFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolroutingfilter.layer23protocolroutingfilter import Layer23ProtocolRoutingFilter
		return self._select(Layer23ProtocolRoutingFilter(self), locals())

	def add_Layer23ProtocolRoutingFilter(self, PortFilterIds=None, ProtocolFilterIds=None):
		"""Adds a child instance of Layer23ProtocolRoutingFilter on the server.

		Args:
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Ports that have been filtered.
			ProtocolFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])): Protocols that have been filtered.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolroutingfilter.layer23protocolroutingfilter.Layer23ProtocolRoutingFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolroutingfilter.layer23protocolroutingfilter import Layer23ProtocolRoutingFilter
		return self._create(Layer23ProtocolRoutingFilter(self), locals())

	def Layer23ProtocolStackFilter(self):
		"""Gets child instances of Layer23ProtocolStackFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23ProtocolStackFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolstackfilter.layer23protocolstackfilter.Layer23ProtocolStackFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolstackfilter.layer23protocolstackfilter import Layer23ProtocolStackFilter
		return self._select(Layer23ProtocolStackFilter(self), locals())

	def add_Layer23ProtocolStackFilter(self, DrilldownType="perRange", NumberOfResults="50", ProtocolStackFilterId=None, SortAscending="False", SortingStatistic=None):
		"""Adds a child instance of Layer23ProtocolStackFilter on the server.

		Args:
			DrilldownType (str(perRange|perSession)): Emulates perRange or perSession view based on the option seleted.
			NumberOfResults (number): Number of traffic flows to be displayed.
			ProtocolStackFilterId (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolStackFilter])): Selected protocol stack filters from the availableProtocolStackFilter list.
			SortAscending (bool): Sets the display order of the view.
			SortingStatistic (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=statistic)): The reference statistic by which the data will be sorted in created SV.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolstackfilter.layer23protocolstackfilter.Layer23ProtocolStackFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolstackfilter.layer23protocolstackfilter import Layer23ProtocolStackFilter
		return self._create(Layer23ProtocolStackFilter(self), locals())

	def Layer23TrafficFlowDetectiveFilter(self):
		"""Gets child instances of Layer23TrafficFlowDetectiveFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23TrafficFlowDetectiveFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.layer23trafficflowdetectivefilter.Layer23TrafficFlowDetectiveFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.layer23trafficflowdetectivefilter import Layer23TrafficFlowDetectiveFilter
		return self._select(Layer23TrafficFlowDetectiveFilter(self), locals())

	def add_Layer23TrafficFlowDetectiveFilter(self, DeadFlowsThreshold="10", FlowFilterType="allFlows", PortFilterIds=None, ShowEgressFlows="False", TrafficItemFilterId=None, TrafficItemFilterIds=None):
		"""Adds a child instance of Layer23TrafficFlowDetectiveFilter on the server.

		Args:
			DeadFlowsThreshold (number): Threshold in seconds after which the flows are declared dead if there are no packets received for a specified number of seconds. This is a global attibute and hence the latest value entered takes precedence over previous values in all the custom views.
			FlowFilterType (str(allFlows|deadFlows|liveFlows)): Indicates the flow detective filter settings.
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.
			ShowEgressFlows (bool): NOT DEFINED
			TrafficItemFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter)): Selected traffic flow detective filter from the availableTrafficItemFilter list.
			TrafficItemFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])): Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.layer23trafficflowdetectivefilter.Layer23TrafficFlowDetectiveFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.layer23trafficflowdetectivefilter import Layer23TrafficFlowDetectiveFilter
		return self._create(Layer23TrafficFlowDetectiveFilter(self), locals())

	def Layer23TrafficFlowFilter(self):
		"""Gets child instances of Layer23TrafficFlowFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23TrafficFlowFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.layer23trafficflowfilter.Layer23TrafficFlowFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.layer23trafficflowfilter import Layer23TrafficFlowFilter
		return self._select(Layer23TrafficFlowFilter(self), locals())

	def add_Layer23TrafficFlowFilter(self, AggregatedAcrossPorts="False", EgressLatencyBinDisplayOption="none", PortFilterIds=None, TrafficItemFilterId=None, TrafficItemFilterIds=None):
		"""Adds a child instance of Layer23TrafficFlowFilter on the server.

		Args:
			AggregatedAcrossPorts (bool): If true, displays aggregated stat value across ports selected by portFilterIds. Default = false
			EgressLatencyBinDisplayOption (str(none|showEgressFlatView|showEgressRows|showLatencyBinStats)): Emulates Latency Bin SV or Egress Tracking SV.
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.
			TrafficItemFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter)): Selected traffic item filter from the availableTrafficItemFilter list.
			TrafficItemFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])): Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.layer23trafficflowfilter.Layer23TrafficFlowFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.layer23trafficflowfilter import Layer23TrafficFlowFilter
		return self._create(Layer23TrafficFlowFilter(self), locals())

	def Layer23TrafficItemFilter(self):
		"""Gets child instances of Layer23TrafficItemFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23TrafficItemFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficitemfilter.layer23trafficitemfilter.Layer23TrafficItemFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficitemfilter.layer23trafficitemfilter import Layer23TrafficItemFilter
		return self._select(Layer23TrafficItemFilter(self), locals())

	def add_Layer23TrafficItemFilter(self, TrafficItemFilterIds=None):
		"""Adds a child instance of Layer23TrafficItemFilter on the server.

		Args:
			TrafficItemFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])): Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficitemfilter.layer23trafficitemfilter.Layer23TrafficItemFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficitemfilter.layer23trafficitemfilter import Layer23TrafficItemFilter
		return self._create(Layer23TrafficItemFilter(self), locals())

	def Layer23TrafficPortFilter(self):
		"""Gets child instances of Layer23TrafficPortFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer23TrafficPortFilter will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficportfilter.layer23trafficportfilter.Layer23TrafficPortFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficportfilter.layer23trafficportfilter import Layer23TrafficPortFilter
		return self._select(Layer23TrafficPortFilter(self), locals())

	def add_Layer23TrafficPortFilter(self, PortFilterIds=None):
		"""Adds a child instance of Layer23TrafficPortFilter on the server.

		Args:
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Selected port filters from the availablePortFilter list.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficportfilter.layer23trafficportfilter.Layer23TrafficPortFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficportfilter.layer23trafficportfilter import Layer23TrafficPortFilter
		return self._create(Layer23TrafficPortFilter(self), locals())

	def Layer47AppLibraryTrafficFilter(self, AdvancedFilterName=None):
		"""Gets child instances of Layer47AppLibraryTrafficFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Layer47AppLibraryTrafficFilter will be returned.

		Args:
			AdvancedFilterName (str): Specifies an advanced filter from the ones available in the selected drill down view.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.layer47applibrarytrafficfilter.Layer47AppLibraryTrafficFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.layer47applibrarytrafficfilter import Layer47AppLibraryTrafficFilter
		return self._select(Layer47AppLibraryTrafficFilter(self), locals())

	def add_Layer47AppLibraryTrafficFilter(self, AdvancedFilterName="", TopxEnabled=None, TopxValue="0"):
		"""Adds a child instance of Layer47AppLibraryTrafficFilter on the server.

		Args:
			AdvancedFilterName (str): Specifies an advanced filter from the ones available in the selected drill down view.
			TopxEnabled (bool): The view only shows the number of rows specified by TopXValue. If the view is OnDemand, it will become RealTime.
			TopxValue (number): The number of rows to be shown when TopXEnabled is set to true.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.layer47applibrarytrafficfilter.Layer47AppLibraryTrafficFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.layer47applibrarytrafficfilter import Layer47AppLibraryTrafficFilter
		return self._create(Layer47AppLibraryTrafficFilter(self), locals())

	@property
	def Page(self):
		"""Returns the one and only one Page object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.page.Page)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.page import Page
		return self._read(Page(self), None)

	def Statistic(self, Caption=None, DefaultCaption=None):
		"""Gets child instances of Statistic from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Statistic will be returned.

		Args:
			Caption (str): 
			DefaultCaption (str): 

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.statistic.statistic.Statistic))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.statistic.statistic import Statistic
		return self._select(Statistic(self), locals())

	@property
	def AutoRefresh(self):
		"""If true, automatically refreshes the statistics values. Default = true

		Returns:
			bool
		"""
		return self._get_attribute('autoRefresh')
	@AutoRefresh.setter
	def AutoRefresh(self, value):
		self._set_attribute('autoRefresh', value)

	@property
	def AutoUpdate(self):
		"""If true, automatically refreshes the statistics values. Default = true

		Returns:
			bool
		"""
		return self._get_attribute('autoUpdate')
	@AutoUpdate.setter
	def AutoUpdate(self, value):
		self._set_attribute('autoUpdate', value)

	@property
	def AvailableStatsSelectorColumns(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('availableStatsSelectorColumns')

	@property
	def Caption(self):
		"""This is the name that will appear in the GUI stats view window header or in the added view tree from tcl. The caption must be unique.

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def CsvFileName(self):
		"""Specifies the file name which is used by the CSV Logging feature. The default value is the caption of the view.

		Returns:
			str
		"""
		return self._get_attribute('csvFileName')
	@CsvFileName.setter
	def CsvFileName(self, value):
		self._set_attribute('csvFileName', value)

	@property
	def EnableCsvLogging(self):
		"""If the CSV Logging feature is enabled the statistics values from a view will be written in a comma separated value format.

		Returns:
			bool
		"""
		return self._get_attribute('enableCsvLogging')
	@EnableCsvLogging.setter
	def EnableCsvLogging(self, value):
		self._set_attribute('enableCsvLogging', value)

	@property
	def Enabled(self):
		"""If true, enables the view that is created from the tcl script.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EnabledStatsSelectorColumns(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledStatsSelectorColumns')
	@EnabledStatsSelectorColumns.setter
	def EnabledStatsSelectorColumns(self, value):
		self._set_attribute('enabledStatsSelectorColumns', value)

	@property
	def PageTimeout(self):
		"""The statistics view page is timed out based on the time specified. default = 25,000 ms

		Returns:
			number
		"""
		return self._get_attribute('pageTimeout')
	@PageTimeout.setter
	def PageTimeout(self, value):
		self._set_attribute('pageTimeout', value)

	@property
	def ReadOnly(self):
		"""The default views created by the application will have this attribute set to false. Tcl SV created by user has this value set to true. Based on this attribute value, the user is allowed to modify the SV attributes.

		Returns:
			bool
		"""
		return self._get_attribute('readOnly')

	@property
	def TimeSeries(self):
		"""If false, then it displays non-timeseries grid views. If true, displays, timeseries line chart view. default = false (non-timeseries)

		Returns:
			bool
		"""
		return self._get_attribute('timeSeries')
	@TimeSeries.setter
	def TimeSeries(self, value):
		self._set_attribute('timeSeries', value)

	@property
	def TreeViewNodeName(self):
		"""Displays the name of the tree view node.

		Returns:
			str
		"""
		return self._get_attribute('treeViewNodeName')
	@TreeViewNodeName.setter
	def TreeViewNodeName(self, value):
		self._set_attribute('treeViewNodeName', value)

	@property
	def Type(self):
		"""The type of view the user wants to create from tcl.

		Returns:
			str(layer23NextGenProtocol|layer23ProtocolAuthAccess|layer23ProtocolPort|layer23ProtocolRouting|layer23ProtocolStack|layer23TrafficFlow|layer23TrafficFlowDetective|layer23TrafficItem|layer23TrafficPort|layer47AppLibraryTraffic|sVReadOnly)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def TypeDescription(self):
		"""If true, desribes the type

		Returns:
			str
		"""
		return self._get_attribute('typeDescription')

	@property
	def ViewCategory(self):
		"""Returns the category of the view based on the type of statistics displayed by the view.

		Returns:
			str(ClassicProtocol|L23Traffic|L47Traffic|Mixed|NextGenProtocol|PerSession|Unknown)
		"""
		return self._get_attribute('viewCategory')

	@property
	def Visible(self):
		"""If true, displays the custom created tcl SVs in the SV tree under TCL Views node.

		Returns:
			bool
		"""
		return self._get_attribute('visible')
	@Visible.setter
	def Visible(self, value):
		self._set_attribute('visible', value)

	def remove(self):
		"""Deletes a child instance of View on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ExportData(self, FilePathName):
		"""Executes the exportData operation on the server.

		Exports the data seen in a view to a file. Supported formats are .html, .xml, .xls and .txt.

		Args:
			FilePathName (str): The path where the exported file should be written.

		Returns:
			str: This can be either a success message or a description of the problem if any error occurred.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('exportData', payload=locals(), response_object=None)

	def GetColumnValues(self, Arg2):
		"""Executes the getColumnValues operation on the server.

		Retrieves the requested column values.

		Args:
			Arg2 (str): The name of the column for which to retrieve statistics.

		Returns:
			dict(arg1:list[str],arg2:str): An array with the values retrieved.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getColumnValues', payload=locals(), response_object=None)

	def GetResultsPath(self):
		"""Executes the getResultsPath operation on the server.

		Gets the path where the results for the current tests are stored.

		Returns:
			str: The results path.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getResultsPath', payload=locals(), response_object=None)

	def GetRowValues(self, Arg2):
		"""Executes the getRowValues operation on the server.

		Retrieves the requested row values.

		Args:
			Arg2 (str): The label identifying the row for which to retrieve statistics. It is formed from the values of the row label columns concatenated using | delimiter. Row label columns appear with orange or yellow names in the view.

		Returns:
			dict(arg1:list[str],arg2:str): An array with the values retrieved.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getRowValues', payload=locals(), response_object=None)

	def GetValue(self, Arg2, Arg3):
		"""Executes the getValue operation on the server.

		Retrieves the requested statistical data.

		Args:
			Arg2 (str): The label identifying the row for which to retrieve statistics. It is formed from the values of the row label columns concatenated using | delimiter. Row label columns appear with orange or yellow names in the view.
			Arg3 (str): The name of the column for which to retrieve statistics.

		Returns:
			str: The retrieved value.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getValue', payload=locals(), response_object=None)

	def Refresh(self):
		"""Executes the refresh operation on the server.

		Refreshes the existing values in the view with the new values. If the view is NGPF on demand, the refresh will get new values for all NGPF on demand views.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('refresh', payload=locals(), response_object=None)

	def RestoreToDefaults(self):
		"""Executes the restoreToDefaults operation on the server.

		NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('restoreToDefaults', payload=locals(), response_object=None)
