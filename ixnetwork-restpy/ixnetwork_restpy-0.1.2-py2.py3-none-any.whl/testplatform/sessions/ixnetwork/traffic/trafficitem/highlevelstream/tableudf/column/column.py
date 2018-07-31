from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Column(Base):
	"""This object specifies column properties of an UDF table.
	"""

	_SDM_NAME = 'column'

	def __init__(self, parent):
		super(Column, self).__init__(parent)

	@property
	def Format(self):
		"""The format of the Table UDF list (column).

		Returns:
			str(ascii|binary|custom|decimal|hex|ipv4|ipv6|mac)
		"""
		return self._get_attribute('format')
	@Format.setter
	def Format(self, value):
		self._set_attribute('format', value)

	@property
	def Offset(self):
		"""The offset value, in bytes, of the Table UDF list (column).

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def Size(self):
		"""The size, in bytes, of the Table UDF list (column).

		Returns:
			number
		"""
		return self._get_attribute('size')
	@Size.setter
	def Size(self, value):
		self._set_attribute('size', value)

	@property
	def Values(self):
		"""The value of the table UDF column.

		Returns:
			list(str)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)

	def remove(self):
		"""Deletes a child instance of Column on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
