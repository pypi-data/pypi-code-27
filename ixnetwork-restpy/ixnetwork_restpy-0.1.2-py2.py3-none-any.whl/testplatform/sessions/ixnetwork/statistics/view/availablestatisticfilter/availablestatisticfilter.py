from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableStatisticFilter(Base):
	"""List of statistics available for filtering.
	"""

	_SDM_NAME = 'availableStatisticFilter'

	def __init__(self, parent):
		super(AvailableStatisticFilter, self).__init__(parent)

	@property
	def Caption(self):
		"""Name of the statistic.

		Returns:
			str
		"""
		return self._get_attribute('caption')
