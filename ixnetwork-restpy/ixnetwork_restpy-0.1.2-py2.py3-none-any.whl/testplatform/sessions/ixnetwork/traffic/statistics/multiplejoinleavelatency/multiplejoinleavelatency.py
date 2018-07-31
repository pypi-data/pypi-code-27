from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MultipleJoinLeaveLatency(Base):
	"""Calculate join/leave latency for AMT in cae of repeated join/leave. This means that a host can join/leave a group multiple times between traffic start and stop
	"""

	_SDM_NAME = 'multipleJoinLeaveLatency'

	def __init__(self, parent):
		super(MultipleJoinLeaveLatency, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true enables multiple join leave latency.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
