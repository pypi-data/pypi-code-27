from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailablePortFilter(Base):
	"""List of ports available for filtering.
	"""

	_SDM_NAME = 'availablePortFilter'

	def __init__(self, parent):
		super(AvailablePortFilter, self).__init__(parent)

	@property
	def Name(self):
		"""The name of the port filter.

		Returns:
			str
		"""
		return self._get_attribute('name')
