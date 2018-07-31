from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Licensing(Base):
	"""Container for licensing options
	"""

	_SDM_NAME = 'licensing'

	def __init__(self, parent):
		super(Licensing, self).__init__(parent)

	@property
	def LicensingServers(self):
		"""List of license servers to use

		Returns:
			list(str)
		"""
		return self._get_attribute('licensingServers')
	@LicensingServers.setter
	def LicensingServers(self, value):
		self._set_attribute('licensingServers', value)

	@property
	def Mode(self):
		"""Set license mode to either perpetual or subscription

		Returns:
			str(mixed|perpetual|subscription)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def Tier(self):
		"""set or get the tier level, using the tier ID. Available IDs are: tier3-10g, tier3, tier2, tier1

		Returns:
			str
		"""
		return self._get_attribute('tier')
	@Tier.setter
	def Tier(self, value):
		self._set_attribute('tier', value)
