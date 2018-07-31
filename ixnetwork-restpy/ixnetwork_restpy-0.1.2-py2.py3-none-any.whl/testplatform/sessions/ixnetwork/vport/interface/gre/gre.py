from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Gre(Base):
	"""Allows the user to set up GRE tunnels from the Ixia port to the DUT port. The GRE protocol can be used to encapsulate packets of many different protocol types and tunnel them across a network of a different protocol type. This basic encapsulation method indicates the Ethertype of the payload packet, and depends on a delivery header with both Layer 2 and Layer 3 information to forward the packet across the network.
	"""

	_SDM_NAME = 'gre'

	def __init__(self, parent):
		super(Gre, self).__init__(parent)

	@property
	def Dest(self):
		"""Part of the GRE Delivery Header: The IP address of the Destination router at the remote end of the GRE tunnel.

		Returns:
			str
		"""
		return self._get_attribute('dest')
	@Dest.setter
	def Dest(self, value):
		self._set_attribute('dest', value)

	@property
	def InKey(self):
		"""This is the user-assigned GRE header authentication key value that the receiving router will check for to validate GRE packets being sent via the tunnel. All packets sent via a specific tunnel should contain the same key value (one key per GRE tunnel).

		Returns:
			number
		"""
		return self._get_attribute('inKey')
	@InKey.setter
	def InKey(self, value):
		self._set_attribute('inKey', value)

	@property
	def OutKey(self):
		"""This is the user-assigned GRE header authentication key value that will be included in the GRE packets being sent via the tunnel. All packets sent via a specific tunnel should contain the same key value (one key per GRE tunnel). In most cases, the In Key and Out Key will be the same.

		Returns:
			number
		"""
		return self._get_attribute('outKey')
	@OutKey.setter
	def OutKey(self, value):
		self._set_attribute('outKey', value)

	@property
	def Source(self):
		"""Part of the GRE Delivery Header: The IP address of the connected interface associated with the source of this GRE tunnel.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ipv4|/api/v1/sessions/1/ixnetwork/vport?deepchild=ipv6)
		"""
		return self._get_attribute('source')
	@Source.setter
	def Source(self, value):
		self._set_attribute('source', value)

	@property
	def UseChecksum(self):
		"""Enables the use of the optional GRE checksum.

		Returns:
			bool
		"""
		return self._get_attribute('useChecksum')
	@UseChecksum.setter
	def UseChecksum(self, value):
		self._set_attribute('useChecksum', value)

	@property
	def UseKey(self):
		"""Enables the use of the optional GRE header key field.

		Returns:
			bool
		"""
		return self._get_attribute('useKey')
	@UseKey.setter
	def UseKey(self, value):
		self._set_attribute('useKey', value)

	@property
	def UseSequence(self):
		"""If more than one GRE tunnel will be used, this is the amount that will be added to create each additional authentication key value to be sent in the GRE packets (one key per GRE tunnel).

		Returns:
			bool
		"""
		return self._get_attribute('useSequence')
	@UseSequence.setter
	def UseSequence(self, value):
		self._set_attribute('useSequence', value)
