from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistic(Base):
	"""
	"""

	_SDM_NAME = 'statistic'

	def __init__(self, parent):
		super(Statistic, self).__init__(parent)

	@property
	def AggregationType(self):
		"""

		Returns:
			str(average|averageRate|ax|axRate|intervalAverage|min|minRate|none|rate|runStateAgg|runStateAggIgnoreRamp|sum|vectorMax|vectorMin|weightedAverage)
		"""
		return self._get_attribute('aggregationType')
	@AggregationType.setter
	def AggregationType(self, value):
		self._set_attribute('aggregationType', value)

	@property
	def Caption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def DefaultCaption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('defaultCaption')

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

	@property
	def ScaleFactor(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('scaleFactor')
	@ScaleFactor.setter
	def ScaleFactor(self, value):
		self._set_attribute('scaleFactor', value)

	@property
	def SourceTypes(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceTypes')
