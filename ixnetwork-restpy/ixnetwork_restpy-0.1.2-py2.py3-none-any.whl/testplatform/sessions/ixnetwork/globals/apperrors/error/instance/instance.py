from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Instance(Base):
	"""An instance of an error
	"""

	_SDM_NAME = 'instance'

	def __init__(self, parent):
		super(Instance, self).__init__(parent)

	@property
	def SourceValues(self):
		"""The source values of the error instance

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceValues')
