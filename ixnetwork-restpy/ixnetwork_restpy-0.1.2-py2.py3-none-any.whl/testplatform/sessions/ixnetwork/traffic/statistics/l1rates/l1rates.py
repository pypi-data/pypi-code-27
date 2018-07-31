from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class L1Rates(Base):
	"""Layer 1 rates.
	"""

	_SDM_NAME = 'l1Rates'

	def __init__(self, parent):
		super(L1Rates, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables layer 1 rates

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
