from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TapSettings(Base):
	"""The TAP values.
	"""

	_SDM_NAME = 'tapSettings'

	def __init__(self, parent):
		super(TapSettings, self).__init__(parent)

	def Parameter(self, CurrentValue=None, CustomDefaultValue=None, DefaultValue=None, MaxValue=None, MinValue=None, Name=None):
		"""Gets child instances of Parameter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Parameter will be returned.

		Args:
			CurrentValue (str): Parameter UI Display Value
			CustomDefaultValue (str): Parameter Custom Default Value
			DefaultValue (str): Parameter Default Value
			MaxValue (str): Parameter Maximum Value
			MinValue (str): Parameter Minimum Value
			Name (str): Parameter Name.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.tapsettings.parameter.parameter.Parameter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.tapsettings.parameter.parameter import Parameter
		return self._select(Parameter(self), locals())
