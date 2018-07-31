from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Tracking(Base):
	"""This object provides different options for tracking.
	"""

	_SDM_NAME = 'tracking'

	def __init__(self, parent):
		super(Tracking, self).__init__(parent)

	@property
	def Egress(self):
		"""Returns the one and only one Egress object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.egress.egress.Egress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.egress.egress import Egress
		return self._read(Egress(self), None)

	@property
	def LatencyBin(self):
		"""Returns the one and only one LatencyBin object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.latencybin.latencybin.LatencyBin)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.latencybin.latencybin import LatencyBin
		return self._read(LatencyBin(self), None)

	@property
	def AvailableProtocolOffsets(self):
		"""Specifies the available Protocol Offsets when the Flows of a Traffic Item are tracked by Custom Override.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableProtocolOffsets')

	@property
	def AvailableTrackBy(self):
		"""Returns list of available tracking field ids

		Returns:
			list(str)
		"""
		return self._get_attribute('availableTrackBy')

	@property
	def AvailableTrackByInfos(self):
		"""Returns list of tracking fields with id/displayname

		Returns:
			list(dict(arg1:str,arg2:str))
		"""
		return self._get_attribute('availableTrackByInfos')

	@property
	def FieldWidth(self):
		"""Specifies the Field Width when the flows of a Traffic Item are tracked by Custom Override.

		Returns:
			str(eightBits|sixteenBits|thirtyTwoBits|twentyFourBits)
		"""
		return self._get_attribute('fieldWidth')
	@FieldWidth.setter
	def FieldWidth(self, value):
		self._set_attribute('fieldWidth', value)

	@property
	def Offset(self):
		"""Specifies the Offset when the Flows of a Traffic Item are tracked by Custom Override.

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def OneToOneMesh(self):
		"""If true, one-one mesh is enabled when flows of a traffic item are tracked by Custom Override.

		Returns:
			bool
		"""
		return self._get_attribute('oneToOneMesh')
	@OneToOneMesh.setter
	def OneToOneMesh(self, value):
		self._set_attribute('oneToOneMesh', value)

	@property
	def ProtocolOffset(self):
		"""Specifies the Protocol Offset when flows of a Traffic Item are tracked by Custom Override.

		Returns:
			str
		"""
		return self._get_attribute('protocolOffset')
	@ProtocolOffset.setter
	def ProtocolOffset(self, value):
		self._set_attribute('protocolOffset', value)

	@property
	def TrackBy(self):
		"""Specifies the tracking option by which the Flows of a Traffic Item are tracked.

		Returns:
			list(str)
		"""
		return self._get_attribute('trackBy')
	@TrackBy.setter
	def TrackBy(self, value):
		self._set_attribute('trackBy', value)

	@property
	def Values(self):
		"""Specifies the Values when the Flows of a Traffic Item are tracked by Custom Override.

		Returns:
			list(str)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)
