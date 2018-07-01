#!/usr/bin/python3
# -*- coding: utf-8 -*-

from warnings import warn
from itertools import count, chain
from os import path as path
import shutil
import random
import symengine
import numpy as np
from jitcxde_common import jitcxde, checker
from jitcxde_common.helpers import sort_helpers, sympify_helpers, copy_helpers, filter_helpers, find_dependent_helpers
from jitcxde_common.symbolic import collect_arguments, has_function

#: the symbol for the state that must be used to define the differential equation. It is a function and the integer argument denotes the component. You may just as well define an analogous function directly with SymEngine or SymPy, but using this function is the best way to get the most of future versions of JiTCSDE, in particular avoiding incompatibilities.
y = symengine.Function("y")

#: the symbol for time for defining the differential equation. If your differential equation has no explicit time dependency (“autonomous system”), you do not need this. You may just as well define an analogous symbol directly with SymEngine or SymPy, but using this function is the best way to get the most of future versions of JiTCSDE, in particular avoiding incompatibilities.
t = symengine.Symbol("t",real=True)

class UnsuccessfulIntegration(Exception):
	"""
		This exception is raised when the integrator cannot meet the accuracy and step-size requirements. If you want to know the exact state of your system before the integration fails or similar, catch this exception.
	"""
	pass

