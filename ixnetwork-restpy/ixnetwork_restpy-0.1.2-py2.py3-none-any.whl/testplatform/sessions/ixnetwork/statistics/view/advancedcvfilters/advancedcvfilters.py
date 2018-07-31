from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AdvancedCVFilters(Base):
	"""Sets the advanced filter for a custom view. Note- To change the filter on an existing view, you must first disable it.
	"""

	_SDM_NAME = 'advancedCVFilters'

	def __init__(self, parent):
		super(AdvancedCVFilters, self).__init__(parent)

	@property
	def AvailableFilterOptions(self):
		"""Returns a list of all the statistics and the operations available for filtering. Note- A protocol and a grouping must be set in order for this to work.

		Returns:
			str
		"""
		return self._get_attribute('availableFilterOptions')

	@property
	def AvailableGroupingOptions(self):
		"""Returns all the grouping options available. Note - A protocol must be set in order for this to work.

		Returns:
			str
		"""
		return self._get_attribute('availableGroupingOptions')

	@property
	def Caption(self):
		"""Sets a name for the filter.

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def Expression(self):
		"""Specifies the filter body. This is a string that must have the specific format. This can be empty or no filter.The available operations and statistics can be obtained from availableFilterOptions.

		Returns:
			str
		"""
		return self._get_attribute('expression')
	@Expression.setter
	def Expression(self, value):
		self._set_attribute('expression', value)

	@property
	def Grouping(self):
		"""Sets a grouping for the filter.

		Returns:
			str
		"""
		return self._get_attribute('grouping')
	@Grouping.setter
	def Grouping(self, value):
		self._set_attribute('grouping', value)

	@property
	def Protocol(self):
		"""Sets a protocol for the filter.

		Returns:
			str
		"""
		return self._get_attribute('protocol')
	@Protocol.setter
	def Protocol(self, value):
		self._set_attribute('protocol', value)

	@property
	def SortingStats(self):
		"""Specifies the list of statistics by which the view is sorted.

		Returns:
			str
		"""
		return self._get_attribute('sortingStats')
	@SortingStats.setter
	def SortingStats(self, value):
		self._set_attribute('sortingStats', value)

	def remove(self):
		"""Deletes a child instance of AdvancedCVFilters on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
