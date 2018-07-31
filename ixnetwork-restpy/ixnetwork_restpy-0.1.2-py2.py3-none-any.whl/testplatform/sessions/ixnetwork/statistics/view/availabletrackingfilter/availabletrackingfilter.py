from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableTrackingFilter(Base):
	"""List of tracking available for filtering.
	"""

	_SDM_NAME = 'availableTrackingFilter'

	def __init__(self, parent):
		super(AvailableTrackingFilter, self).__init__(parent)

	@property
	def Constraints(self):
		"""Lists down the constraints associated with the available tracking filter list.

		Returns:
			list(str)
		"""
		return self._get_attribute('constraints')

	@property
	def Name(self):
		"""Displays the name of the tracking filter.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def TrackingType(self):
		"""Indicates the tracking type.

		Returns:
			str
		"""
		return self._get_attribute('trackingType')

	@property
	def ValueType(self):
		"""Value of tracking to be matched based on operator.

		Returns:
			str
		"""
		return self._get_attribute('valueType')
