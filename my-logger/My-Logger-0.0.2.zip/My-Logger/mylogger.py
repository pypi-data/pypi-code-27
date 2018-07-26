import os
import time
import logging

sep_line = '\n' + 70 * '-' + '\n'

## LOGGING FUNCTIONS
############
def add_seperator(LOG_FILE):
	ftemp = open(LOG_FILE, "a")
	ftemp.write(sep_line)
	ftemp.write(23 * ' ' + time.asctime())
	ftemp.write(sep_line)
	ftemp.close

def get_logger(
		LOG_DIR_PATH   = ".",
		LOG_FORMAT     = '%(asctime)s : %(levelname)-8s : %(message)s',
		LOG_NAME       = '',
		LOG_INIT       = 0
		):

	log           = logging.getLogger(LOG_NAME)
	log_formatter = logging.Formatter(LOG_FORMAT)
	log_formatter.datefmt = '%d-%m-%Y %H:%M:%S'

	# uncomment below code to get console output
	# stream_handler = logging.StreamHandler()
	# stream_handler.setFormatter(log_formatter)
	# log.addHandler(stream_handler)

	LOG_FILE_INFO  = LOG_DIR_PATH + os.sep + 'report.log'
	LOG_FILE_ERROR = LOG_DIR_PATH + os.sep + 'error.log'

	if LOG_INIT == 1:
		add_seperator(LOG_FILE_INFO)
		add_seperator(LOG_FILE_ERROR)

	file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='a')
	file_handler_info.setFormatter(log_formatter)
	file_handler_info.setLevel(logging.DEBUG)
	log.addHandler(file_handler_info)

	file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='a')
	file_handler_error.setFormatter(log_formatter)
	file_handler_error.setLevel(logging.ERROR)
	log.addHandler(file_handler_error)

	log.setLevel(logging.NOTSET)

	return log
