from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Aggregation(Base):
	"""The Card resource group.
	"""

	_SDM_NAME = 'aggregation'

	def __init__(self, parent):
		super(Aggregation, self).__init__(parent)

	@property
	def ActivePort(self):
		"""Deprecated. Use activePorts instead.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port)
		"""
		return self._get_attribute('activePort')

	@property
	def ActivePorts(self):
		"""All active ports from Resource Group.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])
		"""
		return self._get_attribute('activePorts')

	@property
	def AvailableModes(self):
		"""Gets the supported resource group modes.

		Returns:
			list(str[atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGig|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|normal|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGig|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut])
		"""
		return self._get_attribute('availableModes')

	@property
	def Mode(self):
		"""Resource Group mode.

		Returns:
			str(atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGig|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|normal|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGig|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def ResourcePorts(self):
		"""All ports from Resource Group.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])
		"""
		return self._get_attribute('resourcePorts')
