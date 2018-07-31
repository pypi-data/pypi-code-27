from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableAdvancedFilterOptions(Base):
	"""Provides a list of all the statistics and the filtering options for the current view.
	"""

	_SDM_NAME = 'availableAdvancedFilterOptions'

	def __init__(self, parent):
		super(AvailableAdvancedFilterOptions, self).__init__(parent)

	@property
	def Operators(self):
		"""Returns the operators list for a filter option.

		Returns:
			str
		"""
		return self._get_attribute('operators')

	@property
	def Stat(self):
		"""Returns the statistic name for a filter option.

		Returns:
			str
		"""
		return self._get_attribute('stat')
