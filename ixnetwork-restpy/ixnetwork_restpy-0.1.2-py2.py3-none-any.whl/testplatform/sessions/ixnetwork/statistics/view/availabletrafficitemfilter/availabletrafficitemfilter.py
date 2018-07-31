from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableTrafficItemFilter(Base):
	"""List of traffic items available for filtering.
	"""

	_SDM_NAME = 'availableTrafficItemFilter'

	def __init__(self, parent):
		super(AvailableTrafficItemFilter, self).__init__(parent)

	@property
	def Constraints(self):
		"""Lists down the constraints associated with the available traffic item filter list.

		Returns:
			list(str)
		"""
		return self._get_attribute('constraints')

	@property
	def Name(self):
		"""Displays the name of the traffic item filter.

		Returns:
			str
		"""
		return self._get_attribute('name')
