from datetimex import get_second
from datetimex import get_minute
from datetimex import get_hour
from datetimex import get_ampm
from datetimex import get_week
from datetimex import get_weeknum
from datetimex import get_day
from datetimex import get_month
from datetimex import get_year
from datetimex.log import d as log
from datetime import datetime
import time,calendar


numberlist = {
	'前':-2,'前一':-1,'昨':-1,'上':-1,'去':-1,'今':0,'这':0,'一':1,'明':1,'下':1,'后一':1,'后':2,'二':2,'两':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,
	'十一':11,'十二':12,'十三':13,'十四':14,'十五':15,'十六':16,'十七':17,'十八':18,'十九':19,'二十':20,
	'二十一':21,'二十二':22,'二十三':23,'二十四':24,'二十五':25,'二十六':26,'二十七':27,'二十八':28,'二十九':29,'三十':30,
	'三十一':31,'三十二':32,'三十三':33,'三十四':34,'三十五':35,'三十六':36,'三十七':37,'三十八':38,'三十九':39,'四十':40,
	'四十一':41,'四十二':42,'四十三':43,'四十四':44,'四十五':45,'四十六':46,'四十七':47,'四十八':48,'四十九':49,'五十':50,
	'五十一':51,'五十二':52,'五十三':53,'五十四':54,'五十五':55,'五十六':56,'五十七':57,'五十八':58,'五十九':59,'六十':60,
	'六十一':61,'六十二':62,'六十三':63,'六十四':64,'六十五':65,'六十六':66,'六十七':67,'六十八':68,'六十九':69,'七十':70,
	'七十一':71,'七十二':72,'七十三':73,'七十四':74,'七十五':75,'七十六':76,'七十七':77,'七十八':78,'七十九':79,'八十':80,
	'八十一':81,'八十二':82,'八十三':83,'八十四':84,'八十五':85,'八十六':86,'八十七':87,'八十八':88,'八十九':89,'九十':90,
	'九十一':91,'九十二':92,'九十三':93,'九十四':94,'九十五':95,'九十六':96,'九十七':97,'九十八':98,'九十九':99,'一百':100,
}

keyword_second = ['秒钟之后','秒之后','秒钟后','秒后','秒钟','秒']
keyword_minute = ['分钟之后','半个小时','分之后','分钟后','半小时','分后','分钟','分','半']
keyword_hour = ['个小时后','小时之后','点之后','小时后','点后','小时','时','点']
keyword_day = ['号之后','天之后','日之后','大前天','大后天','前日','昨日','今日','明日','后日','日后','前天','昨天','今天','明天','后天','天后','号后','日','号','今','明','昨','前']
keyword_month = ['个月份之后','下一个月份','上一个月份','这一个月份','个月份后','下一个月','月份之后','个月之后','后一个月','前一个月','上个月份','这个月份','上个月','这个月','下个月','月份后','个月后','上月','月份','月']
keyword_year = ['年之后','前年','去年','今年','明年','后年','年后','年']
keyword_ampm = ['上午','中午','下午','傍晚','晚上','夜晚','凌晨','早上','深夜','晚','夜']
keyword_weeknum = ['这星期','上星期','下星期','这个周','上个周','下个周','上一周','这一周','下一周','这周','上周','下周','星期','周']
keyword_week = ['星期天','星期一','星期二','星期三','星期四','星期五','星期六','星期日','周日','周天','周一','周二','周三','周四','周五','周六','周末']
keyword_static = ['后']

keywords = {
	'second':{'name':'second','list':keyword_second},
	'minute':{'name':'minute','list':keyword_minute},
	'hour':{'name':'hour','list':keyword_hour},
	'ampm':{'name':'ampm','list':keyword_ampm},
	'day':{'name':'day','list':keyword_day},
	'month':{'name':'month','list':keyword_month},
	'year':{'name':'year','list':keyword_year},
	'weeknum':{'name':'weeknum','list':keyword_weeknum},
	'week':{'name':'week','list':keyword_week}
}

def format(timedata):				##格式化，如果数据为一位，则在前面加上一个字符串0
	if(len(str(timedata)) == 1):
		log('这里进行字符串长度格式化')
		timedata = '0'+str(timedata)
	else:
		timedata = str(timedata)
	return timedata

def get_time_text(name,list,text):				##返回值为通过定义的值截取后返回的字符串以及值，例：{'name':'minute','value': '半', 'minute_text': '明天早上7点'}
	value = ''
	returnlist = {}
	for x in list:
		if x in text:
			value = x
			break
	if value == '':
		data = 'xx'
	else:
		data = text.split(value)[0]
	returnlist = {
		'name':name,
		'value':value,
		'text':data
	}
	value = ''
	return returnlist

def main(text,time_now):
	timelist = []
	for x in keywords:
		returnlist = get_time_text(keywords.get(x).get('name'),keywords.get(x).get('list'),text)
		timelist.append(returnlist)
	for i in timelist:
		if i.get('name') == 'second':
			second = format(get_second.main(i,text,time_now,numberlist))
			log('秒数为：'+second)
		elif i.get('name') == 'minute':
			minute = format(get_minute.main(i,text,time_now,numberlist))
			log('分数为：'+minute)
		elif i.get('name') == 'hour':
			hour = format(get_hour.main(i,text,time_now,numberlist))
			log('时数为：'+hour)
		elif i.get('name') == 'ampm':
			ampm = format(get_ampm.main(i,text,time_now))
		elif i.get('name') == 'day':
			day = format(get_day.main(i,text,time_now,numberlist))
		elif i.get('name') == 'month':
			month = format(get_month.main(i,text,time_now,numberlist))
		elif i.get('name') == 'year':
			year = format(get_year.main(i,text,time_now,numberlist))
		elif i.get('name') == 'weeknum':
			weeknum = format(get_weeknum.main(i,text,time_now,numberlist))
		elif i.get('name') == 'week':
			week = str(get_week.main(i,text,time_now,numberlist))
	if weeknum+week == 'xxxx':				##这里代表没有相关字眼，即用日期转成周数和星期
		result = datetime.strptime(year+month+day,"%Y%m%d").strftime("%U%w")
		log('日期转周-星期')
		result = year+month+day+result+ampm+hour+minute+second
	else:
		result = datetime.strptime(weeknum+week,"%U%w").strftime("%m%d")
		log('周-星期转-月日')
		result = time_now[0:4]+result+weeknum+week+ampm+hour+minute+second
	log('初步结果：'+result)

	return result
