from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class StatisticFilter(Base):
	"""Statistic filter specification.
	"""

	_SDM_NAME = 'statisticFilter'

	def __init__(self, parent):
		super(StatisticFilter, self).__init__(parent)

	@property
	def Operator(self):
		"""The logical operation to be performed.

		Returns:
			str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isLike|isNotLike|isSmaller)
		"""
		return self._get_attribute('operator')
	@Operator.setter
	def Operator(self, value):
		self._set_attribute('operator', value)

	@property
	def StatisticFilterId(self):
		"""Selected statistic filters from the availableStatisticFilter list.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)
		"""
		return self._get_attribute('statisticFilterId')
	@StatisticFilterId.setter
	def StatisticFilterId(self, value):
		self._set_attribute('statisticFilterId', value)

	@property
	def Value(self):
		"""Value of statistic to be matched based on operator.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def remove(self):
		"""Deletes a child instance of StatisticFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
