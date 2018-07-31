from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FrameRateDistribution(Base):
	"""This object provides the options for Frame Rate distribution.
	"""

	_SDM_NAME = 'frameRateDistribution'

	def __init__(self, parent):
		super(FrameRateDistribution, self).__init__(parent)

	@property
	def PortDistribution(self):
		"""At the port level, apply the target configuration transmission rate for each encapsulation.

		Returns:
			str(applyRateToAll|splitRateEvenly)
		"""
		return self._get_attribute('portDistribution')
	@PortDistribution.setter
	def PortDistribution(self, value):
		self._set_attribute('portDistribution', value)

	@property
	def StreamDistribution(self):
		"""At the flow group level, apply the target rate of each port.

		Returns:
			str(applyRateToAll|splitRateEvenly)
		"""
		return self._get_attribute('streamDistribution')
	@StreamDistribution.setter
	def StreamDistribution(self, value):
		self._set_attribute('streamDistribution', value)
