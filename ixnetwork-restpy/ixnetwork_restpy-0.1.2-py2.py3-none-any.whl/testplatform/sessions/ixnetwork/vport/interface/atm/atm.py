from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Atm(Base):
	"""On Asynchronous Transport Mode (ATM) is a Layer 2, connection-oriented, switching protocol, based on L2 Virtual Circuits (VCs). For operation in a connection-less IP routing or bridging environment, the IP PDUs must be encapsulated within the payload field of an ATM AAL5 CPCS-PDU (ATM Adaptation Layer 5 - Common Part Convergence Sublayer - Protocol Data Unit). The ATM CPCS-PDUs are divided into 48-byte segments which receive 5-byte headers - to form 53-byte ATM cells. The ATM cells are then switched across the ATM network, based on the Virtual Port Identifiers (VPIs) and the Virtual Connection Identifiers (VCIs).
	"""

	_SDM_NAME = 'atm'

	def __init__(self, parent):
		super(Atm, self).__init__(parent)

	@property
	def Encapsulation(self):
		"""The type of RFC 2684 ATM multiplexing encapsulation (routing) protocol to be used.

		Returns:
			str(vcMuxIpv4|vcMuxIpv6|vcMuxBridgeFcs|vcMuxBridgeNoFcs|llcClip|llcBridgeFcs|llcBridgeNoFcs)
		"""
		return self._get_attribute('encapsulation')
	@Encapsulation.setter
	def Encapsulation(self, value):
		self._set_attribute('encapsulation', value)

	@property
	def Vci(self):
		"""Virtual Circuit/Connection Identifier (VCI) for the ATM VC over which information is being transmitted.

		Returns:
			number
		"""
		return self._get_attribute('vci')
	@Vci.setter
	def Vci(self, value):
		self._set_attribute('vci', value)

	@property
	def Vpi(self):
		"""Virtual Path Identifier (VPI) for the ATM VC over which information is being transmitted.

		Returns:
			number
		"""
		return self._get_attribute('vpi')
	@Vpi.setter
	def Vpi(self, value):
		self._set_attribute('vpi', value)
