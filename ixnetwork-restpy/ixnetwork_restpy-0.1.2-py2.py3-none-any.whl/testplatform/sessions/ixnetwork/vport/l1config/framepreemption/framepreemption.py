from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FramePreemption(Base):
	"""
	"""

	_SDM_NAME = 'framePreemption'

	def __init__(self, parent):
		super(FramePreemption, self).__init__(parent)

	@property
	def IsFramePreemptionEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isFramePreemptionEnabled')
	@IsFramePreemptionEnabled.setter
	def IsFramePreemptionEnabled(self, value):
		self._set_attribute('isFramePreemptionEnabled', value)
