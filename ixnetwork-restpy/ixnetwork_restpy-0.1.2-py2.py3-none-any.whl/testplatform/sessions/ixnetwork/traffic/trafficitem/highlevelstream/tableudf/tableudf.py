from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TableUdf(Base):
	"""This object specifies the UDF table properties.
	"""

	_SDM_NAME = 'tableUdf'

	def __init__(self, parent):
		super(TableUdf, self).__init__(parent)

	def Column(self):
		"""Gets child instances of Column from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Column will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.column.column.Column))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.column.column import Column
		return self._select(Column(self), locals())

	def add_Column(self, Format="decimal", Offset="0", Size="0", Values=None):
		"""Adds a child instance of Column on the server.

		Args:
			Format (str(ascii|binary|custom|decimal|hex|ipv4|ipv6|mac)): The format of the Table UDF list (column).
			Offset (number): The offset value, in bytes, of the Table UDF list (column).
			Size (number): The size, in bytes, of the Table UDF list (column).
			Values (list(str)): The value of the table UDF column.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.column.column.Column)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.column.column import Column
		return self._create(Column(self), locals())

	@property
	def Enabled(self):
		"""If enabled, enables the UDF table for this flow group if it is supported.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
