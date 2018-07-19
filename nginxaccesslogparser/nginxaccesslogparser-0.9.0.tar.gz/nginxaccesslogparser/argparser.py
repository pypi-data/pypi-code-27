"""argparser.py - contains method for parsing the application arguments."""

# import required modules
import argparse											# Parser for command-line options, arguments and sub-commands

# DEFAULT_ACCESS_LOG_PATH = 'access.log'	# default path to nginx access log file

# Parses the arguments to the application and returns access log file path and threaded flag
def options_handler():
	"""
	Parses the arguments to the application and returns access log file path and threaded flag

	Parameters
	----------
	No Parameters

	Returns
	-------
	tuple
		(access log file path, threaded flag)
		access log file path : path to the access log file
		threaded flag : if the parsing is to be done using multithreaded mode

	"""

	# create ArgumentParser instance
	parser = argparse.ArgumentParser(description='Parser for nginx access log file')

	# add --input argument
	parser.add_argument('--input', type=str, help='Path to nginx access log file to parse')

	# add --info argument
	parser.add_argument('--info', action="store_true", help='Information about nginx access log parser')

	# add --follow argument
	parser.add_argument('--follow', action="store_true", help='Handling Streaming data')

	# add --thread argument
	parser.add_argument('--thread', type=int, help='If the parsing is to be done using multithreaded mode')

	# parse the arguments
	args = parser.parse_args()

	if ((not args.input) and args.info):				# if Information is requested
		# print application details
		info()
		exit(0)

	elif ((not args.input) and (not args.info)):		# if no option is passed
		print('one of the options --info and --input is required')
		exit(0)

	elif (args.input and args.info):					# if --input and --info both options are supplied
		# print appropriate message
		print('options --info and --input can not be applied together')
		exit(0)

	return args.input, args.thread, args.follow


def info():
	print('-------------------------------------------------------------------------------')
	print('NGINX Access Log Parser:')
	print('-------------------------------------------------------------------------------')
	print('It displays the summary of:')
	print('Number of Requests')
	print('Average Number of Bytes Sent and ')
	print('Number of 2XX, 3XX, 4XX, 5XX status codes')
	print('-------------------------------------------------------------------------------')
	print('Examples:')
	print('-------------------------------------------------------------------------------')
	print('1.')
	print('-------------------------------------------------------------------------------')
	print('Generate Summary for the nginx access log located at /var/log/nginx/access.log')
	print('Explicit specification for the path for nginx access log file')
	print('$ nginxaccesslogparser --input /var/log/nginx/access.log')
	print('-------------------------------------------------------------------------------')
	print('2.')
	print('-------------------------------------------------------------------------------')
	print('Detailed Information about the access_log_parser')
	print('$ nginxaccesslogparser --info')
	print('-------------------------------------------------------------------------------')
	print('3.')
	print('-------------------------------------------------------------------------------')
	print('Multithreaded version of the access log parser with 10000 threads')
	print('For very large log files multithreaded version works well')
	print('$ nginxaccesslogparser --input /var/log/nginx/access.log --thread 10000')
	print('-------------------------------------------------------------------------------')
