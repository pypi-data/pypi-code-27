from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InterArrivalTimeRate(Base):
	"""This object sets the inter arrival time delay of each packet.
	"""

	_SDM_NAME = 'interArrivalTimeRate'

	def __init__(self, parent):
		super(InterArrivalTimeRate, self).__init__(parent)

	@property
	def Enabled(self):
		"""If enabled, fetches inter-arrival time and rate statistics.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
