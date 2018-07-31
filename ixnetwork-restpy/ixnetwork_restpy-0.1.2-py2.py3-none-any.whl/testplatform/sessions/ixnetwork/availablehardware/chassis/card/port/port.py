from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Port(Base):
	"""The physical port assigned to this port configuration.
	"""

	_SDM_NAME = 'port'

	def __init__(self, parent):
		super(Port, self).__init__(parent)

	def TapSettings(self):
		"""Gets child instances of TapSettings from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of TapSettings will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.tapsettings.tapsettings.TapSettings))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.tapsettings.tapsettings import TapSettings
		return self._select(TapSettings(self), locals())

	@property
	def Description(self):
		"""The port description/mode.

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def IsAvailable(self):
		"""The link is available on the port.

		Returns:
			bool
		"""
		return self._get_attribute('isAvailable')

	@property
	def IsBusy(self):
		"""The link is unavailable on the port.

		Returns:
			bool
		"""
		return self._get_attribute('isBusy')

	@property
	def IsLinkUp(self):
		"""The link is up on the port.

		Returns:
			bool
		"""
		return self._get_attribute('isLinkUp')

	@property
	def IsUsable(self):
		"""(read only) Returns true of false depending on whether the port can be used, based on the value of parent card aggregationMode. If card aggregationMode is notSupported and normal it always returns true. If card aggregationMode is tenGigAggregation, only the ports with index 1, 5, 9, and 13 returns true.

		Returns:
			bool
		"""
		return self._get_attribute('isUsable')

	@property
	def Owner(self):
		"""The current owner of the port.

		Returns:
			str
		"""
		return self._get_attribute('owner')

	@property
	def PortId(self):
		"""The physical port ID.

		Returns:
			number
		"""
		return self._get_attribute('portId')

	def ClearOwnership(self, Arg1):
		"""Executes the clearOwnership operation on the server.

		Clears ownership on a list of hardware ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): An array of valid ports references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearOwnership', payload=locals(), response_object=None)

	def CopyTapSettings(self, Arg2):
		"""Executes the copyTapSettings operation on the server.

		It will copy the values from a port to the given ports.

		Args:
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('copyTapSettings', payload=locals(), response_object=None)

	def DeleteCustomDefaults(self, Arg1):
		"""Executes the deleteCustomDefaults operation on the server.

		It will delete custom defaults for the given ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('deleteCustomDefaults', payload=locals(), response_object=None)

	def GetTapSettings(self, Arg1):
		"""Executes the getTapSettings operation on the server.

		Get TAP Settings for the given ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getTapSettings', payload=locals(), response_object=None)

	def RestoreCustomDefaults(self, Arg1):
		"""Executes the restoreCustomDefaults operation on the server.

		It will restore custom defaults for the given ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restoreCustomDefaults', payload=locals(), response_object=None)

	def RestoreDefaults(self, Arg1):
		"""Executes the restoreDefaults operation on the server.

		Restore de default values for the given ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restoreDefaults', payload=locals(), response_object=None)

	def SaveCustomDefaults(self, Arg1):
		"""Executes the saveCustomDefaults operation on the server.

		It will save custom defaults for the given ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('saveCustomDefaults', payload=locals(), response_object=None)

	def SetTapSettings(self, Arg1):
		"""Executes the setTapSettings operation on the server.

		Send TAP Settings to IxServer for the given ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('setTapSettings', payload=locals(), response_object=None)
