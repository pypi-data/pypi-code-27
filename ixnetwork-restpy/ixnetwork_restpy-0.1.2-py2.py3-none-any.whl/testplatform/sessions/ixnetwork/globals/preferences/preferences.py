from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Preferences(Base):
	"""The preferences node contains user configurable system wide preferences
	"""

	_SDM_NAME = 'preferences'

	def __init__(self, parent):
		super(Preferences, self).__init__(parent)

	@property
	def ConnectPortsOnLoadConfig(self):
		"""If true the application will connect the virtual ports to any assigned hardware ports when the configuration is loaded

		Returns:
			bool
		"""
		return self._get_attribute('connectPortsOnLoadConfig')
	@ConnectPortsOnLoadConfig.setter
	def ConnectPortsOnLoadConfig(self, value):
		self._set_attribute('connectPortsOnLoadConfig', value)

	@property
	def LatestConfigInDiagEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('latestConfigInDiagEnabled')
	@LatestConfigInDiagEnabled.setter
	def LatestConfigInDiagEnabled(self, value):
		self._set_attribute('latestConfigInDiagEnabled', value)

	@property
	def RebootPortsOnConnect(self):
		"""If true the application will reboot any connected virtual ports when the configuration is loaded

		Returns:
			bool
		"""
		return self._get_attribute('rebootPortsOnConnect')
	@RebootPortsOnConnect.setter
	def RebootPortsOnConnect(self, value):
		self._set_attribute('rebootPortsOnConnect', value)
