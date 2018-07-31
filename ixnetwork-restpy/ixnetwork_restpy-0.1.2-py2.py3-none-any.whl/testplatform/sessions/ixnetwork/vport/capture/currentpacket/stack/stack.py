from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Stack(Base):
	"""This object specifies the stack properties.
	"""

	_SDM_NAME = 'stack'

	def __init__(self, parent):
		super(Stack, self).__init__(parent)

	def Field(self, DisplayName=None, FieldValue=None):
		"""Gets child instances of Field from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Field will be returned.

		Args:
			DisplayName (str): Refers to the name of the field.
			FieldValue (str): Refers to the value displayed in the field.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.field.field.Field))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.field.field import Field
		return self._select(Field(self), locals())

	@property
	def DisplayName(self):
		"""Refers to the name of the stack.

		Returns:
			str
		"""
		return self._get_attribute('displayName')
