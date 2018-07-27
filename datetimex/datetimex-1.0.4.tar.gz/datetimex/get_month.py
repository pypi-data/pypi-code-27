from datetimex.log import d as log
import re,time

def get_text_month(text,value,list):				##此方法作用为获取传入的中文的月数
	text = text.split(value)[0]
	log('截取后字符串为：'+text)
	if text != '':
		format_text = text
	else:
		format_text = value
	try:
		data = ['年','月','日','星','时','分','秒','点',]
		for x in text:
			for i in data:
				if i == x:
					format_text = text.split(i)[-1]
		log('text:'+format_text)
		if '个' in format_text:
			format_text = format_text.split('个')[0]
		log('处理后的text:'+format_text)
		text = format_text
		month = re.findall('\d+',format_text,re.S)[-1]
		log(month)
	except IndexError:			##此异常为下标越界，即没有找到指定元素，这里为字符串中没有找到数字，即遍历指定集合取出数字
		month = False
		string = ''
		for x in text:
			if x in list:
				string += '1'				###为1代表这个是中文的数字，为0代表不是中文的数字
			else:
				string += '0'
		log('测试这里')
		log(string)

		log(text)
		try:
			index = string.rindex('0')
			log('index值：'+str(index))
			log(text)
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
				month = list[i]
				break
		log("测："+str(month))
	except Exception as e:
			raise e
			log('中文月数获取发生未知异常')
	return int(month)


def gettime_month(text,value,time_now,list):			##此方法将获取指定的月数
	log('关键字为：'+value)
	text_month = get_text_month(text,value,list)			##此方法为获取传入的中文的月数
	now_month = int(time_now[4:6])
	log('中文格式化后的月数：'+str(text_month))
	if value == '上月' or value == '上个月' or value == '前一个月' or value == '这个月' or value == '下一个月' or value == '下个月' or value == '后一个月':
		month = now_month + text_month
	elif value == '月' or value == '月份':
		month = text_month
	elif value == '个月之后' or value == '月之后' or value == '个月后':
		month = now_month + text_month
	else:
		month = time_now[4:6]
		log('这里为没有定义的中文数字处理，暂时不作处理')
	log('月数暂时为：'+str(month))
	month = format(month)
	return month

def main(list,text,time_now,numberlist):
	log(list)
	value = list.get('value')
	text = list.get('text')
	log(value)
	log(text)
	if value == '':
		# if text == 'xx':
		# 	sencond = '00'
		month = time_now[4:6]
	else:
		month = gettime_month(text,value,time_now,numberlist)
	return month