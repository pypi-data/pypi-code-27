try:
	import IPython
	IPython.start_ipython()
except:
	import code
	interpreter = code.InteractiveInterpreter()
	interpreter.interact()