from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Uds(Base):
	"""A counter that increments each time the capture filter conditions are met, as defined in the Capture Filter window.
	"""

	_SDM_NAME = 'uds'

	def __init__(self, parent):
		super(Uds, self).__init__(parent)

	@property
	def CustomFrameSizeFrom(self):
		"""Frame size customized from.

		Returns:
			number
		"""
		return self._get_attribute('customFrameSizeFrom')
	@CustomFrameSizeFrom.setter
	def CustomFrameSizeFrom(self, value):
		self._set_attribute('customFrameSizeFrom', value)

	@property
	def CustomFrameSizeTo(self):
		"""Customized frame size.

		Returns:
			number
		"""
		return self._get_attribute('customFrameSizeTo')
	@CustomFrameSizeTo.setter
	def CustomFrameSizeTo(self, value):
		self._set_attribute('customFrameSizeTo', value)

	@property
	def DestinationAddressSelector(self):
		"""Destination address selector.

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('destinationAddressSelector')
	@DestinationAddressSelector.setter
	def DestinationAddressSelector(self, value):
		self._set_attribute('destinationAddressSelector', value)

	@property
	def Error(self):
		"""Indicates error.

		Returns:
			str(errAnyFrame|errBadCRC|errBadFrame|errGoodFrame)
		"""
		return self._get_attribute('error')
	@Error.setter
	def Error(self, value):
		self._set_attribute('error', value)

	@property
	def FrameSizeType(self):
		"""The type of frame size.

		Returns:
			str(any|custom|jumbo|oversized|undersized)
		"""
		return self._get_attribute('frameSizeType')
	@FrameSizeType.setter
	def FrameSizeType(self, value):
		self._set_attribute('frameSizeType', value)

	@property
	def IsEnabled(self):
		"""If true, UDS is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

	@property
	def PatternSelector(self):
		"""Pattern selector.

		Returns:
			str(anyPattern|notPattern1|notPattern2|pattern1|pattern2)
		"""
		return self._get_attribute('patternSelector')
	@PatternSelector.setter
	def PatternSelector(self, value):
		self._set_attribute('patternSelector', value)

	@property
	def SourceAddressSelector(self):
		"""Source address selector.

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('sourceAddressSelector')
	@SourceAddressSelector.setter
	def SourceAddressSelector(self, value):
		self._set_attribute('sourceAddressSelector', value)
