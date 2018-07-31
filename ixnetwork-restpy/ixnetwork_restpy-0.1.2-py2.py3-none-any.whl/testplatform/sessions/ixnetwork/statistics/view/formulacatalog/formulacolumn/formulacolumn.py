from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FormulaColumn(Base):
	"""The formula is filtered and maintained in columns.
	"""

	_SDM_NAME = 'formulaColumn'

	def __init__(self, parent):
		super(FormulaColumn, self).__init__(parent)

	@property
	def Caption(self):
		"""The name of the formula.

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def Formula(self):
		"""The formula that is filtered.

		Returns:
			str
		"""
		return self._get_attribute('formula')
	@Formula.setter
	def Formula(self, value):
		self._set_attribute('formula', value)

	def remove(self):
		"""Deletes a child instance of FormulaColumn on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
