from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EnumerationFilter(Base):
	"""Enumeration filter specification.
	"""

	_SDM_NAME = 'enumerationFilter'

	def __init__(self, parent):
		super(EnumerationFilter, self).__init__(parent)

	@property
	def SortDirection(self):
		"""Sets the display order of the view.

		Returns:
			str(ascending|descending)
		"""
		return self._get_attribute('sortDirection')
	@SortDirection.setter
	def SortDirection(self, value):
		self._set_attribute('sortDirection', value)

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

	def remove(self):
		"""Deletes a child instance of EnumerationFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
