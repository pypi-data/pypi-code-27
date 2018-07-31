from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MisdirectedPerFlow(Base):
	"""Display misdirected statistics on a per-flow basis. When active this replaces port level misdirected statistics
	"""

	_SDM_NAME = 'misdirectedPerFlow'

	def __init__(self, parent):
		super(MisdirectedPerFlow, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true then misdirected per flow statistics will be enabled

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
