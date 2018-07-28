from datetimex.log import d as log
import re

def get_text_week(text,value,list):				##此方法作用为获取传入的中文的年数
	text = text.split(value)[0]
	log('截取后字符串为：'+text)
	if text != '':
		format_text = text
	else:
		format_text = value
	try:
		data = ['年','月','日','星期','时','分','年','点',]
		for x in text:
			for i in data:
				if i == x:
					format_text = text.split(i)[-1]
		log('处理后的text:'+format_text)
		text = format_text
		week = re.findall('\d+',format_text,re.S)[-1]
		log(week)
	except IndexError:			##此异常为下标越界，即没有找到指定元素，这里为字符串中没有找到数字，即遍历指定集合取出数字
		week = False
		string = ''
		for x in text:
				if x in list:
					string += '1'				###为1代表这个是中文的数字，为0代表不是中文的数字
				else:
					string += '0'
		log('string:'+string)
		try:
			index = string.rindex('0')
			log('index值：'+str(index))
			log(text)
			if index+1 >= len(text):
				text_number = text[:index]		##取出最后一个'0'到字符串开头之间的字符串，这子字符串即为所需的中文数字
				log('这里1:'+text_number)
			else:
				text_number = text[index+1:]		##取出最后一个'0'到字符串结尾之间的字符串，这子字符串即为所需的中文数字
				log('这里2:'+text_number)
		except ValueError:
			text_number = text
		except Exception as e:
			log('此处发生未知错误')
			log(e)
		for i in list:
			if i == text_number:
				week = list[i]
				break
	except Exception as e:
			raise e
			log('中文年数获取发生未知异常')
	return int(week)


def gettime_week(text,value,time_now,list):			##此方法将获取指定的年数
	log('关键字为：'+value)
	text_week = get_text_week(text,value,list)			##此方法为获取传入的中文的年数
	now_week = int(time_now[10:11])
	log('中文格式化后的年数：'+str(text_week))
	if value == '周末' or value == '周天' or value == '周日' or value == '星期日' or value == '星期天':
		week = '0'
	elif value == '周六' or value == '星期六':
		week = '6'
	elif value == '周五' or value == '星期五':
		week = '5'
	elif value == '周四' or value == '星期四':
		week = '4'
	elif value == '周三' or value == '星期三':
		week = '3'
	elif value == '周二' or value == '星期二':
		week = '2'
	elif value == '周一' or value == '星期一':
		week = '1'
	else:
		week = time_now[10:11]
		log('这里为没有定义的中文数字处理，暂时不作处理')
	log('星期数暂时为：'+str(week))
	return week

def main(list,text,time_now,numberlist):
	log(list)
	value = list.get('value')
	text = list.get('text')
	log(value)
	log(text)
	if value == '':
		# if text == 'xx':
		week = 'x'
		# week = time_now[10:11]
		print('测：'+week)
	else:
		week = gettime_week(text,value,time_now,numberlist)

	return week