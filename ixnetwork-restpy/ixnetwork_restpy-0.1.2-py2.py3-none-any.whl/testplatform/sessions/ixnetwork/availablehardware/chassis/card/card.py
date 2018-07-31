from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Card(Base):
	"""This command allows the user to view version and type information for the card.
	"""

	_SDM_NAME = 'card'

	def __init__(self, parent):
		super(Card, self).__init__(parent)

	def Aggregation(self):
		"""Gets child instances of Aggregation from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Aggregation will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.aggregation.aggregation.Aggregation))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.aggregation.aggregation import Aggregation
		return self._select(Aggregation(self), locals())

	def Port(self, Description=None, Owner=None):
		"""Gets child instances of Port from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Port will be returned.

		Args:
			Description (str): The port description/mode.
			Owner (str): The current owner of the port.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.port.Port))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.port import Port
		return self._select(Port(self), locals())

	@property
	def AggregationMode(self):
		"""Gets or sets the aggregation mode.

		Returns:
			str(atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGigAggregation|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|mixed|normal|notSupported|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGigAggregation|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut)
		"""
		return self._get_attribute('aggregationMode')
	@AggregationMode.setter
	def AggregationMode(self, value):
		self._set_attribute('aggregationMode', value)

	@property
	def AggregationSupported(self):
		"""(read only) If true, indicates that the card is operating in resource group mode and not in normal mode

		Returns:
			bool
		"""
		return self._get_attribute('aggregationSupported')

	@property
	def AvailableModes(self):
		"""Gets the supported port resource group modes on the card.

		Returns:
			list(str[atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGigAggregation|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|mixed|normal|notSupported|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGigAggregation|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut])
		"""
		return self._get_attribute('availableModes')

	@property
	def CardId(self):
		"""Identifier for the card on the chassis.

		Returns:
			number
		"""
		return self._get_attribute('cardId')

	@property
	def Description(self):
		"""Description of the card.

		Returns:
			str
		"""
		return self._get_attribute('description')

	def RefreshInfo(self, Arg1):
		"""Executes the refreshInfo operation on the server.

		Refresh the hardware information.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=chassis|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=card])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('refreshInfo', payload=locals(), response_object=None)
