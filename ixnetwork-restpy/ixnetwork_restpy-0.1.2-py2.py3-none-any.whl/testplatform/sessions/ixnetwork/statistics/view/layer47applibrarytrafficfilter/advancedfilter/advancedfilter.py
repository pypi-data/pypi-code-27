from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AdvancedFilter(Base):
	"""Allows you to configure an advanced filter for drill down views.
	"""

	_SDM_NAME = 'advancedFilter'

	def __init__(self, parent):
		super(AdvancedFilter, self).__init__(parent)

	@property
	def Expression(self):
		"""Specifies the filter body. This is a string that must have a specific format.This can be empty (no filter). The available operations and statistics can be obtained from availableAdvancedFilterOptions.

		Returns:
			str
		"""
		return self._get_attribute('expression')
	@Expression.setter
	def Expression(self, value):
		self._set_attribute('expression', value)

	@property
	def Name(self):
		"""Specifies the filter name. It must be unique per view.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def SortingStats(self):
		"""Specifies the list of statistics by which the view will be sorted.

		Returns:
			str
		"""
		return self._get_attribute('sortingStats')
	@SortingStats.setter
	def SortingStats(self, value):
		self._set_attribute('sortingStats', value)

	@property
	def TrackingFilterId(self):
		"""Gets the id of the filter, which is used to add the filter to a view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('trackingFilterId')
	@TrackingFilterId.setter
	def TrackingFilterId(self, value):
		self._set_attribute('trackingFilterId', value)

	def remove(self):
		"""Deletes a child instance of AdvancedFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
