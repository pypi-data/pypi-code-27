from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableAdvancedFilters(Base):
	"""Represents the id of an advanced filter.
	"""

	_SDM_NAME = 'availableAdvancedFilters'

	def __init__(self, parent):
		super(AvailableAdvancedFilters, self).__init__(parent)

	@property
	def Expression(self):
		"""Allows you to get the filter expression or the body from the id.

		Returns:
			str
		"""
		return self._get_attribute('expression')

	@property
	def Name(self):
		"""Allows you to get the filter name from the id.

		Returns:
			str
		"""
		return self._get_attribute('name')
