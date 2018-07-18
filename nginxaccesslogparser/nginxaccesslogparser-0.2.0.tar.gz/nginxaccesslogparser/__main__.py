# import required modules
from .argparser import options_handler
from .linear_parser import *

# main method - Entry point to the application
def main():
	"""
	main - Entry point to the application
	"""

	access_log_path, chunksize = options_handler()

	threaded = False

	if chunksize is not None and chunksize != 0:
		threaded = True

	set_initial_timestamp()
	set_threadlock()

	try:
		if not threaded:
			logs = read_logs(access_log_path)
			records = parse_logs(logs)
			process_records(records)
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
	except KeyboardInterrupt:
		exit(0)

	set_avg_bytes_sent()
	set_total_time()
	set_requests_per_second()

	# displays summary
	show_details()


if __name__=="__main__":
	main()
