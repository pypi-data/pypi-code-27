from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistic(Base):
	"""
	"""

	_SDM_NAME = 'statistic'

	def __init__(self, parent):
		super(Statistic, self).__init__(parent)

	@property
	def Caption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('caption')

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
