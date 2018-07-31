from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowCondition(Base):
	"""Flow condition for displaying egress/ingress statistics.
	"""

	_SDM_NAME = 'flowCondition'

	def __init__(self, parent):
		super(FlowCondition, self).__init__(parent)

	@property
	def Operator(self):
		"""The logical operation to be performed.

		Returns:
			str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)
		"""
		return self._get_attribute('operator')
	@Operator.setter
	def Operator(self, value):
		self._set_attribute('operator', value)

	@property
	def ShowFirstMatchingSet(self):
		"""If true, displays the first matching set.

		Returns:
			bool
		"""
		return self._get_attribute('showFirstMatchingSet')
	@ShowFirstMatchingSet.setter
	def ShowFirstMatchingSet(self, value):
		self._set_attribute('showFirstMatchingSet', value)

	@property
	def TrackingFilterId(self):
		"""Selected tracking filters from the availableTrackingFilter list.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)
		"""
		return self._get_attribute('trackingFilterId')
	@TrackingFilterId.setter
	def TrackingFilterId(self, value):
		self._set_attribute('trackingFilterId', value)

	@property
	def Values(self):
		"""Value to be matched for the condition.

		Returns:
			list(number)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)

	def remove(self):
		"""Deletes a child instance of FlowCondition on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
