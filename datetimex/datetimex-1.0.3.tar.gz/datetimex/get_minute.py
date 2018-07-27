from datetimex.log import d as log
import re

def get_text_minute(text,value,list):				##此方法作用为获取传入的中文的分数
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
		minute = re.findall('\d+',format_text,re.S)[-1]
		log(minute)
	except IndexError:			##此异常为下标越界，即没有找到指定元素，这里为字符串中没有找到数字，即遍历指定集合取出数字
		log('下标越界异常，改为通过汉字取数字')
		minute = False
		string = ''
		for x in text:
				if x in list:
					string += '1'				###为1代表这个是中文的数字，为0代表不是中文的数字
				else:
					string += '0'
		log('string为：'+string)
		log(text)
		try:
			text_number = text[string.rindex('0')+1:]		##取出最后一个'0'到字符串结尾之间的字符串，这子字符串即为所需的中文数字
		except ValueError:
			text_number = text
		except Exception as e:
			log('此处发生未知错误')
			log(e)
		for i in list:
			if i == text_number:
				minute = list[i]
				break
	except Exception as e:
			raise e
			log('中文分数获取发生未知异常')
	return int(minute)


def gettime_minute(text,value,time_now,list):			##此方法将获取指定的分数
	log('关键字为：'+value)
	text_minute = get_text_minute(text,value,list)			##此方法为获取传入的中文的分数
	now_minute = int(time_now[15:17])
	log('中文格式化后的分数：'+str(text_minute))
	if value == '分' or value == '分钟' or value == '分后' or value == '分之后' :
			minute = text_minute
	elif value == '分钟后'or value == '分钟之后':
		log('现在的分数：'+str(now_minute))
		minute = now_minute + text_minute
	elif value == '半小时' or value == '半个小时':
		minute = now_minute + 30
	elif value == '半':
		minute = '30'
	else:
		minute = '00'
		log('这里为没有定义的中文数字处理，暂时不作处理')
	log('分数暂时为：'+str(minute))
	minute = format(minute)
	return minute

def main(list,text,time_now,numberlist):
	log(list)
	value = list.get('value')
	text = list.get('text')
	log(value)
	log(text)
	if value == '':
		# if text == 'xx':
		# 	sencond = '00'
		# minute = time_now[15:17]
		minute = '00'
	else:
		minute = gettime_minute(text,value,time_now,numberlist)
	return minute