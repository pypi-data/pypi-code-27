from datetimex import main
import time

def gettime(text):
	timestamp=int(time.time())
	format_timestamp = time.localtime(int(time.time()))
	time_now = time.strftime("%Y%m%d%U%w%p%I%M%S", format_timestamp)				##格式：年月日周星期时分秒(12小时制)
	return_time = main.main(text,time_now)
	return return_time