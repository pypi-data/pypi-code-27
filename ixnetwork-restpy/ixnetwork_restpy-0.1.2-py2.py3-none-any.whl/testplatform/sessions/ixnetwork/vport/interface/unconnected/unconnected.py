from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Unconnected(Base):
	"""Unconnected protocol interfaces that are not connected by any links to the SUT or to other Ixia ports. The unconnected interfaces can be set up to link the Ixia-emulated router to virtual networks behind the router, such as emulated OSPF network ranges.
	"""

	_SDM_NAME = 'unconnected'

	def __init__(self, parent):
		super(Unconnected, self).__init__(parent)

	@property
	def ConnectedVia(self):
		"""The name of a specified connected protocol interface on the link that is directly connected to the DUT.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)
