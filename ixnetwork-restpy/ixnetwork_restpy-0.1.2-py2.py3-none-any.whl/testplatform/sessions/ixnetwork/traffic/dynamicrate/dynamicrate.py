from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DynamicRate(Base):
	"""This object provides different options for the rate that can be changed on the fly.
	"""

	_SDM_NAME = 'dynamicRate'

	def __init__(self, parent):
		super(DynamicRate, self).__init__(parent)

	@property
	def BitRateUnitsType(self):
		"""The rate units for transmitting packet.

		Returns:
			str(bitsPerSec|bytesPerSec|kbitsPerSec|kbytesPerSec|mbitsPerSec|mbytesPerSec)
		"""
		return self._get_attribute('bitRateUnitsType')
	@BitRateUnitsType.setter
	def BitRateUnitsType(self, value):
		self._set_attribute('bitRateUnitsType', value)

	@property
	def EnforceMinimumInterPacketGap(self):
		"""Sets the minimum inter-packet gap allowed for Ethernet ports only.

		Returns:
			number
		"""
		return self._get_attribute('enforceMinimumInterPacketGap')
	@EnforceMinimumInterPacketGap.setter
	def EnforceMinimumInterPacketGap(self, value):
		self._set_attribute('enforceMinimumInterPacketGap', value)

	@property
	def HighLevelStreamName(self):
		"""The name of the high level stream

		Returns:
			str
		"""
		return self._get_attribute('highLevelStreamName')

	@property
	def InterPacketGapUnitsType(self):
		"""The inter-packet gap expressed in units.

		Returns:
			str(bytes|nanoseconds)
		"""
		return self._get_attribute('interPacketGapUnitsType')
	@InterPacketGapUnitsType.setter
	def InterPacketGapUnitsType(self, value):
		self._set_attribute('interPacketGapUnitsType', value)

	@property
	def OverSubscribed(self):
		"""If true, the packet transmission rate is oversubscribed.

		Returns:
			bool
		"""
		return self._get_attribute('overSubscribed')

	@property
	def Rate(self):
		"""The rate at which packet is transmitted.

		Returns:
			number
		"""
		return self._get_attribute('rate')
	@Rate.setter
	def Rate(self, value):
		self._set_attribute('rate', value)

	@property
	def RateType(self):
		"""The types of packet rate transmission.

		Returns:
			str(bitsPerSecond|framesPerSecond|interPacketGap|percentLineRate)
		"""
		return self._get_attribute('rateType')
	@RateType.setter
	def RateType(self, value):
		self._set_attribute('rateType', value)

	@property
	def TrafficItemName(self):
		"""The name of the parent traffic item.

		Returns:
			str
		"""
		return self._get_attribute('trafficItemName')

	@property
	def TxPort(self):
		"""The transmitting port.

		Returns:
			number
		"""
		return self._get_attribute('txPort')
