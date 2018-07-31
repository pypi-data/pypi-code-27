from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TlvProfile(Base):
	"""Tlv profile functionality is contained under this node
	"""

	_SDM_NAME = 'tlvProfile'

	def __init__(self, parent):
		super(TlvProfile, self).__init__(parent)

	def DefaultTlv(self, Description=None, Name=None):
		"""Gets child instances of DefaultTlv from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of DefaultTlv will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.defaulttlv.DefaultTlv))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.defaulttlv import DefaultTlv
		return self._select(DefaultTlv(self), locals())

	def Tlv(self, Description=None, Name=None):
		"""Gets child instances of Tlv from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Tlv will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv.Tlv))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv import Tlv
		return self._select(Tlv(self), locals())

	def add_Tlv(self, Description=None, IncludeInMessages=None, IsEnabled=None, Name=None):
		"""Adds a child instance of Tlv on the server.

		Args:
			Description (str): Description of the tlv
			IncludeInMessages (list(str)): Include the TLV in these protocol messages
			IsEnabled (bool): Enables/disables this tlv
			Name (str): Name of the tlv

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv.Tlv)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv import Tlv
		return self._create(Tlv(self), locals())

	def CopyTlv(self, Arg2):
		"""Executes the copyTlv operation on the server.

		Copy a template tlv to a topology tlv profile

		Args:
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology)): An object reference to a source template tlv

		Returns:
			str(None): An object reference to the newly created topology tlv as a result of the copy operation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('copyTlv', payload=locals(), response_object=None)

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
