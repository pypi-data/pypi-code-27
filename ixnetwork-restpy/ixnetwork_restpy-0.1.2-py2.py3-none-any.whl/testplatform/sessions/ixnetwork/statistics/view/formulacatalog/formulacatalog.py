from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FormulaCatalog(Base):
	"""This object holds the catalog information for the various statisticalformula.
	"""

	_SDM_NAME = 'formulaCatalog'

	def __init__(self, parent):
		super(FormulaCatalog, self).__init__(parent)

	def FormulaColumn(self, Caption=None, Formula=None):
		"""Gets child instances of FormulaColumn from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of FormulaColumn will be returned.

		Args:
			Caption (str): The name of the formula.
			Formula (str): The formula that is filtered.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacolumn.formulacolumn.FormulaColumn))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacolumn.formulacolumn import FormulaColumn
		return self._select(FormulaColumn(self), locals())

	def add_FormulaColumn(self, Caption="", Formula=""):
		"""Adds a child instance of FormulaColumn on the server.

		Args:
			Caption (str): The name of the formula.
			Formula (str): The formula that is filtered.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacolumn.formulacolumn.FormulaColumn)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacolumn.formulacolumn import FormulaColumn
		return self._create(FormulaColumn(self), locals())
