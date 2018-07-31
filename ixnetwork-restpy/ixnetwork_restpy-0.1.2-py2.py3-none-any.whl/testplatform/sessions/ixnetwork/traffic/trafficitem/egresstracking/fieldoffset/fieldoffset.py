from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FieldOffset(Base):
	"""Specifies the offset position of the selected field.
	"""

	_SDM_NAME = 'fieldOffset'

	def __init__(self, parent):
		super(FieldOffset, self).__init__(parent)

	def Stack(self, DisplayName=None, StackTypeId=None, TemplateName=None):
		"""Gets child instances of Stack from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Stack will be returned.

		Args:
			DisplayName (str): The display name of the stack.
			StackTypeId (str): 
			TemplateName (str): Indiates the protocol template name that is added to a packet in a stack.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.stack.stack.Stack))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.stack.stack import Stack
		return self._select(Stack(self), locals())
