from datetimex.log import d as log
import re

def get_text_sencond(text,value,list):				##此方法作用为获取传入的中文的秒数
	text = text.split(value)[0]
	log('截取后字符串为：'+text)
	format_text = text
	try:
		data = ['年','月','日','星期','时','分','秒','点',]
		for x in text:
			for i in data:
				if i == x:
					format_text = text.split(i)[-1]
		log('处理后的text:'+format_text)
		sencond = re.findall('\d+',format_text,re.S)[-1]
		log(sencond)
	except IndexError:			##此异常为下标越界，即没有找到指定元素，这里为字符串中没有找到数字，即遍历指定集合取出数字
		sencond = False
		string = ''
		for x in text:
				if x in list:
					string += '1'				###为1代表这个是中文的数字，为0代表不是中文的数字
				else:
					string += '0'
		try:
			text_number = text[string.rindex('0')+1:]		##取出最后一个'0'到字符串结尾之间的字符串，这子字符串即为所需的中文数字
		except ValueError:
			text_number = text
		except Exception as e:
			log('此处发生未知错误')
			log(e)
		for i in list:
			if i == text_number:
				sencond = list[i]
				break
	except Exception as e:
			raise e
			log('中文秒数获取发生未知异常')
	return int(sencond)


def gettime_second(text,value,time_now,list):			##此方法将获取指定的秒数
	log('关键字为：'+value)
	text_sencond = get_text_sencond(text,value,list)			##此方法为获取传入的中文的秒数
	now_sencond = int(time_now[17:])
	log('中文格式化后的秒数：'+str(text_sencond))
	if value == '秒' or value == '秒钟':
			sencond = text_sencond
	elif value == '秒后' or value == '秒钟后' or value == '秒之后' or value == '秒钟之后':
		log('现在的秒数：'+str(now_sencond))
		sencond = now_sencond + text_sencond
	else:
		sencond = '00'
		log('这里为没有定义的中文数字处理，暂时不作处理')
	log('秒数暂时为：'+str(sencond))
	return sencond

def main(list,text,time_now,numberlist):
	log(list)
	value = list.get('value')
	text = list.get('text')
	log(value)
	log(text)
	if value == '':
		# if text == 'xx':
		# 	sencond = '00'
		sencond = '00'
	else:
		sencond = gettime_second(text,value,time_now,numberlist)
	return sencond