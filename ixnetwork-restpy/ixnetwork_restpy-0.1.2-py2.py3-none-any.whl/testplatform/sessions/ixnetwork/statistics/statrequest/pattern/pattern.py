from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Pattern(Base):
	"""This object refers to the pattern of the statistics flow.
	"""

	_SDM_NAME = 'pattern'

	def __init__(self, parent):
		super(Pattern, self).__init__(parent)

	@property
	def FlowLabel(self):
		"""This corresponds to the name or the label given to each flow.

		Returns:
			str
		"""
		return self._get_attribute('flowLabel')
	@FlowLabel.setter
	def FlowLabel(self, value):
		self._set_attribute('flowLabel', value)

	@property
	def RowCount(self):
		"""Displays the a particular row number in the view.

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	def remove(self):
		"""Deletes a child instance of Pattern on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
