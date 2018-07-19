import re
import time
import threading
from terminaltables import AsciiTable
from .access_log import NginxAccessLog

# global variables
requests_processed, total_time, requests_per_second, count, total_bytes_sent, avg_bytes_sent, xx2, xx3, xx4, xx5 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
initial_timestamp = None
threadLock = None

conf = '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"'
regex = ''.join(
	'(?P<' + g + '>.*?)' if g else re.escape(c)
	for g, c in re.findall(r'\$(\w+)|(.)', conf))

# read access log file at given path and return list of logs
def read_logs(access_log_path):
	logs = []

	with open(access_log_path) as f:
		for line in f:
			logs.append(line)

	return logs


# parse a single log
def parse_log(log):
	global regex

	log_dict = re.match(regex, log).groupdict()
	return NginxAccessLog(log_dict['status'], int(log_dict['body_bytes_sent']))

# parses the list of logs and returns list of NginxAccessLog instances
def parse_logs(logs):
	records = []

	for log in logs:
		records.append(parse_log(log))

	return records


def process_record(record):

	global threadLock
	global requests_processed, total_time, requests_per_second, count, total_bytes_sent, avg_bytes_sent, xx2, xx3, xx4, xx5

	threadLock.acquire()

	code = record.status_code[0]

	if code == '2':
		xx2 += 1
	elif code == '3':
		xx3 += 1
	elif code == '4':
		xx4 += 1
	elif code == '5':
		xx5 += 1

	total_bytes_sent += record.bytes_sent
	count += 1

	requests_processed += 1

	threadLock.release()


def process_records(records):
	for record in records:
		process_record(record)

def parse_process_logs(logs):
	records = parse_logs(logs)
	process_records(records)

# prints the summary and detailed table for the nginx logs after parsing is completed
def show_details():
	global requests_processed, total_time, requests_per_second, count, avg_bytes_sent, xx2, xx3, xx4, xx5

	print("Summary :")
	print("Number of requests processed : {0}".format(requests_processed))
	print("Total time: {0} sec".format(total_time))
	print("Request/sec: {0} req/sec".format(requests_per_second))

	table_data = [
		["count", "avg_bytes_sent", "2xx", "3xx", "4xx", "5xx"],
		[count, avg_bytes_sent, xx2, xx3, xx4, xx5]
	]

	table = AsciiTable(table_data)

	print()
	print(table.table)

def set_threadlock():
	global threadLock														# threadLock global variable\
	threadLock = threading.Lock()

def set_avg_bytes_sent():
	global total_bytes_sent, avg_bytes_sent, requests_processed
	avg_bytes_sent = total_bytes_sent / requests_processed

def set_initial_timestamp():
	global initial_timestamp
	initial_timestamp = time.time()

def set_total_time():
	global total_time, initial_timestamp
	total_time = time.time() - initial_timestamp

def set_requests_per_second():
	global requests_per_second, requests_processed, total_time
	requests_per_second = requests_processed / total_time


def open_file(access_log_path):
	try:
		access_log_file = open(access_log_path, 'r')	# read access log file
		return access_log_file
	except Exception as e:								# file can not be opened if
		print('Incorrect File or Path')					# file or path is Incorrect
		exit(0)
