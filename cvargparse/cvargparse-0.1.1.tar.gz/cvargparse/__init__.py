import argparse, logging

class Arg(object):
	def __init__(self, *args, **kw):
		super(Arg, self).__init__()
		self.args = args
		self.kw = kw

class FileArg(Arg):
	def __init__(self, *args, **kw):
		super(FileArg, self).__init__(*args, **kw)

	@classmethod
	def mode(cls, file_mode, encoding=None):
		def wrapper(*args, **kw):
			obj = cls(*args, **kw)
			obj.kw["type"] = argparse.FileType(file_mode, encoding=encoding)
			return obj
		return wrapper

class BaseParser(argparse.ArgumentParser):
	def __init__(self, arglist=[], nologging=False, sysargs=None, *args, **kw):
		super(BaseParser, self).__init__(*args, **kw)
		self.__nologging = nologging
		self.__sysargs = sysargs
		if isinstance(arglist, ArgFactory):
			arglist = arglist.get()

		for arg in arglist:
			if isinstance(arg, Arg):
				self.add_argument(*arg.args, **arg.kw)
			else:
				self.add_argument(*arg[0], **arg[1])


		if not self.has_logging: return

		self.add_argument(
			'--logfile', type=str, default='',
			help='file for logging output')

		self.add_argument(
			'--loglevel', type=str, default='INFO',
			help='logging level. see logging module for more information')

		self.__args = None


	@property
	def args(self):
		if self.__args is None:
			self.__args = self.parse_args(self.__sysargs)

		return self.__args


	@property
	def has_logging(self):
		return not self.__nologging

	def init_logger(self, simple=False):
		if not self.has_logging: return
		fmt = '%(message)s' if simple else '%(levelname)s - [%(asctime)s] %(filename)s:%(lineno)d [%(funcName)s]: %(message)s'
		logging.basicConfig(
			format=fmt,
			level=getattr(logging, self.args.loglevel.upper(), logging.DEBUG),
			filename=self.args.logfile or None,
			filemode="w")


class GPUParser(BaseParser):
	def __init__(self, *args, **kw):
		super(GPUParser, self).__init__(*args, **kw)
		self.add_argument(
			"--gpu", "-g", type=int, nargs="+", default=[-1],
			help="which GPU to use. select -1 for CPU only")


def factory(func):
	"""
		Returns 'self' at the end
	"""
	def inner(self, *args, **kw):
		func(self, *args, **kw)
		return self
	return inner

class ArgFactory(object):
	def __init__(self, initial=[]):
		super(ArgFactory, self).__init__()
		self.args = initial

	def get(self):
		return self.args

	@factory
	def batch_size(self):
		self.args.append(
			Arg("--batch_size", "-b", type=int, default=32, help="batch size")
		)

	@factory
	def epochs(self):
		self.args.append(
			Arg("--epochs", "-e", type=int, default=30, help="number of epochs"),
		)

	@factory
	def debug(self):
		self.args.append(
			Arg("--debug", action="store_true", help="enable chainer debug mode"),
		)

	@factory
	def seed(self):
		self.args.append(
			Arg("--seed", type=int, default=None, help="random seed"),
		)

	@factory
	def weight_decay(self, default=5e-3):
		self.args.append(
			Arg("--decay", type=float, default=default, help="weight decay"),
		)

	@factory
	def learning_rate(self, lr=1e-2, lrs=10, lrd=1e-1, lrt=1e-6):
		self.args.extend([
			Arg("--learning_rate", "-lr", type=float, default=lr, help="learning rate"),
			Arg("--lr_shift", "-lrs", type=int, default=lrs, help="learning rate shift interval (in epochs)"),
			Arg("--lr_decrease_rate", "-lrd", type=float, default=lrd, help="learning rate decrease"),
			Arg("--lr_target", "-lrt", type=float, default=lrt, help="learning rate target"),
		])

__version__ = "0.1.1"
