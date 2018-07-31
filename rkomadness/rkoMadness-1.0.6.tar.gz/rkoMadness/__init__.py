import re,subprocess,os
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado.web import RequestHandler
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from console_progressbar import ProgressBar
class Management:
	@staticmethod
	def argParser(args,settings):
		try:
			CRED = '\033[91m'
			CEND = '\033[0m'
			global newSettings
			newSettings=settings
			match = re.search(r'^run(.*)$', args[0], re.IGNORECASE)
			if match:
				Management().runServer(args)
			match = re.search(r'^newapp(.*)$', args[0], re.IGNORECASE)
			if match:
				Management().createapp(args)
			else:
				print(CRED + "Unkown command. Run rkomadness help for more details" + CEND)
		except Exception as e:
			raise e
	@staticmethod
	def runServer(args):
		try:
			pb = ProgressBar(total=100, prefix='Starting project', suffix='Done!', decimals=3, length=40, fill='X')
			pb.print_progress_bar(30)
			if len(args) >1:
				if len(args) > 2:
					raise ValueError('Command incorrect. Please try python manage.py run port')
				else:
					port=int(args[1])
			else:
				port=8000
			print(port)
			options.logging=None
			options.parse_command_line()
			print('Spawning new process')
			pb.print_progress_bar(50)
			print('Spawning Server on port {0}'.format(str(port)))
			http_server = HTTPServer(Application())
			pb.print_progress_bar(70)
			http_server.listen(port)
			pb.print_progress_bar(90)
			print('Server started and created succesfully')
			pb.print_progress_bar(100)
			print('\x1b[6;30;42m' + 'Your project is now running you can access it at http://127.0.0.1:{0}'.format(str(port)) + '\x1b[0m')
			IOLoop.instance().start()

		except Exception as e:
			raise e
	@staticmethod
	def createapp(args):
		try:
			if len(args) <=1:
				raise ValueError('Command incorrect. Please try python manage.py newapp appname')
			appname=args[1]
			subprocess.Popen("mkdir {0}".format(appname),shell=True)
			subprocess.Popen('touch {0}/__init__.py'.format(appname),shell=True)
			subprocess.Popen('touch {0}/controllers.py'.format(appname),shell=True)
		except Exception as e:
			raise e
class Application(Application):
	def __init__(self):
		try:
			handlers=newSettings.URL
			settings={}
			super(Application, self).__init__(handlers, **settings)
		except Exception as e:
			raise e
class BaseHandler(RequestHandler):
	def initialize(self):
		pass