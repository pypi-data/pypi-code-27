from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInfoUpdate(Base):
	"""The learned information trigger node that contains trigger tables of learned information.
	"""

	_SDM_NAME = 'learnedInfoUpdate'

	def __init__(self, parent):
		super(LearnedInfoUpdate, self).__init__(parent)

	def PceBasicRsvpSyncLspUpdateParams(self):
		"""Gets child instances of PceBasicRsvpSyncLspUpdateParams from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceBasicRsvpSyncLspUpdateParams will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicrsvpsynclspupdateparams.PceBasicRsvpSyncLspUpdateParams))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicrsvpsynclspupdateparams import PceBasicRsvpSyncLspUpdateParams
		return self._select(PceBasicRsvpSyncLspUpdateParams(self), locals())

	def PceBasicSrSyncLspUpdateParams(self):
		"""Gets child instances of PceBasicSrSyncLspUpdateParams from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceBasicSrSyncLspUpdateParams will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicsrsynclspupdateparams.PceBasicSrSyncLspUpdateParams))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicsrsynclspupdateparams import PceBasicSrSyncLspUpdateParams
		return self._select(PceBasicSrSyncLspUpdateParams(self), locals())

	def PceDetailedRsvpSyncLspUpdateParams(self):
		"""Gets child instances of PceDetailedRsvpSyncLspUpdateParams from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceDetailedRsvpSyncLspUpdateParams will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedrsvpsynclspupdateparams.PceDetailedRsvpSyncLspUpdateParams))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedrsvpsynclspupdateparams import PceDetailedRsvpSyncLspUpdateParams
		return self._select(PceDetailedRsvpSyncLspUpdateParams(self), locals())

	def PceDetailedSrSyncLspUpdateParams(self):
		"""Gets child instances of PceDetailedSrSyncLspUpdateParams from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceDetailedSrSyncLspUpdateParams will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedsrsynclspupdateparams.PceDetailedSrSyncLspUpdateParams))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedsrsynclspupdateparams import PceDetailedSrSyncLspUpdateParams
		return self._select(PceDetailedSrSyncLspUpdateParams(self), locals())

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
