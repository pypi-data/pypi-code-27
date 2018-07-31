from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceUpdateSrEroSubObjectList(Base):
	"""
	"""

	_SDM_NAME = 'pceUpdateSrEroSubObjectList'

	def __init__(self, parent):
		super(PceUpdateSrEroSubObjectList, self).__init__(parent)

	@property
	def ActiveThisEro(self):
		"""Controls whether the ERO sub-object will be sent in the PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('activeThisEro')

	@property
	def Bos(self):
		"""This bit is set to true for the last entry in the label stack i.e., for the bottom of the stack, and false for all other label stack entries. This control will be editable only if SID Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bos')

	@property
	def FBit(self):
		"""A Flag which is used to carry additional information pertaining to SID. When this bit is set, the NAI value in the subobject body is null.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fBit')

	@property
	def Ipv4NodeId(self):
		"""IPv4 Node ID is specified as an IPv4 address. This control can be configured if NAI Type is set to IPv4 Node ID and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4NodeId')

	@property
	def Ipv6NodeId(self):
		"""IPv6 Node ID is specified as an IPv6 address. This control can be configured if NAI Type is set to IPv6 Node ID and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6NodeId')

	@property
	def LocalInterfaceId(self):
		"""This is the Local Interface ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localInterfaceId')

	@property
	def LocalIpv4Address(self):
		"""This Control can be configured if NAI Type is set to IPv4 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localIpv4Address')

	@property
	def LocalIpv6Address(self):
		"""This Control can be configured if NAI Type is set to IPv6 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localIpv6Address')

	@property
	def LocalNodeId(self):
		"""This is the Local Node ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localNodeId')

	@property
	def LooseHop(self):
		"""Indicates if user wants to represent a loose-hop sub object in the LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('looseHop')

	@property
	def MplsLabel(self):
		"""This control will be editable if the SID Type is set to either 20bit or 32bit MPLS-Label. This field will take the 20bit value of the MPLS-Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mplsLabel')

	@property
	def MplsLabel32(self):
		"""MPLS Label 32 Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mplsLabel32')

	@property
	def NaiType(self):
		"""NAI (Node or Adjacency Identifier) contains the NAI associated with the SID. Depending on the value of SID Type, the NAI can have different formats such as, Not Applicable IPv4 Node ID IPv6 Node ID IPv4 Adjacency IPv6 Adjacency Unnumbered Adjacency with IPv4 NodeIDs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('naiType')

	@property
	def RemoteInterfaceId(self):
		"""This is the Remote Interface ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteInterfaceId')

	@property
	def RemoteIpv4Address(self):
		"""This Control can be configured if NAI Type is set to IPv4 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteIpv4Address')

	@property
	def RemoteIpv6Address(self):
		"""This Control can be configured if NAI Type is set to IPv6 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteIpv6Address')

	@property
	def RemoteNodeId(self):
		"""This is the Remote Node ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteNodeId')

	@property
	def Sid(self):
		"""SID is the Segment Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sid')

	@property
	def SidType(self):
		"""Using the Segment Identifier Type control user can configure whether to include SID or not and if included what is its type. Types are as follows: Null SID 20bit MPLS Label 32bit MPLS Label. If it is Null then S bit is set in the packet. Default value is 20bit MPLS Label.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sidType')

	@property
	def Tc(self):
		"""This field is used to carry traffic class information. This control will be editable only if SID Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tc')

	@property
	def Ttl(self):
		"""This field is used to encode a time-to-live value. This control will be editable only if SID Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ttl')

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
