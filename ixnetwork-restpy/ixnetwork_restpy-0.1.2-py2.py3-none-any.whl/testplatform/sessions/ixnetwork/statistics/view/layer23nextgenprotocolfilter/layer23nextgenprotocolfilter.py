from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23NextGenProtocolFilter(Base):
	"""Describes the filter of next gen protocols for layer 2 and layer 3
	"""

	_SDM_NAME = 'layer23NextGenProtocolFilter'

	def __init__(self, parent):
		super(Layer23NextGenProtocolFilter, self).__init__(parent)

	def AdvancedFilter(self, Expression=None, Name=None, SortingStats=None):
		"""Gets child instances of AdvancedFilter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AdvancedFilter will be returned.

		Args:
			Expression (str): Specifies the filter body. This is a string that must have a specific format.This can be empty (no filter). The available operations and statistics can be obtained from availableAdvancedFilterOptions.
			Name (str): Specifies the filter name. It must be unique per view.
			SortingStats (str): Specifies the list of statistics by which the view will be sorted.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.advancedfilter.advancedfilter.AdvancedFilter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.advancedfilter.advancedfilter import AdvancedFilter
		return self._select(AdvancedFilter(self), locals())

	def add_AdvancedFilter(self, Expression="", Name="", SortingStats="", TrackingFilterId=None):
		"""Adds a child instance of AdvancedFilter on the server.

		Args:
			Expression (str): Specifies the filter body. This is a string that must have a specific format.This can be empty (no filter). The available operations and statistics can be obtained from availableAdvancedFilterOptions.
			Name (str): Specifies the filter name. It must be unique per view.
			SortingStats (str): Specifies the list of statistics by which the view will be sorted.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): Gets the id of the filter, which is used to add the filter to a view.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.advancedfilter.advancedfilter.AdvancedFilter)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.advancedfilter.advancedfilter import AdvancedFilter
		return self._create(AdvancedFilter(self), locals())

	def AvailableAdvancedFilterOptions(self, Operators=None, Stat=None):
		"""Gets child instances of AvailableAdvancedFilterOptions from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AvailableAdvancedFilterOptions will be returned.

		Args:
			Operators (str): Returns the operators list for a filter option.
			Stat (str): Returns the statistic name for a filter option.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.availableadvancedfilteroptions.availableadvancedfilteroptions.AvailableAdvancedFilterOptions))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.availableadvancedfilteroptions.availableadvancedfilteroptions import AvailableAdvancedFilterOptions
		return self._select(AvailableAdvancedFilterOptions(self), locals())

	@property
	def AdvancedCVFilter(self):
		"""Sets the advanced filter for a custom view. Note: To change the filter on an existing view, you must first disable it.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=advancedCVFilters)
		"""
		return self._get_attribute('advancedCVFilter')
	@AdvancedCVFilter.setter
	def AdvancedCVFilter(self, value):
		self._set_attribute('advancedCVFilter', value)

	@property
	def AdvancedFilterName(self):
		"""Selects an advanced filter from the ones available in the selected drill down view.

		Returns:
			str
		"""
		return self._get_attribute('advancedFilterName')
	@AdvancedFilterName.setter
	def AdvancedFilterName(self, value):
		self._set_attribute('advancedFilterName', value)

	@property
	def AggregationType(self):
		"""Signifies the type of aggregation of next gen protocols

		Returns:
			str(perPort|perSession)
		"""
		return self._get_attribute('aggregationType')
	@AggregationType.setter
	def AggregationType(self, value):
		self._set_attribute('aggregationType', value)

	@property
	def AllAdvancedFilters(self):
		"""Returns a list with all the filters that are present in the selected drill down views. This includes filters that cannot be applied for the current drill down view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('allAdvancedFilters')

	@property
	def MatchingAdvancedFilters(self):
		"""Returns a list that contains only the filters that can be applied on the current drill down view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('matchingAdvancedFilters')

	@property
	def PortFilterIds(self):
		"""Filters the port IDs

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])
		"""
		return self._get_attribute('portFilterIds')
	@PortFilterIds.setter
	def PortFilterIds(self, value):
		self._set_attribute('portFilterIds', value)

	@property
	def ProtocolFilterIds(self):
		"""Filters the protocol IDs

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])
		"""
		return self._get_attribute('protocolFilterIds')
	@ProtocolFilterIds.setter
	def ProtocolFilterIds(self, value):
		self._set_attribute('protocolFilterIds', value)

	def remove(self):
		"""Deletes a child instance of Layer23NextGenProtocolFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def AddAdvancedFilter(self, Arg2):
		"""Executes the addAdvancedFilter operation on the server.

		NOT DEFINED

		Args:
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('addAdvancedFilter', payload=locals(), response_object=None)

	def RemoveAdvancedFilter(self, Arg2):
		"""Executes the removeAdvancedFilter operation on the server.

		NOT DEFINED

		Args:
			Arg2 (str): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('removeAdvancedFilter', payload=locals(), response_object=None)

	def RemoveAllAdvancedFilters(self):
		"""Executes the removeAllAdvancedFilters operation on the server.

		NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('removeAllAdvancedFilters', payload=locals(), response_object=None)
