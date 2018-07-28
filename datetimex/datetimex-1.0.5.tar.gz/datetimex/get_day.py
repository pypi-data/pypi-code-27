from datetimex.log import d as log
import re,time,datetime

def get_text_day(text,value,list):				##此方法作用为获取传入的中文的天数
	text = text.split(value)[0]
	log('截取后字符串为：'+text)
	if text != '':
		format_text = text
	else:
		format_text = value
	try:
		data = ['年','月','日','星期','时','分','天','点',]
		for x in text:
			for i in data:
				if i == x:
					format_text = text.split(i)[-1]
		if '个' in format_text:
			format_text = format_text.split('个')[0]
		log('处理后的text:'+format_text)
		text = format_text
		day = re.findall('\d+',text,re.S)[-1]
		log(day)
	except IndexError:			##此异常为下标越界，即没有找到指定元素，这里为字符串中没有找到数字，即遍历指定集合取出数字
		day = False
		string = ''
		for x in text:
				if x in list:
					string += '1'				###为1代表这个是中文的数字，为0代表不是中文的数字
				else:
					string += '0'
		log('二进制后：'+string)
		try:
			index = string.rindex('0')
			log('index值：'+str(index))
			if index+1 >= len(text):
				text_number = text[:index]		##取出最后一个'0'到字符串开头之间的字符串，这子字符串即为所需的中文数字
				log('这里1'+text_number)
			else:
				text_number = text[index+1:]		##取出最后一个'0'到字符串结尾之间的字符串，这子字符串即为所需的中文数字
				log('这里2'+text_number)
		except ValueError:
			log('二次异常')
			text_number = text
		except Exception as e:
			log('此处发生未知错误')
			log(e)
		log(text_number)
		for i in list:
			if i == text_number:
				log('相等了')
				day = list[i]
				break
	except Exception as e:
			raise e
			log('中文天数获取发生未知异常')
	return int(day)


def gettime_day(text,value,time_now,list):			##此方法将获取指定的天数
	log('关键字为：'+value)
	text_day = get_text_day(text,value,list)			##此方法为获取传入的中文的天数
	now_day = int(time_now[6:8])
	log('中文格式化后的天数：'+str(text_day))
	if value == '号' or value == '日' or value == '号之后' or value == '号后':
		day = text_day
	elif value == '天之后' or value == '日之后' or value == '日后' or value == '天后':
		day = now_day + text_day
	elif value == '大前天' or value == '大后天' or value == '前日' or value == '昨日' or value == '今日' or value == '明日' or value == '后日' or value == '大后天' or value == '前天' or value == '昨天' or value == '今天' or value == '明天' or value == '后天' or value == '明天' or value == '明天' or value == '明天':
			dayvalue = int(text_day)
			today = datetime.date.today()
			tomorrow = str(today + datetime.timedelta(days=dayvalue)).replace('-','')
			day = tomorrow[6:8]
	elif value == '日' or value == '号':
		log('现在的天数：'+str(now_day))
		day = now_day + text_day
	elif value == '今' or value == '明' or value == '昨' or value == '前':			###这里为‘今晚**点’所用
		day = now_day
	else:
		day = now_day
		log('这里为没有定义的中文数字处理，暂时不作处理')
	log('天数暂时为：'+str(day))
	return day

def main(list,text,time_now,numberlist):
	log(list)
	value = list.get('value')
	text = list.get('text')
	log(value)
	log(text)
	if value == '':
		# if text == 'xx':
		# 	sencond = '00'
		day = time_now[6:8]
	else:
		day = gettime_day(text,value,time_now,numberlist)
	return day