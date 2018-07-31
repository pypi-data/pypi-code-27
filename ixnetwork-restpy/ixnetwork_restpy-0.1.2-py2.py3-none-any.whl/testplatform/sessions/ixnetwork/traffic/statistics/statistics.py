from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistics(Base):
	"""This object fetches all the traffic statistics.
	"""

	_SDM_NAME = 'statistics'

	def __init__(self, parent):
		super(Statistics, self).__init__(parent)

	@property
	def AdvancedSequenceChecking(self):
		"""Returns the one and only one AdvancedSequenceChecking object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.advancedsequencechecking.advancedsequencechecking.AdvancedSequenceChecking)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.advancedsequencechecking.advancedsequencechecking import AdvancedSequenceChecking
		return self._read(AdvancedSequenceChecking(self), None)

	@property
	def CpdpConvergence(self):
		"""Returns the one and only one CpdpConvergence object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.cpdpconvergence.cpdpconvergence.CpdpConvergence)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.cpdpconvergence.cpdpconvergence import CpdpConvergence
		return self._read(CpdpConvergence(self), None)

	@property
	def DataIntegrity(self):
		"""Returns the one and only one DataIntegrity object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.dataintegrity.dataintegrity.DataIntegrity)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.dataintegrity.dataintegrity import DataIntegrity
		return self._read(DataIntegrity(self), None)

	@property
	def DelayVariation(self):
		"""Returns the one and only one DelayVariation object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.delayvariation.delayvariation.DelayVariation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.delayvariation.delayvariation import DelayVariation
		return self._read(DelayVariation(self), None)

	@property
	def ErrorStats(self):
		"""Returns the one and only one ErrorStats object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.errorstats.errorstats.ErrorStats)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.errorstats.errorstats import ErrorStats
		return self._read(ErrorStats(self), None)

	@property
	def InterArrivalTimeRate(self):
		"""Returns the one and only one InterArrivalTimeRate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.interarrivaltimerate.interarrivaltimerate.InterArrivalTimeRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.interarrivaltimerate.interarrivaltimerate import InterArrivalTimeRate
		return self._read(InterArrivalTimeRate(self), None)

	@property
	def Iptv(self):
		"""Returns the one and only one Iptv object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.iptv.iptv.Iptv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.iptv.iptv import Iptv
		return self._read(Iptv(self), None)

	@property
	def L1Rates(self):
		"""Returns the one and only one L1Rates object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.l1rates.l1rates.L1Rates)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.l1rates.l1rates import L1Rates
		return self._read(L1Rates(self), None)

	@property
	def Latency(self):
		"""Returns the one and only one Latency object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.latency.latency.Latency)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.latency.latency import Latency
		return self._read(Latency(self), None)

	@property
	def MisdirectedPerFlow(self):
		"""Returns the one and only one MisdirectedPerFlow object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.misdirectedperflow.misdirectedperflow.MisdirectedPerFlow)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.misdirectedperflow.misdirectedperflow import MisdirectedPerFlow
		return self._read(MisdirectedPerFlow(self), None)

	@property
	def MultipleJoinLeaveLatency(self):
		"""Returns the one and only one MultipleJoinLeaveLatency object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.multiplejoinleavelatency.multiplejoinleavelatency.MultipleJoinLeaveLatency)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.multiplejoinleavelatency.multiplejoinleavelatency import MultipleJoinLeaveLatency
		return self._read(MultipleJoinLeaveLatency(self), None)

	@property
	def OneTimeJoinLeaveLatency(self):
		"""Returns the one and only one OneTimeJoinLeaveLatency object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.onetimejoinleavelatency.onetimejoinleavelatency.OneTimeJoinLeaveLatency)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.onetimejoinleavelatency.onetimejoinleavelatency import OneTimeJoinLeaveLatency
		return self._read(OneTimeJoinLeaveLatency(self), None)

	@property
	def PacketLossDuration(self):
		"""Returns the one and only one PacketLossDuration object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.packetlossduration.packetlossduration.PacketLossDuration)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.packetlossduration.packetlossduration import PacketLossDuration
		return self._read(PacketLossDuration(self), None)

	@property
	def Prbs(self):
		"""Returns the one and only one Prbs object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.prbs.prbs.Prbs)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.prbs.prbs import Prbs
		return self._read(Prbs(self), None)

	@property
	def SequenceChecking(self):
		"""Returns the one and only one SequenceChecking object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.sequencechecking.sequencechecking.SequenceChecking)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.sequencechecking.sequencechecking import SequenceChecking
		return self._read(SequenceChecking(self), None)
