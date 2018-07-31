from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Counter(Base):
	"""This object provides different options for UDF in Counter Type.
	"""

	_SDM_NAME = 'counter'

	def __init__(self, parent):
		super(Counter, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""Contains all the possible widths available for a UDF in particular Type.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def BitOffset(self):
		"""Specifies additional Offset of the UDF in terms of bits. This Offset will start from where the Offset provided in Byte Offset field ends.

		Returns:
			number
		"""
		return self._get_attribute('bitOffset')
	@BitOffset.setter
	def BitOffset(self, value):
		self._set_attribute('bitOffset', value)

	@property
	def Count(self):
		"""Specifies the repeat count for the UDF. After the elapse of this count, UDF will again start from the Start Value.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def Direction(self):
		"""Specifies if the UDF value will be incremented or decremented.

		Returns:
			str(decrement|increment)
		"""
		return self._get_attribute('direction')
	@Direction.setter
	def Direction(self, value):
		self._set_attribute('direction', value)

	@property
	def StartValue(self):
		"""Specifies the Start Value of the UDF.

		Returns:
			number
		"""
		return self._get_attribute('startValue')
	@StartValue.setter
	def StartValue(self, value):
		self._set_attribute('startValue', value)

	@property
	def StepValue(self):
		"""Specifies the Step Value by which the UDF value will be incremented or decremented.

		Returns:
			number
		"""
		return self._get_attribute('stepValue')
	@StepValue.setter
	def StepValue(self, value):
		self._set_attribute('stepValue', value)

	@property
	def Width(self):
		"""Specifies the width of the UDF.

		Returns:
			str(1|10|11|12|13|14|15|16|17|18|19|2|20|21|22|23|24|25|26|27|28|29|3|30|31|32|4|5|6|7|8|9)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)
