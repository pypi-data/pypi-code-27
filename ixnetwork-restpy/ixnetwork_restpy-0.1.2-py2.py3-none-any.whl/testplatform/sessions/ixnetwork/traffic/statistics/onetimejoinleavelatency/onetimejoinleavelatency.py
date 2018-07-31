from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OneTimeJoinLeaveLatency(Base):
	"""Calculate join/leave latency for AMT in case of one-time join/leave. This means that a host can only join/leave a group once between traffic start and stop
	"""

	_SDM_NAME = 'oneTimeJoinLeaveLatency'

	def __init__(self, parent):
		super(OneTimeJoinLeaveLatency, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true enables one time join leave latency.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
