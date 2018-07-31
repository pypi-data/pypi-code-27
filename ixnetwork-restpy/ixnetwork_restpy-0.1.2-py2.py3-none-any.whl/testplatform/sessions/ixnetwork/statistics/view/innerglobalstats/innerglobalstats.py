from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InnerGlobalStats(Base):
	"""NOT DEFINED
	"""

	_SDM_NAME = 'innerGlobalStats'

	def __init__(self, parent):
		super(InnerGlobalStats, self).__init__(parent)

	@property
	def ColumnCaptions(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('columnCaptions')

	@property
	def RowValues(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('rowValues')
