from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TransmissionDistribution(Base):
	"""This object provides the options for packet transmission distribution.
	"""

	_SDM_NAME = 'transmissionDistribution'

	def __init__(self, parent):
		super(TransmissionDistribution, self).__init__(parent)

	@property
	def AvailableDistributions(self):
		"""Indicates the available transmission distributions for the traffic streams.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableDistributions')

	@property
	def Distributions(self):
		"""Indicates the predefined size distribution based on size and weight.

		Returns:
			list(str)
		"""
		return self._get_attribute('distributions')
	@Distributions.setter
	def Distributions(self, value):
		self._set_attribute('distributions', value)

	@property
	def DistributionsDisplayNames(self):
		"""Returns user friendly list of distribution fields

		Returns:
			list(str)
		"""
		return self._get_attribute('distributionsDisplayNames')
