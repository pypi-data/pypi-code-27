from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Topology(Base):
	"""Topology represents the concept of network devices which are to be configured on a group of ports.
	"""

	_SDM_NAME = 'topology'

	def __init__(self, parent):
		super(Topology, self).__init__(parent)

	def DeviceGroup(self, DescriptiveName=None, Name=None):
		"""Gets child instances of DeviceGroup from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DeviceGroup will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup.DeviceGroup))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup import DeviceGroup
		return self._select(DeviceGroup(self), locals())

	def add_DeviceGroup(self, Multiplier="10", Name=None):
		"""Adds a child instance of DeviceGroup on the server.

		Args:
			Multiplier (number): Number of device instances per parent device instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup.DeviceGroup)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup import DeviceGroup
		return self._create(DeviceGroup(self), locals())

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def Note(self):
		"""Any Note about the Topology

		Returns:
			str
		"""
		return self._get_attribute('note')
	@Note.setter
	def Note(self, value):
		self._set_attribute('note', value)

	@property
	def PortCount(self):
		"""Number of /vports or /lags assigned (including unmapped ports)

		Returns:
			number
		"""
		return self._get_attribute('portCount')

	@property
	def Ports(self):
		"""Logical port information.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('ports')
	@Ports.setter
	def Ports(self, value):
		self._set_attribute('ports', value)

	@property
	def PortsStateCount(self):
		"""State of ports on this topology, arg1:total, arg2:up, arg3:down, arg4:other

		Returns:
			dict(arg1:number,arg2:number,arg3:number,arg4:number)
		"""
		return self._get_attribute('portsStateCount')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def Vports(self):
		"""Virtual port information.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('vports')
	@Vports.setter
	def Vports(self, value):
		self._set_attribute('vports', value)

	def remove(self):
		"""Deletes a child instance of Topology on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def AdjustPortCount(self, Arg2):
		"""Executes the adjustPortCount operation on the server.

		Adjusts the number of /vport objects in the -vports attribute by creating or deleting /vport objects and modifying the -vports attribute

		Args:
			Arg2 (number): The target number of /vport objects references in the /topology -vports attribute

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('adjustPortCount', payload=locals(), response_object=None)

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('fetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)

	def RestartDown(self, Targets):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions in Topology that are in 'Down' state.

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def Start(self, Targets):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Targets):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
