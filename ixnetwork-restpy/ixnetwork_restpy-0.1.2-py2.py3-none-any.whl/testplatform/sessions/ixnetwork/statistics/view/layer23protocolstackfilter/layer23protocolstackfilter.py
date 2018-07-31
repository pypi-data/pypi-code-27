from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23ProtocolStackFilter(Base):
	"""Filters associated with layer23ProtocolStack view.
	"""

	_SDM_NAME = 'layer23ProtocolStackFilter'

	def __init__(self, parent):
		super(Layer23ProtocolStackFilter, self).__init__(parent)

	@property
	def DrilldownType(self):
		"""Emulates perRange or perSession view based on the option seleted.

		Returns:
			str(perRange|perSession)
		"""
		return self._get_attribute('drilldownType')
	@DrilldownType.setter
	def DrilldownType(self, value):
		self._set_attribute('drilldownType', value)

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
	def ProtocolStackFilterId(self):
		"""Selected protocol stack filters from the availableProtocolStackFilter list.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolStackFilter])
		"""
		return self._get_attribute('protocolStackFilterId')
	@ProtocolStackFilterId.setter
	def ProtocolStackFilterId(self, value):
		self._set_attribute('protocolStackFilterId', value)

	@property
	def SortAscending(self):
		"""Sets the display order of the view.

		Returns:
			bool
		"""
		return self._get_attribute('sortAscending')
	@SortAscending.setter
	def SortAscending(self, value):
		self._set_attribute('sortAscending', value)

	@property
	def SortingStatistic(self):
		"""The reference statistic by which the data will be sorted in created SV.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=statistic)
		"""
		return self._get_attribute('sortingStatistic')
	@SortingStatistic.setter
	def SortingStatistic(self, value):
		self._set_attribute('sortingStatistic', value)

	def remove(self):
		"""Deletes a child instance of Layer23ProtocolStackFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
