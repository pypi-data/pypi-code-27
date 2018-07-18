# import required modules
import time
from .argparser import options_handler
from .linear_parser import *

# main method
def main():
	"""
	main - Entry point to the application
	"""

	access_log_path, chunksize, follow  = options_handler()

	# threaded = False
	#
	# if chunksize is not None and chunksize != 0:
	# 	threaded = True

	threaded = chunksize is not None and chunksize != 0

	set_initial_timestamp()
	set_threadlock()

	try:
		if (not threaded) and (not follow):
			logs = read_logs(access_log_path)
			records = parse_logs(logs)
			process_records(records)

			set_avg_bytes_sent()
			set_total_time()
			set_requests_per_second()

			# displays summary
			show_details()
		elif (not threaded) and follow:
			myfile = open(access_log_path, 'r')
			# start_prompt_thread()
			while True:
				logs = myfile.readlines()
				if len(logs) is not 0:
					# print('Parsing Started')
					records = parse_logs(logs)
					process_records(records)

					set_avg_bytes_sent()
					set_total_time()
					set_requests_per_second()
					# print('Parsing Completed')
					# set_prompt_flag()

				else:
					time.sleep(10.0)
		else:
			threads = []
			flag = True
			access_log_file = open_file(access_log_path)

			while flag:
				lines = []
				for i in range(chunksize):
					line = access_log_file.readline()
					if not line:
						flag = False
						break
					lines.append(line)

				if len(lines) != 0:
					# print(lines)
					t = threading.Thread(target=parse_process_logs, args=(lines,))
					t.start()
					threads.append(t)

			for thread in threads:
				thread.join()

			set_avg_bytes_sent()
			set_total_time()
			set_requests_per_second()

			# displays summary
			show_details()
	except KeyboardInterrupt:
		show_details()
		exit(0)

if __name__ == '__main__':
	main()
