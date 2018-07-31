from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Chassis(Base):
	"""The chassis command is used to add a new chassis to a chain of chassis, configure an existing chassis or delete an existing one from the chain in use.
	"""

	_SDM_NAME = 'chassis'

	def __init__(self, parent):
		super(Chassis, self).__init__(parent)

	def Card(self, Description=None):
		"""Gets child instances of Card from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Card will be returned.

		Args:
			Description (str): Description of the card.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.card.Card))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.card import Card
		return self._select(Card(self), locals())

	@property
	def CableLength(self):
		"""Specifies the length of the cable between two adjacent chassis. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			number
		"""
		return self._get_attribute('cableLength')
	@CableLength.setter
	def CableLength(self, value):
		self._set_attribute('cableLength', value)

	@property
	def ChainTopology(self):
		"""The chain topology type. This must be defined on the master chassis. It must be defined only after the chassis host name has been specified and applied on the current chassis. For legacy chassis chains, the daisy chainTopology should be indicated.

		Returns:
			str(daisy|none|star)
		"""
		return self._get_attribute('chainTopology')
	@ChainTopology.setter
	def ChainTopology(self, value):
		self._set_attribute('chainTopology', value)

	@property
	def ChassisType(self):
		"""The type of chassis.

		Returns:
			str
		"""
		return self._get_attribute('chassisType')

	@property
	def ChassisVersion(self):
		"""The version of the Chassis in use.

		Returns:
			str
		"""
		return self._get_attribute('chassisVersion')

	@property
	def ConnectRetries(self):
		"""The number of time the client attempted to re-connect with the chassis. (read only)

		Returns:
			number
		"""
		return self._get_attribute('connectRetries')

	@property
	def Hostname(self):
		"""The IP address associated with the chassis.

		Returns:
			str
		"""
		return self._get_attribute('hostname')
	@Hostname.setter
	def Hostname(self, value):
		self._set_attribute('hostname', value)

	@property
	def Ip(self):
		"""The IP address associated with the chassis.

		Returns:
			str
		"""
		return self._get_attribute('ip')

	@property
	def IsLicensesRetrieved(self):
		"""Retrieves the licenses in the chassis.

		Returns:
			bool
		"""
		return self._get_attribute('isLicensesRetrieved')

	@property
	def IsMaster(self):
		"""Specifies whether this chassis is a master of a slave in a chain. There can be only one master chassis in a chain. NOTE: The master is automatically assigned based on cable connections.

		Returns:
			bool
		"""
		return self._get_attribute('isMaster')

	@property
	def IxnBuildNumber(self):
		"""IxNetwork build number.

		Returns:
			str
		"""
		return self._get_attribute('ixnBuildNumber')

	@property
	def IxosBuildNumber(self):
		"""The IxOS version of the Chassis in use.

		Returns:
			str
		"""
		return self._get_attribute('ixosBuildNumber')

	@property
	def LicenseErrors(self):
		"""Shows the licening errors that occurred due to licensing problems.

		Returns:
			list(str)
		"""
		return self._get_attribute('licenseErrors')

	@property
	def MasterChassis(self):
		"""Specify the hostname of the master chassis on a slave chassis. Must be left blank on master. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			str
		"""
		return self._get_attribute('masterChassis')
	@MasterChassis.setter
	def MasterChassis(self, value):
		self._set_attribute('masterChassis', value)

	@property
	def ProtocolBuildNumber(self):
		"""The Protocols version of the Chassis in use.

		Returns:
			str
		"""
		return self._get_attribute('protocolBuildNumber')

	@property
	def SequenceId(self):
		"""Indicates the order at which the chassis in a chassis chain are pulsed by IxOS. Star topology chains are automatically setting this value. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			number
		"""
		return self._get_attribute('sequenceId')
	@SequenceId.setter
	def SequenceId(self, value):
		self._set_attribute('sequenceId', value)

	@property
	def State(self):
		"""The following states can be read from the port: polling, ready, and down.

		Returns:
			str(down|down|polling|polling|polling|ready)
		"""
		return self._get_attribute('state')

	def remove(self):
		"""Deletes a child instance of Chassis on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def GetTapSettings(self, Arg1):
		"""Executes the getTapSettings operation on the server.

		Get TAP Settings for the given chassis

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=chassis])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getTapSettings', payload=locals(), response_object=None)

	def RefreshInfo(self, Arg1):
		"""Executes the refreshInfo operation on the server.

		Refresh the hardware information.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=chassis|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=card])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('refreshInfo', payload=locals(), response_object=None)

	def SetTapSettings(self, Arg1):
		"""Executes the setTapSettings operation on the server.

		Send TAP Settings to IxServer for the given chassis.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=chassis])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('setTapSettings', payload=locals(), response_object=None)
