from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Vport(Base):
	"""This is the virtual port hierarchy, which is used to configure IxNetwork.
	"""

	_SDM_NAME = 'vport'

	def __init__(self, parent):
		super(Vport, self).__init__(parent)

	@property
	def Capture(self):
		"""Returns the one and only one Capture object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.capture.Capture)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.capture import Capture
		return self._read(Capture(self), None)

	def DiscoveredNeighbor(self, IsRouter=None, LastUpdate=None, NeighborIp=None, NeighborMac=None):
		"""Gets child instances of DiscoveredNeighbor from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DiscoveredNeighbor will be returned.

		Args:
			IsRouter (str): (read only) Indicates if the neighbor is a router or not.
			LastUpdate (str): (read only) Indicates when the last update for the neighbor happened.
			NeighborIp (str): (read only) The IP address of the neighbor.
			NeighborMac (str): (read only) The MAC address of the neighbor.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.discoveredneighbor.discoveredneighbor.DiscoveredNeighbor))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.discoveredneighbor.discoveredneighbor import DiscoveredNeighbor
		return self._select(DiscoveredNeighbor(self), locals())

	def add_DiscoveredNeighbor(self):
		"""Adds a child instance of DiscoveredNeighbor on the server.

		Args:

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.discoveredneighbor.discoveredneighbor.DiscoveredNeighbor)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.discoveredneighbor.discoveredneighbor import DiscoveredNeighbor
		return self._create(DiscoveredNeighbor(self), locals())

	def Interface(self, Description=None, Eui64Id=None):
		"""Gets child instances of Interface from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Interface will be returned.

		Args:
			Description (str): The identifier for the port including card and port numbers, and the port type.
			Eui64Id (str): This is the 64-bit IEEE Modified EUI ID value for the Interface Identifier portion of the IPv6 address.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.interface.Interface))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.interface import Interface
		return self._select(Interface(self), locals())

	def add_Interface(self, Description="", Enabled="False", Eui64Id=None, Mtu="1500", Type="default"):
		"""Adds a child instance of Interface on the server.

		Args:
			Description (str): The identifier for the port including card and port numbers, and the port type.
			Enabled (bool): Enables the selected protocol interface.
			Eui64Id (str): This is the 64-bit IEEE Modified EUI ID value for the Interface Identifier portion of the IPv6 address.
			Mtu (number): The maximum transmission unit for the interfaces created with this range.
			Type (str(default|gre|routed)): The identifier or 'tag' for this DHCP option.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.interface.Interface)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.interface import Interface
		return self._create(Interface(self), locals())

	@property
	def InterfaceDiscoveredAddress(self):
		"""Returns the one and only one InterfaceDiscoveredAddress object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interfacediscoveredaddress.interfacediscoveredaddress.InterfaceDiscoveredAddress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interfacediscoveredaddress.interfacediscoveredaddress import InterfaceDiscoveredAddress
		return self._read(InterfaceDiscoveredAddress(self), None)

	@property
	def L1Config(self):
		"""Returns the one and only one L1Config object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.l1config.L1Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.l1config import L1Config
		return self._read(L1Config(self), None)

	@property
	def RateControlParameters(self):
		"""Returns the one and only one RateControlParameters object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.ratecontrolparameters.ratecontrolparameters.RateControlParameters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.ratecontrolparameters.ratecontrolparameters import RateControlParameters
		return self._read(RateControlParameters(self), None)

	@property
	def ActualSpeed(self):
		"""The actual speed.

		Returns:
			number
		"""
		return self._get_attribute('actualSpeed')

	@property
	def AssignedTo(self):
		"""(Read Only) A new port is assigned with this option.

		Returns:
			str
		"""
		return self._get_attribute('assignedTo')

	@property
	def CardDescription(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cardDescription')
	@CardDescription.setter
	def CardDescription(self, value):
		self._set_attribute('cardDescription', value)

	@property
	def ConnectedTo(self):
		"""The physical port to which the unassigned port is assigned.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port)
		"""
		return self._get_attribute('connectedTo')
	@ConnectedTo.setter
	def ConnectedTo(self, value):
		self._set_attribute('connectedTo', value)

	@property
	def ConnectionInfo(self):
		"""Detailed information about location of the physical port that is assigned to this port configuration.

		Returns:
			str
		"""
		return self._get_attribute('connectionInfo')

	@property
	def ConnectionState(self):
		"""Consolidated state of the vport. This combines the connection state with link state.

		Returns:
			str(assignedInUseByOther|assignedUnconnected|connectedLinkDown|connectedLinkUp|connecting|unassigned)
		"""
		return self._get_attribute('connectionState')

	@property
	def ConnectionStatus(self):
		"""A string describing the status of the hardware connected to this vport

		Returns:
			str
		"""
		return self._get_attribute('connectionStatus')

	@property
	def InternalId(self):
		"""For internal use.

		Returns:
			number
		"""
		return self._get_attribute('internalId')

	@property
	def IsAvailable(self):
		"""If true, this virtual port is available for assigning to a physical port.

		Returns:
			bool
		"""
		return self._get_attribute('isAvailable')

	@property
	def IsConnected(self):
		"""If true, indicates that the port is connected.

		Returns:
			bool
		"""
		return self._get_attribute('isConnected')

	@property
	def IsMapped(self):
		"""If true, this virtual port is mapped.

		Returns:
			bool
		"""
		return self._get_attribute('isMapped')

	@property
	def IsPullOnly(self):
		"""(This action only affects assigned ports.) This action will temporarily set the port as an Unassigned Port. This function is used to pull the configuration set by a Tcl script or an IxExplorer port file into the IxNetwork configuration.

		Returns:
			bool
		"""
		return self._get_attribute('isPullOnly')
	@IsPullOnly.setter
	def IsPullOnly(self, value):
		self._set_attribute('isPullOnly', value)

	@property
	def IsVMPort(self):
		"""If true the hardware connected to this vport is a virtual machine port

		Returns:
			bool
		"""
		return self._get_attribute('isVMPort')

	@property
	def IxnChassisVersion(self):
		"""(Read Only) If true, the installer installs the same resources as installed by the IxNetwork Full installer/IxNetwork Chassis installer on chassis.

		Returns:
			str
		"""
		return self._get_attribute('ixnChassisVersion')

	@property
	def IxnClientVersion(self):
		"""(Read Only) If true, this installs full client side IxNetwork or IxNetwork-FT components.

		Returns:
			str
		"""
		return self._get_attribute('ixnClientVersion')

	@property
	def IxosChassisVersion(self):
		"""(Read Only) If true, the installer installs the same resources as installed by IxOS on a chassis.

		Returns:
			str
		"""
		return self._get_attribute('ixosChassisVersion')

	@property
	def Licenses(self):
		"""Number of licenses.

		Returns:
			str
		"""
		return self._get_attribute('licenses')

	@property
	def Name(self):
		"""The description of the port: (1) For an assigned port, the format is: (Port type) (card no.): (port no.) - (chassis name or IP). (2) For an (unassigned) port configuration, the format is: (Port type) Port 00x.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def RxMode(self):
		"""The receive mode of the virtual port.

		Returns:
			str(capture|captureAndMeasure|measure|packetImpairment)
		"""
		return self._get_attribute('rxMode')
	@RxMode.setter
	def RxMode(self, value):
		self._set_attribute('rxMode', value)

	@property
	def State(self):
		"""The virtual port state.

		Returns:
			str(busy|down|unassigned|up|versionMismatch)
		"""
		return self._get_attribute('state')

	@property
	def StateDetail(self):
		"""This attribute describes the state of the port.

		Returns:
			str(busy|cpuNotReady|idle|inActive|l1ConfigFailed|protocolsNotSupported|versionMismatched|waitingForCPUStatus)
		"""
		return self._get_attribute('stateDetail')

	@property
	def TransmitIgnoreLinkStatus(self):
		"""If true, the port ingores the link status when transmitting data.

		Returns:
			bool
		"""
		return self._get_attribute('transmitIgnoreLinkStatus')
	@TransmitIgnoreLinkStatus.setter
	def TransmitIgnoreLinkStatus(self, value):
		self._set_attribute('transmitIgnoreLinkStatus', value)

	@property
	def TxGapControlMode(self):
		"""This object controls the Gap Control mode of the port.

		Returns:
			str(averageMode|fixedMode)
		"""
		return self._get_attribute('txGapControlMode')
	@TxGapControlMode.setter
	def TxGapControlMode(self, value):
		self._set_attribute('txGapControlMode', value)

	@property
	def TxMode(self):
		"""The transmit mode.

		Returns:
			str(interleaved|interleavedCoarse|packetImpairment|sequential|sequentialCoarse)
		"""
		return self._get_attribute('txMode')
	@TxMode.setter
	def TxMode(self, value):
		self._set_attribute('txMode', value)

	@property
	def Type(self):
		"""The type of port selection.

		Returns:
			str(atlasFourHundredGigLan|atlasFourHundredGigLanFcoe|atm|ethernet|ethernetFcoe|ethernetImpairment|ethernetvm|fc|fortyGigLan|fortyGigLanFcoe|hundredGigLan|hundredGigLanFcoe|krakenFourHundredGigLan|novusHundredGigLan|novusHundredGigLanFcoe|novusTenGigLan|novusTenGigLanFcoe|pos|tenFortyHundredGigLan|tenFortyHundredGigLanFcoe|tenGigLan|tenGigLanFcoe|tenGigWan|tenGigWanFcoe)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def ValidTxModes(self):
		"""

		Returns:
			list(str[interleaved|interleavedCoarse|packetImpairment|sequential|sequentialCoarse])
		"""
		return self._get_attribute('validTxModes')

	def remove(self):
		"""Deletes a child instance of Vport on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def AddQuickFlowGroups(self, Arg1, Arg2):
		"""Executes the addQuickFlowGroups operation on the server.

		Add quick flow traffic items to the configuration.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])): An array of valid virtual port object references.
			Arg2 (number): The number of quick flow groups to add.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('addQuickFlowGroups', payload=locals(), response_object=None)

	def ClearNeighborSolicitation(self, Arg1):
		"""Executes the clearNeighborSolicitation operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearNeighborSolicitation', payload=locals(), response_object=None)

	def ClearNeighborSolicitation(self):
		"""Executes the clearNeighborSolicitation operation on the server.

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearNeighborSolicitation', payload=locals(), response_object=None)

	def ClearNeighborTable(self):
		"""Executes the clearNeighborTable operation on the server.

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearNeighborTable', payload=locals(), response_object=None)

	def ClearPortTransmitDuration(self, Arg1):
		"""Executes the clearPortTransmitDuration operation on the server.

		Clear the port transmit duration.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearPortTransmitDuration', payload=locals(), response_object=None)

	def ConnectPort(self, Arg1):
		"""Executes the connectPort operation on the server.

		Connect a list of ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('connectPort', payload=locals(), response_object=None)

	def ConnectPorts(self, Arg1):
		"""Executes the connectPorts operation on the server.

		Connect a list of ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('connectPorts', payload=locals(), response_object=None)

	def EnableOAM(self, Arg1, Arg2):
		"""Executes the enableOAM operation on the server.

		Enable/Disable OAM on a list of ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.
			Arg2 (bool): If true, it will enable OAM. Otherwise, it will disable OAM.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('enableOAM', payload=locals(), response_object=None)

	def IgmpJoin(self, Arg2):
		"""Executes the igmpJoin operation on the server.

		Args:
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('igmpJoin', payload=locals(), response_object=None)

	def IgmpJoin(self, Arg2, Arg3):
		"""Executes the igmpJoin operation on the server.

		Args:
			Arg2 (str): 
			Arg3 (number): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('igmpJoin', payload=locals(), response_object=None)

	def IgmpLeave(self, Arg2):
		"""Executes the igmpLeave operation on the server.

		Args:
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('igmpLeave', payload=locals(), response_object=None)

	def IgmpLeave(self, Arg2, Arg3):
		"""Executes the igmpLeave operation on the server.

		Args:
			Arg2 (str): 
			Arg3 (number): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('igmpLeave', payload=locals(), response_object=None)

	def Import(self, Arg2):
		"""Executes the import operation on the server.

		Imports the port file (also supports legacy port files).

		Args:
			Arg2 (obj(ixnetwork_restpy.files.Files)): The file to be imported.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg2, Files)
		return self._execute('import', payload=locals(), response_object=None)

	def LinkUpDn(self, Arg1, Arg2):
		"""Executes the linkUpDn operation on the server.

		Simulate port link up/down.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.
			Arg2 (str(down|up)): A valid enum value as specified by the restriction.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('linkUpDn', payload=locals(), response_object=None)

	def PullPort(self):
		"""Executes the pullPort operation on the server.

		Pulls config onto vport or group of vports.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('pullPort', payload=locals(), response_object=None)

	def RefreshUnresolvedNeighbors(self):
		"""Executes the refreshUnresolvedNeighbors operation on the server.

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('refreshUnresolvedNeighbors', payload=locals(), response_object=None)

	def ReleasePort(self, Arg1):
		"""Executes the releasePort operation on the server.

		Release a hardware port.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('releasePort', payload=locals(), response_object=None)

	def ResetPortCpu(self, Arg1):
		"""Executes the resetPortCpu operation on the server.

		Reboot port CPU.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resetPortCpu', payload=locals(), response_object=None)

	def ResetPortCpuAndFactoryDefault(self, Arg1):
		"""Executes the resetPortCpuAndFactoryDefault operation on the server.

		Reboots the port CPU and restores the default settings.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resetPortCpuAndFactoryDefault', payload=locals(), response_object=None)

	def RestartPppNegotiation(self):
		"""Executes the restartPppNegotiation operation on the server.

		Restarts the PPP negotiation on the port.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('restartPppNegotiation', payload=locals(), response_object=None)

	def SendArp(self):
		"""Executes the sendArp operation on the server.

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendArp', payload=locals(), response_object=None)

	def SendArp(self, Arg2):
		"""Executes the sendArp operation on the server.

		Args:
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface])): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendArp', payload=locals(), response_object=None)

	def SendArpAll(self, Arg1):
		"""Executes the sendArpAll operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('sendArpAll', payload=locals(), response_object=None)

	def SendNs(self):
		"""Executes the sendNs operation on the server.

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendNs', payload=locals(), response_object=None)

	def SendNs(self, Arg2):
		"""Executes the sendNs operation on the server.

		Args:
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface])): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendNs', payload=locals(), response_object=None)

	def SendNsAll(self, Arg1):
		"""Executes the sendNsAll operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('sendNsAll', payload=locals(), response_object=None)

	def SendRs(self):
		"""Executes the sendRs operation on the server.

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendRs', payload=locals(), response_object=None)

	def SendRs(self, Arg2):
		"""Executes the sendRs operation on the server.

		Args:
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface])): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendRs', payload=locals(), response_object=None)

	def SendRsAll(self, Arg1):
		"""Executes the sendRsAll operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('sendRsAll', payload=locals(), response_object=None)

	def SetFactoryDefaults(self, Arg1):
		"""Executes the setFactoryDefaults operation on the server.

		Set default values for port settings.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): An array of valid ports references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('setFactoryDefaults', payload=locals(), response_object=None)

	def StartStatelessTraffic(self, Arg1):
		"""Executes the startStatelessTraffic operation on the server.

		Start the traffic configuration for stateless traffic items only.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startStatelessTraffic', payload=locals(), response_object=None)

	def StartStatelessTrafficBlocking(self, Arg1):
		"""Executes the startStatelessTrafficBlocking operation on the server.

		Start the traffic configuration for stateless traffic items only. This will block until traffic is fully started.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startStatelessTrafficBlocking', payload=locals(), response_object=None)

	def StopStatelessTraffic(self, Arg1):
		"""Executes the stopStatelessTraffic operation on the server.

		Stop the stateless traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopStatelessTraffic', payload=locals(), response_object=None)

	def StopStatelessTrafficBlocking(self, Arg1):
		"""Executes the stopStatelessTrafficBlocking operation on the server.

		Stop the traffic configuration for stateless traffic items only. This will block until traffic is fully stopped.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopStatelessTrafficBlocking', payload=locals(), response_object=None)

	def UnassignPorts(self, Arg1, Arg2):
		"""Executes the unassignPorts operation on the server.

		Unassign hardware ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): A list of ports to be unassigned.
			Arg2 (bool): If true, virtual ports will be deleted.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('unassignPorts', payload=locals(), response_object=None)