class jitcsde(jitcxde):
	"""
	Parameters
	----------
	f_sym : iterable of symbolic expressions or generator function yielding symbolic expressions
		The `i`-th element is the `i`-th component of the value of the SDE’s drift term :math:`f(t,y)`.
	
	g_sym : iterable of symbolic expressions or generator function yielding symbolic expressions
		The `i`-th element is the `i`-th component of the value of the SDE’s diffusion term :math:`g(t,y)`.
	
	helpers : list of length-two iterables, each containing a symbol and an expression
		Each helper is a variable that will be calculated before evaluating the drift and diffusion terms and can be used in their computation. The first component of the tuple is the helper’s symbol as referenced in the drift and diffusion terms or other helpers, the second component describes how to compute it from `t`, `y` and other helpers. This is for example useful to realise a mean-field coupling, where the helper could look like `(mean, sum(y(i) for i in range(100))/100)`. (See `the JiTCODE documentation <http://jitcode.readthedocs.io/#module-SW_of_Roesslers>`_ for an example.)
	
	g_helpers : `"auto"` (default), `"same"`, or like `helpers`
	
		* If `"auto"`, JiTCSDE will automatically determine which helpers are needed for `f` and `g`. The only drawback of this is that it may take some time for larger differential equations.
		* If `"same"`, `helpers` will be used for both `f` and `g` as it is.
		* If this is a list of helpers (or empty list), `helpers` will be used only for calculating `f` and `g_helpers` for `g`.
	
	n : integer
		Length of `f_sym` and `g_sym`, i.e., the dimension of the system. While JiTCSDE can easily determine this itself (and will, if necessary), this may take some time if `f_sym` is a generator function and `n` is large. Take care that this value is correct – if it isn’t, you will not get a helpful error message.
	
	additive : None or boolean
		Whether the noise term is additive, i.e., `g_sym` is independent of the state (`y`). In this case a simpler, faster integrator can be used. While JiTCSDE can easily determine this itself (and will, if necessary), this may take some time if `n` is large. If you incorrectly set this to `True`, you will not get a helpful error message.
	
	ito : boolean
		Whether the SDE is formulated in Itō or Stratonovitch calculus.
		In the latter case, the SDE will be converted to Itō calculus, as this is what is required by the integrator.
		Note that is conversion may be inefficient for large differential equations with helpers.
	
	control_pars : list of symbols
		Each symbol corresponds to a control parameter that can be used when defining the equations and set after compilation with `set_parameters`. Using this makes sense if you need to do a parameter scan with short integrations for each parameter and you are spending a considerable amount of time compiling.
	
	verbose : boolean
		Whether JiTCSDE shall give progress reports on the processing steps.
	
	module_location : string
		location of a module file from which functions are to be loaded (see `save_compiled`). If you use this, you need not give `f_sym` and `g_sym` as arguments, but in this case you must give `n`. Also note that the integrator may lack some functionalities, depending on the arguments you provide.
	"""
	
	def __init__( self,
			f_sym = (), g_sym = (),
			helpers = None, g_helpers = "auto",
			n = None,
			additive = None, ito = True,
			control_pars = (),
			verbose = True,
			module_location = None
		):
		
		super(jitcsde,self).__init__(n,verbose,module_location)
		
		if f_sym and not g_sym and not module_location:
			raise ValueError("You gave f_sym as an argument but neither g_sym nor module_location. JiTCSDE cannot properly work with this.")
		
		self.f_sym = self._handle_input(f_sym)
		self.g_sym = self._handle_input(g_sym)
		
		# The following two are the arguments passed to the function; _f_helpers and _g_helpers (note the underscore) are used internally.
		self.helpers = helpers
		self.g_helpers = g_helpers
		
		self._arrange_helpers()
		self._determine_additivity(additive)
		if not ito:
			if self.additive:
				warn("No need for conversion from Stratonovich to Itō for additive SDE.")
			else:
				self._stratonovich_to_ito()
		
		self.control_pars = control_pars
		self.integration_parameters_set = False
		self.SDE = None
		self.seed = None
		self._y = None
		self._t = None
	
	def _determine_additivity(self,additive):
		if additive is None:
			self.additive = (
					    all( not has_function(entry    ,y) for entry  in self.g_sym()    )
					and all( not has_function(helper[1],y) for helper in self._g_helpers )
					)
		else:
			self.additive = additive
	
	def _stratonovich_to_ito(self):
		if hasattr(self,"itoed"):
			raise AssertionError("_stratonovich_to_ito must not be called twice.")
		else:
			self.itoed = True
		
		# The actual conversion.
		f_sym = list(self.f_sym())
		for i,g_entry in enumerate(self.g_sym()):
			g_diff = g_entry.diff(y(i))
			for helper in find_dependent_helpers(self._g_helpers,y(i)):
				g_diff += g_entry.diff(helper[0]) * helper[1]
			f_sym[i] += g_entry * g_diff / 2
		self.f_sym = lambda: f_sym
		
		# Rearrange helpers if necessary
		if self.g_helpers == "same" or not self.g_helpers:
			pass
		elif self.g_helpers == "auto":
			self._arrange_helpers()
		elif self.g_helpers != "same":
			for g_helper in self.g_helpers:
				if not any(g_helper[0]==f_helper[0] for f_helper in self.helpers):
					self.helpers.append(g_helper)
			self._arrange_helpers()
	
	def _arrange_helpers(self):
		"""
		Splits helpers into those needed by f and those needed by g.
		"""
		helpers = sort_helpers(sympify_helpers(self.helpers or []))
		
		if self.g_helpers=="auto":
			f_needed = set().union(*(entry.free_symbols for entry in self.f_sym()))
			g_needed = set().union(*(entry.free_symbols for entry in self.g_sym()))
			
			self._f_helpers = filter_helpers(helpers,f_needed)
			self._g_helpers = filter_helpers(helpers,g_needed)
		
		else:
			self._f_helpers = helpers
			if self.g_helpers=="same":
				self._g_helpers = copy_helpers(helpers)
			else:
				self._g_helpers = sort_helpers(sympify_helpers(self.g_helpers or []))
	
	@property
	def y(self):
		if self.SDE:
			return self.SDE.get_state()
		else:
			return self._y
	
	@y.setter
	def y(self, value):
		self._y = value
		self.reset_integrator()
	
	@property
	def t(self):
		"""
		Returns
		-------
		time : float
		The current time of the integrator.
		"""
		if self.SDE:
			return self.SDE.t
		else:
			return self._t
	
	@t.setter
	def t(self, value):
		self._t = value
		self.reset_integrator()
	
	@checker
	def _check_non_empty(self):
		for function,name in [(self.f_sym, "f_sym"), (self.g_sym, "g_sym")]:
			self._check_assert( function(), "%s is empty."%name )
		
	@checker
	def _check_valid_arguments(self):
		for function,name in [(self.f_sym, "f_sym"), (self.g_sym, "g_sym")]:
			for i,entry in enumerate(function()):
				for argument in collect_arguments(entry,y):
					self._check_assert(
							argument[0] >= 0,
							"y is called with a negative argument (%i) in component %i of %s." % (argument[0],i,name)
						)
					self._check_assert(
							argument[0] < self.n,
							"y is called with an argument (%i) higher than the system’s dimension (%i) in component %i of %s."  % (argument[0], self.n,i,name)
						)
	
	@checker
	def _check_valid_symbols(self):
		valid_symbols = [t] + [helper[0] for helper in chain(self._f_helpers,self._g_helpers)] + list(self.control_pars)
		
		for function,name in [(self.f_sym, "f_sym"), (self.g_sym, "g_sym")]:
			for i,entry in enumerate(function()):
				for symbol in entry.atoms(symengine.Symbol):
					self._check_assert(
							symbol in valid_symbols,
							"Invalid symbol (%s) in component %i of %s."  % (symbol.name,i,name)
						)
	
	def reset_integrator(self):
		"""
		Resets the integrator, forgetting all stored noise (and waiting times for `jitcsde_jump`) and forcing re-initiation when it is needed next.
		"""
		self.SDE = None
	
	@property
	def is_initiated(self):
		return self.SDE is not None
	
	def set_initial_value(self, initial_value, time=0.0):
		"""
		Sets the initial value and starting time of the integration.
		"""
		if self.n != len(initial_value):
			raise ValueError("The dimension of the initial value does not match the dimension of your differential equations.")
		
		self.y = np.array( initial_value, copy=True, dtype=float )
		self.t = time
		return self
	
	def set_seed(self, seed=None):
		"""
		Sets the seed used for random-number generation. Use this if you want to have reproducible conditions. Whenever the integrator is (re)initialised, this seed is used. If you do not call this method or call it with `None` as an argument, the seed is chosen elsewise (depending on which backend and random-number generator is used).
		"""
		self.seed = seed
	
	def generate_lambdas(self):
		"""
		Explicitly initiates a purely Python-based integrator.
		"""
		
		import jitcsde._python_core as python_core
		
		assert self.y is not None, "You need to set an initial value first."
		assert self.t is not None, "You need to set an initial time first."
		
		self.SDE = python_core.sde_integrator(
				self.f_sym, self.g_sym,
				self.y,
				self.t,
				self._f_helpers, self._g_helpers,
				self.control_pars,
				self.seed,
				self.additive
			)
		self.compile_attempt = False
	
	def _compile_C(self):
		self.compile_C()
	
	def compile_C(
			self,
			simplify = None,
			do_cse = False,
			numpy_rng = False,
			chunk_size = 100,
			extra_compile_args = None,
			extra_link_args = None,
			verbose = False,
			modulename = None,
			omp = False,
		):
		"""
		translates the derivative to C code using SymEngine’s `C-code printer <https://github.com/symengine/symengine/pull/1054>`_.
		For detailed information many of the arguments and other ways to tweak the compilation, read `these notes <jitcde-common.readthedocs.io>`_.
		
		Parameters
		----------
		simplify : boolean
			Whether the derivative should be `simplified <http://docs.sympy.org/dev/modules/simplify/simplify.html>`_ (with `ratio=1.0`) before translating to C code. The main reason why you could want to disable this is if your derivative is already  optimised and so large that simplifying takes a considerable amount of time. If `None`, this will be automatically disabled for `n>10`.
		
		do_cse : boolean
			Whether SymPy’s `common-subexpression detection <http://docs.sympy.org/dev/modules/rewriting.html#module-sympy.simplify.cse_main>`_ should be applied before translating to C code.
			It is almost always better to let the compiler do this (unless you want to set the compiler optimisation to `-O2` or lower). As this requires all entries of `f` and `g` at once, it may void advantages gained from using generator functions as an input. Also, this feature uses SymPy and not SymEngine.
		
		numpy_rng : boolean
			Whether `numpy.random.normal` shall be explicitly employed for generating random numbers. This is less efficient and mainly exists for testing purposes to ensure that the random numbers are the same as when using the Python backend. Note that the alternative is still based on the same code as NumPy’s random-number generator (until somebody changes it) and should produce the same results. Also note that details in the arithmetic realisation may still cause tiny differences in the results from the two backends, which can then be magnified by the butterfly effect.
		
		chunk_size : integer
			If the number of instructions in the final C code exceeds this number, it will be split into chunks of this size. See `Handling very large differential equations <http://jitcde-common.readthedocs.io/#handling-very-large-differential-equations>`_ on why this is useful and how to best choose this value.
			If smaller than 1, no chunking will happen.
		
		extra_compile_args : iterable of strings
		extra_link_args : iterable of strings
			Arguments to be handed to the C compiler or linker, respectively.
		
		verbose : boolean
			Whether the compiler commands shall be shown. This is the same as Setuptools’ `verbose` setting.

		modulename : string or `None`
			The name used for the compiled module.
		
		omp : pair of iterables of strings or boolean
			What compiler arguments shall be used for multiprocessing (using OpenMP). If `True`, they will be selected automatically. If empty or `False`, no compilation for multiprocessing will happen (unless you supply the relevant compiler arguments otherwise).
		"""
		
		self.compile_attempt = False
		
		if simplify is None:
			simplify = self.n<=10
		
		helper_lengths = dict()
		
		for sym,helpers,name,long_name in [
					( self.f_sym, self._f_helpers, "f", "drift"     ),
					( self.g_sym, self._g_helpers, "g", "diffusion" )
				]:
			setter_name = "set_" + long_name
			wc = sym()
			helpers_wc = copy_helpers(helpers)
			
			if simplify:
				wc = (entry.simplify(ratio=1.0) for entry in wc)
			
			if do_cse:
				import sympy
				additional_helper = sympy.Function("additional_"+name+"_helper")
				
				_cse = sympy.cse(
						sympy.Matrix(sympy.sympify(list(wc))),
						symbols = (additional_helper(i) for i in count())
					)
				helpers_wc.extend(symengine.sympify(_cse[0]))
				wc = symengine.sympify(_cse[1][0])
			
			arguments = [
					("self", "sde_integrator * const"),
					("t", "double const"),
					(long_name, "double", self.n),
				]
			if name=="f" or not self.additive:
				arguments.append( ("Y","double",self.n) )
			if name=="f":
				arguments.append( ("h","double") )
			
			functions = ["y"]
			self.substitutions = {
					control_par: symengine.Symbol("self->parameter_"+control_par.name)
					for control_par in self.control_pars
				}
			
			def finalise(expression):
				return expression.subs(self.substitutions)
			
			if helpers_wc:
				converted_helpers = []
				get_helper = symengine.Function("get_"+name+"_helper")
				set_helper = symengine.Function("set_"+name+"_helper")
				
				for i,helper in enumerate(helpers_wc):
					converted_helpers.append(set_helper(i, finalise(helper[1])))
					self.substitutions[helper[0]] = get_helper(i)
				
				extra_arguments = [(name, "double", len(helpers_wc))]
				functions.extend(["get_"+name+"_helper", "set_"+name+"_helper"])
				
				self.render_and_write_code(
						converted_helpers,
						name = name + "_helpers",
						chunk_size = chunk_size,
						arguments = arguments + extra_arguments
					)
			
			setter = symengine.Function(setter_name)
			self.render_and_write_code(
					(setter(i,finalise(entry)) for i,entry in enumerate(wc)),
					name = name,
					chunk_size = chunk_size,
					arguments = arguments
				)
			
			helper_lengths[name] = len(helpers_wc)
		
		self._process_modulename(modulename)
		
		self._render_template(
				n = self.n,
				number_of_f_helpers = helper_lengths["f"],
				number_of_g_helpers = helper_lengths["g"],
				control_pars = [ par.name for par in self.control_pars ],
				additive = self.additive,
				numpy_rng = numpy_rng,
				chunk_size = chunk_size # only for OMP
			)
		
		if not numpy_rng:
			rng_file = path.join(path.dirname(__file__),"random_numbers.c")
			shutil.copy(rng_file,self._tmpfile())
		
		self._compile_and_load(verbose,extra_compile_args,extra_link_args,omp)
	
	def _initiate(self):
		if self.compile_attempt is None:
			self._attempt_compilation()
		
		if not self.is_initiated:
			assert self.y is not None, "You need to set an initial value first."
			assert self.t is not None, "You need to set an initial time first."
			
			if self.compile_attempt:
				# We cannot just use “seed = self.seed or int(…” here, as this would not work as intended if self.seed is 0.
				seed = int(random.getrandbits(32)) if self.seed is None else self.seed
				self.SDE = self.jitced.sde_integrator(self._t,self.y,seed)
			else:
				self.generate_lambdas()
		
		self._set_integration_parameters()
	
	def set_parameters(self, *parameters):
		"""
		Set the control parameters defined by the `control_pars` argument of the `jitcsde`.
		
		Parameters
		----------
		parameters : floats
			Values of the control parameters. The order must be the same as in the `control_pars` argument of the `jitcsde`.
		"""
	
		self._initiate()
		self.SDE.set_parameters(*parameters)
	
	def _set_integration_parameters(self):
		if not self.integration_parameters_set:
			self.report("Using default integration parameters.")
			self.set_integration_parameters()
	
	def set_integration_parameters(self,
			atol = 1e-10,
			rtol = 1e-5,
			first_step = 1.0,
			min_step = 1e-10,
			max_step = 10.0,
			decrease_threshold = 1.1,
			increase_threshold = 0.5,
			safety_factor = 0.9,
			max_factor = 5.0,
			min_factor = 0.2,
		):
		
		"""
		Sets the parameters for the step-size adaption.
		
		Parameters
		----------
		atol : float
		rtol : float
			The tolerance of the estimated integration error is determined as :math:`\\texttt{atol} + \\texttt{rtol}·|y|`. The step-size adaption algorithm is the same as for the GSL. For details see `its documentation <http://www.gnu.org/software/gsl/manual/html_node/Adaptive-Step_002dsize-Control.html>`_.
		
		first_step : float
			The step-size adaption starts with this value.
			
		min_step : float
			Should the step-size have to be adapted below this value, the integration is aborted and `UnsuccessfulIntegration` is raised.
		
		max_step : float
			The step size will be capped at this value.
			
		decrease_threshold : float
			If the estimated error divided by the tolerance exceeds this, the step size is decreased.
		
		increase_threshold : float
			If the estimated error divided by the tolerance is smaller than this, the step size is increased.
		
		safety_factor : float
			To avoid frequent adaption, all freshly adapted step sizes are multiplied with this factor.
		
		max_factor : float
		min_factor : float
			The maximum and minimum factor by which the step size can be adapted in one adaption step.
		"""
		
		if first_step > max_step:
			first_step = max_step
			warn("Decreasing first_step to match max_step")
		if min_step > first_step:
			min_step = first_step
			warn("Decreasing min_step to match first_step")
		
		assert decrease_threshold>=1.0, "decrease_threshold smaller than 1"
		assert increase_threshold<=1.0, "increase_threshold larger than 1"
		assert max_factor>=1.0, "max_factor smaller than 1"
		assert min_factor<=1.0, "min_factor larger than 1"
		assert safety_factor<=1.0, "safety_factor larger than 1"
		assert atol>=0.0, "negative atol"
		assert rtol>=0.0, "negative rtol"
		if atol==0 and rtol==0:
			warn("atol and rtol are both 0. You probably do not want this.")
		
		self.atol = atol
		self.rtol = rtol
		self.dt = first_step
		self.min_step = min_step
		self.max_step = max_step
		self.decrease_threshold = decrease_threshold
		self.increase_threshold = increase_threshold
		self.safety_factor = safety_factor
		self.max_factor = max_factor
		self.min_factor = min_factor
		
		self.q = 1.5
		
		self.integration_parameters_set = True
	
	
	def _control_for_min_step(self):
		if self.dt < self.min_step:
			raise UnsuccessfulIntegration("\n"
				"Could not integrate with the given tolerance parameters:\n\n"
				"atol: %e\n"
				"rtol: %e\n"
				"min_step: %e\n\n"
				"The most likely reasons for this are:\n"
				"• The SDE is ill-posed or stiff.\n"
				"• You did not allow for an absolute error tolerance (atol) though your SDE calls for it. Even a very small absolute tolerance (1e-16) may sometimes help."
				% (self.atol, self.rtol, self.min_step))
	
	def _adjust_step_size(self, actual_dt):
		"""
		adjusts the step size and returns whether the step was successful
		"""
		p = self.SDE.get_p(self.atol, self.rtol)
		if p > self.decrease_threshold:
			self.dt = actual_dt * max(self.safety_factor*p**(-1/self.q), self.min_factor)
			self._control_for_min_step()
			return False
		else:
			if p <= self.increase_threshold:
				factor = self.safety_factor*p**(-1/(self.q+1)) if p else self.max_factor
				sug_step = actual_dt*min(factor, self.max_factor)
				self.dt = max( self.dt, min(sug_step, self.max_step) )
			return True
	
	def integrate(self, target_time):
		"""
		Tries to evolve the dynamics.
		
		Parameters
		----------
		
		target_time : float
			time until which the dynamics is evolved
		
		Returns
		-------
		state : NumPy array
			the computed state of the system at `target_time`.
		"""
		self._initiate()
		
		last_step = ( self.SDE.t >= target_time )
		
		while not last_step:
			if self.SDE.t+self.dt < target_time:
				actual_dt = self.dt
			else:
				actual_dt = target_time - self.SDE.t
				last_step = True
			self.SDE.get_next_step(actual_dt)
			
			if self._adjust_step_size(actual_dt):
				self.SDE.accept_step()
			else:
				last_step = False
		
		return self.SDE.get_state()
	
	def pin_noise(self, number, step_size):
		"""
		Fills the noise memory with a realisation of the underlying Wiener process sampled at `number` points with a distance of `step_size` (i.e., for a total length of `number`·`step_size`).
		
		This is mainly intended for testing purposes, e.g., if you want to investigate the influence of the step-size-adjustment parameters in a controlled setting. Note that this only pins the Wiener process at the specified points. All other points will have to be interpolated with a Brownian bridge, but the lower the `step_size`, the more constrained they will be. Note that this inevitably slows things down.
		
		Parameters
		----------
		
		number : integer
			number of pre-defined noise points
		
		step_size : float
			distance of pre-defined noise points
		"""
		
		assert number>=0, "Number must be non-negative"
		assert step_size>0, "Step size must be positive"
		
		self._initiate()
		self.SDE.pin_noise(number,step_size)

