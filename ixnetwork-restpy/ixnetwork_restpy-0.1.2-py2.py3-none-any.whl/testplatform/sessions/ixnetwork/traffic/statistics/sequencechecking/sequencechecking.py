from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SequenceChecking(Base):
	"""This object fetches sequence checking statistics.
	"""

	_SDM_NAME = 'sequenceChecking'

	def __init__(self, parent):
		super(SequenceChecking, self).__init__(parent)

	@property
	def AdvancedSequenceThreshold(self):
		"""Checks the sequence.

		Returns:
			number
		"""
		return self._get_attribute('advancedSequenceThreshold')
	@AdvancedSequenceThreshold.setter
	def AdvancedSequenceThreshold(self, value):
		self._set_attribute('advancedSequenceThreshold', value)

	@property
	def Enabled(self):
		"""If enabled, fetches sequence checking statistics to measure duplicate packets, sequence gap, and the last sequence number.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def SequenceMode(self):
		"""The mode to conduct sequence checking.

		Returns:
			str(advanced|rxPacketArrival|rxSwitchedPath|rxThreshold)
		"""
		return self._get_attribute('sequenceMode')
	@SequenceMode.setter
	def SequenceMode(self, value):
		self._set_attribute('sequenceMode', value)
