from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23TrafficItemFilter(Base):
	"""Filters associated with layer23TrafficItem view.
	"""

	_SDM_NAME = 'layer23TrafficItemFilter'

	def __init__(self, parent):
		super(Layer23TrafficItemFilter, self).__init__(parent)

	@property
	def TrafficItemFilterIds(self):
		"""Selected traffic item filters from the availableTrafficItemFilter list.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrafficItemFilter])
		"""
		return self._get_attribute('trafficItemFilterIds')
	@TrafficItemFilterIds.setter
	def TrafficItemFilterIds(self, value):
		self._set_attribute('trafficItemFilterIds', value)

	def remove(self):
		"""Deletes a child instance of Layer23TrafficItemFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