class jitcsde_jump(jitcsde):
	"""
	An extension of `jitcsde` that can additionally handle random jumps. Note that as you are controlling the randomness in these functions, you also have to handle the random seed yourself. The handling is like that of `jitcsde` except for:
	
	Parameters
	----------

	IJI : callable `IJI(time,state)` returning a non-negative number
		A function (or similar) that returns a waiting time for the next jump, i.e., that draws one value from the inter-jump-interval distribution. A new waiting time using this function is determined directly after each jump (and at the first call of `integrate`). Hence, only the state and time at those times affect the waiting time, if you choose it to be time- or state-dependent.
	
	amp : callable `amp(time,state)` returning an array of size `n`.
		A function (or similar) that returns the actual jump.
		This must be a NumPy array, even if your system is one-dimensional.
	"""
	
	def __init__( self, IJI, amp, *args, **kwargs ):
		if not kwargs.pop("ito",True):
			raise NotImplementedError("I don’t know how to convert jumpy Stratonovich SDEs to Itō SDEs – nobody does.")
		super(jitcsde_jump,self).__init__(*args, **kwargs)
		self.IJI = IJI
		self.amp = amp
		self._next_jump = None
	
	@property
	def next_jump(self):
		if self._next_jump is None:
			self._initiate()
			self._next_jump = self.t + self.IJI(self.t,self.y)
		return self._next_jump
	
	def reset_integrator(self):
		super(jitcsde_jump,self).reset_integrator()
		self._next_jump = None
	
	def integrate(self, target_time):
		while self.next_jump<target_time:
			state = super(jitcsde_jump,self).integrate(self.next_jump)
			time = self.t
			self.SDE.apply_jump( self.amp(time,state) )
			self._next_jump = self.t + self.IJI(time,self.y)
		
		return super(jitcsde_jump,self).integrate(target_time)
	
	def check(self, fail_fast=True):
		"""
			Same as jitcsde’s check, but additionally checks the output of the amp function (by calling it).
		"""
		super(jitcsde_jump,self).check(fail_fast)
	
	@checker
	def check_amp_function(self):
		output = self.amp(
				self.t or 0.0,
				self.y or np.random.random(self.n)
			)
		
		self._check_assert(
				isinstance(output,np.ndarray),
				"Output of amp function is not an array"
			)
		self._check_assert(
				output.size == self.n,
				"Output of amp function has the wrong dimension"
			)

