from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class StackLink(Base):
	"""This is a list of stack objects that can be linked
	"""

	_SDM_NAME = 'stackLink'

	def __init__(self, parent):
		super(StackLink, self).__init__(parent)

	@property
	def LinkedTo(self):
		"""Indicates which stack item this is linked to.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stackLink)
		"""
		return self._get_attribute('linkedTo')
	@LinkedTo.setter
	def LinkedTo(self, value):
		self._set_attribute('linkedTo', value)
