from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableProtocolFilter(Base):
	"""The protocol combinations that are permitted in IxNetwork.
	"""

	_SDM_NAME = 'availableProtocolFilter'

	def __init__(self, parent):
		super(AvailableProtocolFilter, self).__init__(parent)

	@property
	def Name(self):
		"""The unique identifier of the object.

		Returns:
			str
		"""
		return self._get_attribute('name')
