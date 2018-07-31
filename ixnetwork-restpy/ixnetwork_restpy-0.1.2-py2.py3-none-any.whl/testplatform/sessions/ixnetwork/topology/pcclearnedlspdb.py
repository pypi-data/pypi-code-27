from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PccLearnedLspDb(Base):
	"""PCC Learned LSPs Information Database
	"""

	_SDM_NAME = 'pccLearnedLspDb'

	def __init__(self, parent):
		super(PccLearnedLspDb, self).__init__(parent)

	@property
	def DestIpv4Address(self):
		"""Returns the one and only one DestIpv4Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv4address.DestIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv4address import DestIpv4Address
		return self._read(DestIpv4Address(self), None)

	@property
	def DestIpv6Address(self):
		"""Returns the one and only one DestIpv6Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv6address.DestIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv6address import DestIpv6Address
		return self._read(DestIpv6Address(self), None)

	@property
	def ErrorInfo(self):
		"""Returns the one and only one ErrorInfo object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.errorinfo.ErrorInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.errorinfo import ErrorInfo
		return self._read(ErrorInfo(self), None)

	@property
	def IpVersion(self):
		"""Returns the one and only one IpVersion object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipversion.IpVersion)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipversion import IpVersion
		return self._read(IpVersion(self), None)

	@property
	def Ipv4NodeId(self):
		"""Returns the one and only one Ipv4NodeId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4nodeid.Ipv4NodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4nodeid import Ipv4NodeId
		return self._read(Ipv4NodeId(self), None)

	@property
	def Ipv6NodeId(self):
		"""Returns the one and only one Ipv6NodeId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6nodeid.Ipv6NodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6nodeid import Ipv6NodeId
		return self._read(Ipv6NodeId(self), None)

	@property
	def LearnedLspIndex(self):
		"""Returns the one and only one LearnedLspIndex object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedlspindex.LearnedLspIndex)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedlspindex import LearnedLspIndex
		return self._read(LearnedLspIndex(self), None)

	@property
	def LearnedMsgDbType(self):
		"""Returns the one and only one LearnedMsgDbType object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedmsgdbtype.LearnedMsgDbType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedmsgdbtype import LearnedMsgDbType
		return self._read(LearnedMsgDbType(self), None)

	@property
	def LocalIntefaceId(self):
		"""Returns the one and only one LocalIntefaceId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localintefaceid.LocalIntefaceId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localintefaceid import LocalIntefaceId
		return self._read(LocalIntefaceId(self), None)

	@property
	def LocalIpv4Address(self):
		"""Returns the one and only one LocalIpv4Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv4address.LocalIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv4address import LocalIpv4Address
		return self._read(LocalIpv4Address(self), None)

	@property
	def LocalIpv6Address(self):
		"""Returns the one and only one LocalIpv6Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv6address.LocalIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv6address import LocalIpv6Address
		return self._read(LocalIpv6Address(self), None)

	@property
	def LocalNodeId(self):
		"""Returns the one and only one LocalNodeId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localnodeid.LocalNodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localnodeid import LocalNodeId
		return self._read(LocalNodeId(self), None)

	@property
	def MplsLabel(self):
		"""Returns the one and only one MplsLabel object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplslabel.MplsLabel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplslabel import MplsLabel
		return self._read(MplsLabel(self), None)

	@property
	def PlspId(self):
		"""Returns the one and only one PlspId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.plspid.PlspId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.plspid import PlspId
		return self._read(PlspId(self), None)

	@property
	def RemoteInterfaceId(self):
		"""Returns the one and only one RemoteInterfaceId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteinterfaceid.RemoteInterfaceId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteinterfaceid import RemoteInterfaceId
		return self._read(RemoteInterfaceId(self), None)

	@property
	def RemoteIpv4Address(self):
		"""Returns the one and only one RemoteIpv4Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv4address.RemoteIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv4address import RemoteIpv4Address
		return self._read(RemoteIpv4Address(self), None)

	@property
	def RemoteIpv6Address(self):
		"""Returns the one and only one RemoteIpv6Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv6address.RemoteIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv6address import RemoteIpv6Address
		return self._read(RemoteIpv6Address(self), None)

	@property
	def RemoteNodeId(self):
		"""Returns the one and only one RemoteNodeId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remotenodeid.RemoteNodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remotenodeid import RemoteNodeId
		return self._read(RemoteNodeId(self), None)

	@property
	def RequestId(self):
		"""Returns the one and only one RequestId object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestid.RequestId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestid import RequestId
		return self._read(RequestId(self), None)

	@property
	def Sid(self):
		"""Returns the one and only one Sid object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sid.Sid)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sid import Sid
		return self._read(Sid(self), None)

	@property
	def SidType(self):
		"""Returns the one and only one SidType object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype.SidType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype import SidType
		return self._read(SidType(self), None)

	@property
	def SidType(self):
		"""Returns the one and only one SidType object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype.SidType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype import SidType
		return self._read(SidType(self), None)

	@property
	def SourceIpv4Address(self):
		"""Returns the one and only one SourceIpv4Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv4address.SourceIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv4address import SourceIpv4Address
		return self._read(SourceIpv4Address(self), None)

	@property
	def SourceIpv6Address(self):
		"""Returns the one and only one SourceIpv6Address object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv6address.SourceIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv6address import SourceIpv6Address
		return self._read(SourceIpv6Address(self), None)

	@property
	def SymbolicPathName(self):
		"""Returns the one and only one SymbolicPathName object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.symbolicpathname.SymbolicPathName)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.symbolicpathname import SymbolicPathName
		return self._read(SymbolicPathName(self), None)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

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
