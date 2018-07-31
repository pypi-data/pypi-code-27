from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AdvancedSequenceChecking(Base):
	"""Checks advanced sequence.
	"""

	_SDM_NAME = 'advancedSequenceChecking'

	def __init__(self, parent):
		super(AdvancedSequenceChecking, self).__init__(parent)

	@property
	def AdvancedSequenceThreshold(self):
		"""Signifies the threshold of advanced sequence

		Returns:
			number
		"""
		return self._get_attribute('advancedSequenceThreshold')
	@AdvancedSequenceThreshold.setter
	def AdvancedSequenceThreshold(self, value):
		self._set_attribute('advancedSequenceThreshold', value)

	@property
	def Enabled(self):
		"""If true, enables advanced sequence checking

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
