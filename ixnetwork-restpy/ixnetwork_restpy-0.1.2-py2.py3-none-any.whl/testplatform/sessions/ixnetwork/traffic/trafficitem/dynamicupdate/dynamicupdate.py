from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DynamicUpdate(Base):
	"""Contains attributes that help IxNetwork update the corresponding traffic packet labels on the fly based on the information from the configured protocol.
	"""

	_SDM_NAME = 'dynamicUpdate'

	def __init__(self, parent):
		super(DynamicUpdate, self).__init__(parent)

	@property
	def AvailableDynamicUpdateFields(self):
		"""(Read only) Specifies the available Dynamic Updates support.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableDynamicUpdateFields')

	@property
	def AvailableSessionAwareTrafficFields(self):
		"""(Read only) Specifies the available Kill Bit support.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableSessionAwareTrafficFields')

	@property
	def EnabledDynamicUpdateFields(self):
		"""If true, enables the Dynamic Updates support.

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledDynamicUpdateFields')
	@EnabledDynamicUpdateFields.setter
	def EnabledDynamicUpdateFields(self, value):
		self._set_attribute('enabledDynamicUpdateFields', value)

	@property
	def EnabledDynamicUpdateFieldsDisplayNames(self):
		"""Returns user friendly list of dynamic update fields

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledDynamicUpdateFieldsDisplayNames')

	@property
	def EnabledSessionAwareTrafficFields(self):
		"""If true, enables the Kill Bit support.

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledSessionAwareTrafficFields')
	@EnabledSessionAwareTrafficFields.setter
	def EnabledSessionAwareTrafficFields(self, value):
		self._set_attribute('enabledSessionAwareTrafficFields', value)
