from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableHardware(Base):
	"""This is the hierachy of the available hardware.
	"""

	_SDM_NAME = 'availableHardware'

	def __init__(self, parent):
		super(AvailableHardware, self).__init__(parent)

	def Chassis(self, ChassisType=None, ChassisVersion=None, Hostname=None, Ip=None, IxnBuildNumber=None, IxosBuildNumber=None, MasterChassis=None, ProtocolBuildNumber=None):
		"""Gets child instances of Chassis from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Chassis will be returned.

		Args:
			ChassisType (str): The type of chassis.
			ChassisVersion (str): The version of the Chassis in use.
			Hostname (str): The IP address associated with the chassis.
			Ip (str): The IP address associated with the chassis.
			IxnBuildNumber (str): IxNetwork build number.
			IxosBuildNumber (str): The IxOS version of the Chassis in use.
			MasterChassis (str): Specify the hostname of the master chassis on a slave chassis. Must be left blank on master. Must be set only after the chassis hostname has been set and committed on the current chassis.
			ProtocolBuildNumber (str): The Protocols version of the Chassis in use.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.chassis.Chassis))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.chassis import Chassis
		return self._select(Chassis(self), locals())

	def add_Chassis(self, CableLength="3.0", ChainTopology="daisy", Hostname=None, MasterChassis=None, SequenceId="0"):
		"""Adds a child instance of Chassis on the server.

		Args:
			CableLength (number): Specifies the length of the cable between two adjacent chassis. Must be set only after the chassis hostname has been set and committed on the current chassis.
			ChainTopology (str(daisy|none|star)): The chain topology type. This must be defined on the master chassis. It must be defined only after the chassis host name has been specified and applied on the current chassis. For legacy chassis chains, the daisy chainTopology should be indicated.
			Hostname (str): The IP address associated with the chassis.
			MasterChassis (str): Specify the hostname of the master chassis on a slave chassis. Must be left blank on master. Must be set only after the chassis hostname has been set and committed on the current chassis.
			SequenceId (number): Indicates the order at which the chassis in a chassis chain are pulsed by IxOS. Star topology chains are automatically setting this value. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.chassis.Chassis)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.chassis import Chassis
		return self._create(Chassis(self), locals())

	@property
	def IsLocked(self):
		"""If true, locks the Hardware Manager.

		Returns:
			bool
		"""
		return self._get_attribute('isLocked')

	@property
	def IsOffChassis(self):
		"""If true, the Hardware Manager is Off Chassis.

		Returns:
			bool
		"""
		return self._get_attribute('isOffChassis')
	@IsOffChassis.setter
	def IsOffChassis(self, value):
		self._set_attribute('isOffChassis', value)

	@property
	def OffChassisHwM(self):
		"""Enables the Off Chassis Hardware Manager. The Hardware Manager is an IxOS component that manages the resources on an Ixia chassis. IxNetwork communicates with a chassis through Hardware Manager. Normally, Hardware Manager runs on the chassis itself; however, it can also be installed and run on a separate PC. This configuration is known as an Off-Chassis Hardware Manager.

		Returns:
			str
		"""
		return self._get_attribute('offChassisHwM')
	@OffChassisHwM.setter
	def OffChassisHwM(self, value):
		self._set_attribute('offChassisHwM', value)
