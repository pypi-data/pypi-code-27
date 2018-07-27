from datetimex.log import d as log
import re
 
def get_text_weeknum(text,value,list):				##此方法作用为获取传入的中文的年数
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
		weeknum = re.findall('\d+',format_text,re.S)[-1]
		log(weeknum)
	except IndexError:			##此异常为下标越界，即没有找到指定元素，这里为字符串中没有找到数字，即遍历指定集合取出数字
		weeknum = False
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
				weeknum = list[i]
				break
	except Exception as e:
			raise e
			log('中文年数获取发生未知异常')
	return int(weeknum)


def gettime_weeknum(text,value,time_now,list):			##此方法将获取指定的年数
	log('关键字为：'+value)
	text_weeknum = get_text_weeknum(text,value,list)			##此方法为获取传入的中文的年数
	now_weeknum = int(time_now[8:10])
	log('中文格式化后的年数：'+str(text_weeknum))
	if value == '这星期' or value == '这一周' or value == '这周':
		weeknum = now_weeknum
	elif value == '上星期' or value == '上个周' or value == '上周':
		weeknum = now_weeknum - 1
	elif value == '下星期' or value == '下个周' or value == '下周':
		weeknum = now_weeknum + 1
	elif value == '星期' or value == '周':
		weeknum = time_now[8:10]
	else:
		weeknum = time_now[8:10]
		log('这里为没有定义的中文数字处理，暂时不作处理')
	log('周数暂时为：'+str(weeknum))
	weeknum = format(weeknum)
	return weeknum

def main(list,text,time_now,numberlist):
	log(list)
	value = list.get('value')
	text = list.get('text')
	log(value)
	log(text)
	if value == '':
		# if text == 'xx':
		weeknum = 'xx'
		# weeknum = time_now[8:10]
	else:
		weeknum = gettime_weeknum(text,value,time_now,numberlist)
	return weeknum