from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DataCollection(Base):
	"""Specifies the collection of data.
	"""

	_SDM_NAME = 'dataCollection'

	def __init__(self, parent):
		super(DataCollection, self).__init__(parent)

	@property
	def Enable(self):
		"""If it is true, enables collection of data

		Returns:
			bool
		"""
		return self._get_attribute('Enable')
	@Enable.setter
	def Enable(self, value):
		self._set_attribute('Enable', value)

	@property
	def LastRunId(self):
		"""Specifies the identifier for last run.

		Returns:
			number
		"""
		return self._get_attribute('LastRunId')
