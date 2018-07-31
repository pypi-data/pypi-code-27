from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AllFlowsFilter(Base):
	"""All flows filter specification.
	"""

	_SDM_NAME = 'allFlowsFilter'

	def __init__(self, parent):
		super(AllFlowsFilter, self).__init__(parent)

	@property
	def NumberOfResults(self):
		"""Number of traffic flows to be displayed.

		Returns:
			number
		"""
		return self._get_attribute('numberOfResults')
	@NumberOfResults.setter
	def NumberOfResults(self, value):
		self._set_attribute('numberOfResults', value)

	@property
	def SortByStatisticId(self):
		"""The reference statistic by which the data will be sorted in created SV.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)
		"""
		return self._get_attribute('sortByStatisticId')
	@SortByStatisticId.setter
	def SortByStatisticId(self, value):
		self._set_attribute('sortByStatisticId', value)

	@property
	def SortingCondition(self):
		"""Sets the display order of the view.

		Returns:
			str(bestPerformers|worstPerformers)
		"""
		return self._get_attribute('sortingCondition')
	@SortingCondition.setter
	def SortingCondition(self, value):
		self._set_attribute('sortingCondition', value)

	def remove(self):
		"""Deletes a child instance of AllFlowsFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
