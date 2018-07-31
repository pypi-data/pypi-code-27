from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RxFilters(Base):
	"""This object defines the parameters for the Rx Filters.
	"""

	_SDM_NAME = 'rxFilters'

	def __init__(self, parent):
		super(RxFilters, self).__init__(parent)

	@property
	def FilterPalette(self):
		"""Returns the one and only one FilterPalette object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.filterpalette.filterpalette.FilterPalette)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.filterpalette.filterpalette import FilterPalette
		return self._read(FilterPalette(self), None)

	def Uds(self):
		"""Gets child instances of Uds from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Uds will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.uds.uds.Uds))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.uds.uds import Uds
		return self._select(Uds(self), locals())
