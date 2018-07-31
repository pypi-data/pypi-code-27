from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Latency(Base):
	"""This object sets the latency mode to fetch related statistics for each mode.
	"""

	_SDM_NAME = 'latency'

	def __init__(self, parent):
		super(Latency, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, latency statistics is enabled and if false, latency statistics is disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Mode(self):
		"""Latency statistics is generated according to the mode set if latency is enabled.

		Returns:
			str(cutThrough|forwardingDelay|mef|storeForward)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)
