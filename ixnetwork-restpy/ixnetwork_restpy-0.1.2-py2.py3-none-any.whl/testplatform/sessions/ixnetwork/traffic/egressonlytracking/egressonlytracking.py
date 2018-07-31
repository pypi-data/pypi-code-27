from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EgressOnlyTracking(Base):
	"""
	"""

	_SDM_NAME = 'egressOnlyTracking'

	def __init__(self, parent):
		super(EgressOnlyTracking, self).__init__(parent)

	@property
	def Egress(self):
		"""Struct contains: egress offset and egress mask

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('egress')
	@Egress.setter
	def Egress(self, value):
		self._set_attribute('egress', value)

	@property
	def Enabled(self):
		"""Enables the egress only tracking for the given port.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Port(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)
		"""
		return self._get_attribute('port')
	@Port.setter
	def Port(self, value):
		self._set_attribute('port', value)

	@property
	def SignatureOffset(self):
		"""Offset where the signature value will be placed in the packet.

		Returns:
			number
		"""
		return self._get_attribute('signatureOffset')
	@SignatureOffset.setter
	def SignatureOffset(self, value):
		self._set_attribute('signatureOffset', value)

	@property
	def SignatureValue(self):
		"""Signature value to be placed inside the packet.

		Returns:
			str
		"""
		return self._get_attribute('signatureValue')
	@SignatureValue.setter
	def SignatureValue(self, value):
		self._set_attribute('signatureValue', value)

	def remove(self):
		"""Deletes a child instance of EgressOnlyTracking on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
