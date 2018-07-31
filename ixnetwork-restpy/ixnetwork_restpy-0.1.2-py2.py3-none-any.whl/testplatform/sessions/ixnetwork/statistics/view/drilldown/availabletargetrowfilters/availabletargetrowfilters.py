from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableTargetRowFilters(Base):
	"""Provides a list of filters that can be used to select the row used to perform the drill-down
	"""

	_SDM_NAME = 'availableTargetRowFilters'

	def __init__(self, parent):
		super(AvailableTargetRowFilters, self).__init__(parent)
