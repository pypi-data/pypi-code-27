
import ConfigSpace as CS
from hpbandster.core.worker import Worker

class HPOlib2Worker(Worker):
	def __init__(self,benchmark, configspace=None, budget_name='budget', budget_preprocessor=None, measure_test_loss=False,**kwargs):
		
		super().__init__(**kwargs)
		self.benchmark = benchmark
		
		if configspace is None:
			self.configspace = benchmark.get_configuration_space()
		else:
			self.configspace = configspace
		
		self.budget_name=budget_name

		if budget_preprocessor is None:
			self.budget_preprocessor = lambda b: b
		else:
			self.budget_preprocessor = budget_preprocessor

		self.measure_test_loss = measure_test_loss

	def compute(self, config, budget, **kwargs):
		c = CS.Configuration(self.configspace, values=config)
		kwargs = {self.budget_name: self.budget_preprocessor(budget)}
		res = self.benchmark.objective_function(c, **kwargs)
		
		if self.measure_test_loss:
			res['test_loss'] = self.benchmark.objective_function_test(c, **kwargs)['function_value']
		return({
			'loss': res['function_value'],
			'info': res
		})
