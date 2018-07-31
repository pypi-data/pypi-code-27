from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class HighLevelStream(Base):
	"""A Flow Group that is generated from the Traffic Item. Each Traffic Item generates one or more Flow Groups, which in turn map to hardware streams on the port. Each Flow Group/highLevelStream picks up its QOS, Rate, Frame size properties/attributes from its corresponding configElement configuration under the Traffic Item.
	"""

	_SDM_NAME = 'highLevelStream'

	def __init__(self, parent):
		super(HighLevelStream, self).__init__(parent)

	@property
	def FramePayload(self):
		"""Returns the one and only one FramePayload object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framepayload.framepayload.FramePayload)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framepayload.framepayload import FramePayload
		return self._read(FramePayload(self), None)

	@property
	def FrameRate(self):
		"""Returns the one and only one FrameRate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framerate.framerate.FrameRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framerate.framerate import FrameRate
		return self._read(FrameRate(self), None)

	@property
	def FrameSize(self):
		"""Returns the one and only one FrameSize object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framesize.framesize.FrameSize)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framesize.framesize import FrameSize
		return self._read(FrameSize(self), None)

	def Stack(self, DisplayName=None, StackTypeId=None, TemplateName=None):
		"""Gets child instances of Stack from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Stack will be returned.

		Args:
			DisplayName (str): The display name of the stack.
			StackTypeId (str): 
			TemplateName (str): Indiates the protocol template name that is added to a packet in a stack.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stack.stack.Stack))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stack.stack import Stack
		return self._select(Stack(self), locals())

	def StackLink(self):
		"""Gets child instances of StackLink from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of StackLink will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stacklink.stacklink.StackLink))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stacklink.stacklink import StackLink
		return self._select(StackLink(self), locals())

	def TableUdf(self):
		"""Gets child instances of TableUdf from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of TableUdf will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.tableudf.TableUdf))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.tableudf import TableUdf
		return self._select(TableUdf(self), locals())

	@property
	def TransmissionControl(self):
		"""Returns the one and only one TransmissionControl object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.transmissioncontrol.transmissioncontrol.TransmissionControl)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.transmissioncontrol.transmissioncontrol import TransmissionControl
		return self._read(TransmissionControl(self), None)

	def Udf(self):
		"""Gets child instances of Udf from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Udf will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.udf.udf.Udf))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.udf.udf import Udf
		return self._select(Udf(self), locals())

	@property
	def AppliedFrameSize(self):
		"""(Read only) Indicates the applied frame size of the high level stream.

		Returns:
			str
		"""
		return self._get_attribute('appliedFrameSize')

	@property
	def AppliedPacketCount(self):
		"""(Read only) Indicates the aplied packet count of the high level stream.

		Returns:
			number
		"""
		return self._get_attribute('appliedPacketCount')

	@property
	def Crc(self):
		"""The Cyclic Redundancy Check frame of the configured high level stream.

		Returns:
			str(badCrc|goodCrc)
		"""
		return self._get_attribute('crc')
	@Crc.setter
	def Crc(self, value):
		self._set_attribute('crc', value)

	@property
	def CurrentPacketCount(self):
		"""(Read only) Denotes the number of packets.

		Returns:
			number
		"""
		return self._get_attribute('currentPacketCount')

	@property
	def DestinationMacMode(self):
		"""The mode in which the Destination MAC Address is configured, either manual or ARP.

		Returns:
			str(arp|manual)
		"""
		return self._get_attribute('destinationMacMode')
	@DestinationMacMode.setter
	def DestinationMacMode(self, value):
		self._set_attribute('destinationMacMode', value)

	@property
	def Distributions(self):
		"""Denotes the distribution of the high level stream.

		Returns:
			list(dict(arg1:str,arg2:str))
		"""
		return self._get_attribute('distributions')

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EncapsulationName(self):
		"""Name of the configured encapsulation type.

		Returns:
			str
		"""
		return self._get_attribute('encapsulationName')

	@property
	def EndpointSetId(self):
		"""The ID of the configured endpoint set.

		Returns:
			number
		"""
		return self._get_attribute('endpointSetId')

	@property
	def Name(self):
		"""An alphanumeric string that returns the name of the field.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def OverSubscribed(self):
		"""If true, the rate is oversubscribed.

		Returns:
			bool
		"""
		return self._get_attribute('overSubscribed')

	@property
	def Pause(self):
		"""If true then pause is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('pause')
	@Pause.setter
	def Pause(self, value):
		self._set_attribute('pause', value)

	@property
	def PreambleCustomSize(self):
		"""Customizes the preamble size of the frame.

		Returns:
			number
		"""
		return self._get_attribute('preambleCustomSize')
	@PreambleCustomSize.setter
	def PreambleCustomSize(self, value):
		self._set_attribute('preambleCustomSize', value)

	@property
	def PreambleFrameSizeMode(self):
		"""The starting size of the frame.

		Returns:
			str(auto|custom)
		"""
		return self._get_attribute('preambleFrameSizeMode')
	@PreambleFrameSizeMode.setter
	def PreambleFrameSizeMode(self, value):
		self._set_attribute('preambleFrameSizeMode', value)

	@property
	def RxPortIds(self):
		"""A list of virtual ports that are the receiving ports

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('rxPortIds')
	@RxPortIds.setter
	def RxPortIds(self, value):
		self._set_attribute('rxPortIds', value)

	@property
	def RxPortNames(self):
		"""A list of names from the receiving virtual ports.

		Returns:
			list(str)
		"""
		return self._get_attribute('rxPortNames')

	@property
	def State(self):
		"""(Read only) Denotes the current state of the stream.

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def Suspend(self):
		"""Suspends all traffic on this high level stream.

		Returns:
			bool
		"""
		return self._get_attribute('suspend')
	@Suspend.setter
	def Suspend(self, value):
		self._set_attribute('suspend', value)

	@property
	def TxPortId(self):
		"""The virtual port that is the transmitting port.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)
		"""
		return self._get_attribute('txPortId')
	@TxPortId.setter
	def TxPortId(self, value):
		self._set_attribute('txPortId', value)

	@property
	def TxPortName(self):
		"""The name of the virtual port that is the transmitting port.

		Returns:
			str
		"""
		return self._get_attribute('txPortName')

	def DeleteQuickFlowGroups(self, Arg1):
		"""Executes the deleteQuickFlowGroups operation on the server.

		Deletes a list of quick flow groups.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream])): An array of valid object references.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('deleteQuickFlowGroups', payload=locals(), response_object=None)

	def PreviewFlowPackets(self, Arg2, Arg3):
		"""Executes the previewFlowPackets operation on the server.

		Preview packets for selected highLevelstream

		Args:
			Arg2 (number): 
			Arg3 (number): 

		Returns:
			dict(arg1:number,arg2:number,arg3:list[str],arg4:list[list[str]]): No return value.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('previewFlowPackets', payload=locals(), response_object=None)

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
