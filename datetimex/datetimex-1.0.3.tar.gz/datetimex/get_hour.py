from datetimex.log import d as log
import re

def get_text_hour(text,value,list):				##此方法作用为获取传入的中文的时数
	text = text.split(value)[0]
	log('截取后字符串为：'+text)
	if text != '':
		format_text = text
	else:
		format_text = value
	try:
		data = ['年','月','日','星期','时','分','秒','点','上','下']
		for x in text:
			for i in data:
				if i == x:
					format_text = text.split(i)[-1]
		if '个' in format_text:
			format_text = format_text.split('个')[0]
		log('处理后的text:'+format_text)
		text = format_text
		hour = re.findall('\d+',format_text,re.S)[-1]
		log(hour)
	except IndexError:			##此异常为下标越界，即没有找到指定元素，这里为字符串中没有找到数字，即遍历指定集合取出数字
		hour = False
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
			text_number = text
		except Exception as e:
			log('此处发生未知错误')
			log(e)

		for i in list:
			if i == text_number:
				hour = list[i]
				break
	except Exception as e:
			raise e
			log('中文时数获取发生未知异常')
	return int(hour)


def gettime_hour(text,value,time_now,list):			##此方法将获取指定的时数
	log('关键字为：'+value)
	text_hour = get_text_hour(text,value,list)			##此方法为获取传入的中文的时数
	now_hour = int(time_now[13:15])
	log('中文格式化后的时数：'+str(text_hour))
	log(text)
	if value == '个小时后' or value == '小时之后' or value == '小时后' or value == '小时':
		hour = now_hour+text_hour
	elif value == '点之后' or value == '点之后' or value == '点' or value == '时':
		log('现在的时数：'+str(now_hour))
		hour = text_hour
	else:
		hour = time_now[13:15]
		log('这里为没有定义的中文数字处理，暂时不作处理')
	log('时数暂时为：'+str(hour))
	hour = format(hour)
	return hour

def main(list,text,time_now,numberlist):
	log(list)
	value = list.get('value')
	text = list.get('text')
	log(value)
	log(text)
	if value == '':
		# if text == 'xx':
		# 	sencond = '00'
		hour = time_now[13:15]
	else:
		hour = gettime_hour(text,value,time_now,numberlist)
	return hour