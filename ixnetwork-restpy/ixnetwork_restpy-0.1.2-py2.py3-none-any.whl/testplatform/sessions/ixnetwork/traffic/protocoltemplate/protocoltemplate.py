from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ProtocolTemplate(Base):
	"""This object provides different options for Protocol Template.
	"""

	_SDM_NAME = 'protocolTemplate'

	def __init__(self, parent):
		super(ProtocolTemplate, self).__init__(parent)

	def Field(self, __id__=None, DisplayName=None, FieldTypeId=None):
		"""Gets child instances of Field from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Field will be returned.

		Args:
			__id__ (str): An alphanumeric string that defines the internal field ID.
			DisplayName (str): It is used to get the name of the particular field as available in the protocol template.
			FieldTypeId (str): 

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.field.field.Field))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.field.field import Field
		return self._select(Field(self), locals())

	@property
	def DisplayName(self):
		"""The display name of the template.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def StackTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('stackTypeId')

	@property
	def TemplateName(self):
		"""Indicates the protocol template name that is added to a packet.

		Returns:
			str
		"""
		return self._get_attribute('templateName')
