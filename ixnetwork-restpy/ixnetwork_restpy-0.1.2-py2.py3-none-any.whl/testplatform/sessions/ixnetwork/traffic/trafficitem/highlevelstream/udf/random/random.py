from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Random(Base):
	"""This object specifies the random properties of UDF.
	"""

	_SDM_NAME = 'random'

	def __init__(self, parent):
		super(Random, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""Species all the possible widths available for a UDF in particular Type.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def Mask(self):
		"""Sets the UDF mask.

		Returns:
			str
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def Width(self):
		"""Specifies the width of the UDF.

		Returns:
			str(16|24|32|8)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)
