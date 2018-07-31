from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ConfigElement(Base):
	"""A grouping of endpoints under the Traffic Item per unique encapsulation/packet structure. The user sees each configElement as rows in the Pages of the wizard after the first page of the Wizard and also on the First Page under Endpoint sets as below. The user can then configure QOS, Frame Size, Rate etc per configElement. The configElements control the rate/frame size/qos properties of one or more flowGroups/highLevelStreams that are generated from the Traffic Item.
	"""

	_SDM_NAME = 'configElement'

	def __init__(self, parent):
		super(ConfigElement, self).__init__(parent)

	@property
	def FramePayload(self):
		"""Returns the one and only one FramePayload object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framepayload.framepayload.FramePayload)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framepayload.framepayload import FramePayload
		return self._read(FramePayload(self), None)

	@property
	def FrameRate(self):
		"""Returns the one and only one FrameRate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framerate.framerate.FrameRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framerate.framerate import FrameRate
		return self._read(FrameRate(self), None)

	@property
	def FrameRateDistribution(self):
		"""Returns the one and only one FrameRateDistribution object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.frameratedistribution.frameratedistribution.FrameRateDistribution)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.frameratedistribution.frameratedistribution import FrameRateDistribution
		return self._read(FrameRateDistribution(self), None)

	@property
	def FrameSize(self):
		"""Returns the one and only one FrameSize object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framesize.framesize.FrameSize)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framesize.framesize import FrameSize
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
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.stack.Stack))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.stack import Stack
		return self._select(Stack(self), locals())

	def StackLink(self):
		"""Gets child instances of StackLink from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of StackLink will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stacklink.stacklink.StackLink))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stacklink.stacklink import StackLink
		return self._select(StackLink(self), locals())

	@property
	def TransmissionControl(self):
		"""Returns the one and only one TransmissionControl object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissioncontrol.transmissioncontrol.TransmissionControl)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissioncontrol.transmissioncontrol import TransmissionControl
		return self._read(TransmissionControl(self), None)

	def TransmissionDistribution(self):
		"""Gets child instances of TransmissionDistribution from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of TransmissionDistribution will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissiondistribution.transmissiondistribution.TransmissionDistribution))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissiondistribution.transmissiondistribution import TransmissionDistribution
		return self._select(TransmissionDistribution(self), locals())

	@property
	def Crc(self):
		"""The Cyclic Redundancy Check frame of the configured encapsulation set.

		Returns:
			str(badCrc|goodCrc)
		"""
		return self._get_attribute('crc')
	@Crc.setter
	def Crc(self, value):
		self._set_attribute('crc', value)

	@property
	def DestinationMacMode(self):
		"""The destination MAC address that is to be configured.

		Returns:
			str(arp|manual)
		"""
		return self._get_attribute('destinationMacMode')
	@DestinationMacMode.setter
	def DestinationMacMode(self, value):
		self._set_attribute('destinationMacMode', value)

	@property
	def EnableDisparityError(self):
		"""If true, enables disparity error

		Returns:
			bool
		"""
		return self._get_attribute('enableDisparityError')
	@EnableDisparityError.setter
	def EnableDisparityError(self, value):
		self._set_attribute('enableDisparityError', value)

	@property
	def EncapsulationName(self):
		"""Indicates the name of the encapsulation set.

		Returns:
			str
		"""
		return self._get_attribute('encapsulationName')

	@property
	def EndpointSetId(self):
		"""Indicates the identification of the endpoint set.

		Returns:
			number
		"""
		return self._get_attribute('endpointSetId')

	@property
	def PreambleCustomSize(self):
		"""Indicates the customized preamble size of the frame.

		Returns:
			number
		"""
		return self._get_attribute('preambleCustomSize')
	@PreambleCustomSize.setter
	def PreambleCustomSize(self, value):
		self._set_attribute('preambleCustomSize', value)

	@property
	def PreambleFrameSizeMode(self):
		"""The preamble size to synchronize sender and receiver of the configured encapsulation set.

		Returns:
			str(auto|custom)
		"""
		return self._get_attribute('preambleFrameSizeMode')
	@PreambleFrameSizeMode.setter
	def PreambleFrameSizeMode(self, value):
		self._set_attribute('preambleFrameSizeMode', value)
