from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Dcc(Base):
	"""The Layer 1 Configuration is being configured for a POS port and DCC is selected as the Payload Type.
	"""

	_SDM_NAME = 'dcc'

	def __init__(self, parent):
		super(Dcc, self).__init__(parent)

	@property
	def Crc(self):
		"""Choose the type of Cyclic Redundancy Check to be used.

		Returns:
			str(crc16|crc32)
		"""
		return self._get_attribute('crc')
	@Crc.setter
	def Crc(self, value):
		self._set_attribute('crc', value)

	@property
	def OverheadByte(self):
		"""Choose the type of Overhead bytes to be used for transmitting the DCC packet streams.

		Returns:
			str(loh|soh)
		"""
		return self._get_attribute('overheadByte')
	@OverheadByte.setter
	def OverheadByte(self, value):
		self._set_attribute('overheadByte', value)

	@property
	def TimeFill(self):
		"""Choose the type of bytes used to fill the gaps between DCC frames.

		Returns:
			str(flag7E|markIdle)
		"""
		return self._get_attribute('timeFill')
	@TimeFill.setter
	def TimeFill(self, value):
		self._set_attribute('timeFill', value)
