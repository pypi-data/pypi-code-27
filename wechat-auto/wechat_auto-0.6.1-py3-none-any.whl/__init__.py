import itchat
from itchat.content import *
import json
import time
import threading
import os
import re
import random
from .components import AI
from .components import weather

'''
全局变量
'''
LIST_FRIENDS = [] #好友列表
LIST_CHATROOM = [] #群列表
SWITCH_AI = False #是否开启AI自动回复
SWITCH_GREET = False #是否开启定时问候
SWITCH_CHATROOM = False #是否开启定时群消息
SWITCH_GROUP = False #是否开启新人入群自动打招呼
ALLCOMMAND = "开启(关闭)AI回复\n开启(关闭)定时消息[,小时][,分钟]\n开启(关闭)群消息\n开启(关闭)群新人问候\n状态\n"
HOUR='8' #定时消息时针
MIN='0' #定时消息分针
GREETING=('Hi[愉快]','很高兴认识你~以后我们就是朋友啦！','不过我可能不会经常在线，所以如果回复的不及时请见谅哦[偷笑]')#加好友后的打招呼信息
MAX_COUNT = 100 #问候用户每天最大数量
CHATROOM_NAME = "咖喱的好笑群" #定时发送笑话的群昵称
CHATROOM_SPAN = 3600 #发送笑话间隔时间
FILTER_CHATROOM = ['咖喱的好笑群'] #过滤群昵称，这些群新人加入不自动打招呼
MESSAGE_CHATRROM = 'Hi' #群内对新人的打招呼信息



#BEGIN--------------------------------好友AI自动回复模块-----------------------------------------

#好友发送的文本消息
@itchat.msg_register(TEXT)
def msg_friend_text(msg):
    global SWITCH_AI
    #通过文件助手控制各个模块开关
    if msg['ToUserName'] == 'filehelper':
        _command(msg)
        return
    #开启后自动回复
    if SWITCH_AI and msg['User']['RemarkName']!='例外':
        return AI.get_msg(msg['Text'],msg['User']['UserName'][-32:-1])

#END--------------------------------好友AI自动回复模块---------------------------------------------


#BEGIN-------------------------------被删好友记录模块-----------------------------------------------------

#系统消息
#删除好友用户记录到本地文档，定期清理好友
@itchat.msg_register(NOTE)
def msg_friend_note(msg):
    #如果拉黑或者删除，则读取昵称写入文件
    if re.match(r'^.*开启了朋友验证，你还不是他（她）朋友.*$',msg['Text'])!=None or re.match(r'^消息已发出，但被对方拒收了.*$',msg['Text'])!=None:
        nickname=msg['User']['NickName']
        with open("storage/deleted_friend",'a+',encoding='utf8') as deleted_friend:
            deleted_friend.write(nickname+'\n')

#END-------------------------------被删好友记录模块-----------------------------------------------------

#BEGIN------------------------------------新人入群自动打招呼模块-----------------------------------------

#群内发送的通知
@itchat.msg_register([NOTE],isGroupChat=True)
def msg_chatroom_note(msg):
    #如果有新人加入群聊而且不在群过滤列表中怎么发送打招呼消息
    if re.search(r'加入群聊',msg.Text)!=None and SWITCH_GROUP and _check_chatroom_name(msg.FromUserName):
        name = re.match(r'^"(.*?)".*$',msg.Text)[1]
        itchat.send("@"+name.strip()+" "+MESSAGE_CHATRROM, msg.FromUserName) 

def _check_chatroom_name(username):
    nickname = _get_chatroom_nickname(username)
    for condi in FILTER_CHATROOM:
        result = re.search(condi,nickname)
        if result != None:
            return False
    #所有过滤关键字都不符合则返回真可以在群里发送打招呼消息
    return True

def _get_chatroom_nickname(username):
    for chatroom in LIST_CHATROOM:
        if chatroom.UserName == username:
            return chatroom.NickName
    return ""

#END------------------------------------新人入群自动打招呼模块-----------------------------------------


#BEGIN----------------------------------新好友请求自动添加模块-----------------------------------------

#新好友请求
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print(msg)
    #延时接受好友请求
    #time.sleep(10)
    itchat.add_friend(**msg['Text'])# 该操作将自动将好友的消息录入，不需要重载通讯录
    #新好友的打招呼信息,延迟后发送打招呼信息
    time.sleep(2)
    itchat.send_msg(GREETING[0],msg['RecommendInfo']['UserName'])
    time.sleep(5)
    itchat.send_msg(GREETING[1],msg['RecommendInfo']['UserName'])
    time.sleep(3)
    itchat.send_msg(GREETING[2],msg['RecommendInfo']['UserName'])

#END-------------------------------------新好友请求自动添加模块-----------------------------------------

#BEGIN-----------------------------------手机远程控制模块----------------------------------------------
#说明：_command函数在msg_friend_text函数中调用，如果手机发送信息给‘文件传输助手’则调用这个控制模块

def _command(msg):
    global SWITCH_AI
    global SWITCH_GREET
    global SWITCH_CHATROOM
    global SWITCH_GROUP
    global HOUR
    global MIN
    if re.match(r'^help.*$',msg['Text']) != None:
        itchat.send(ALLCOMMAND, toUserName='filehelper')
    if re.match(r'^开启AI回复.*$',msg['Text']) != None:
        SWITCH_AI = True
        itchat.send('已经开启AI回复', toUserName='filehelper')
    if re.match(r'^关闭AI回复.*$',msg['Text']) != None:
        SWITCH_AI = False
        itchat.send('已经关闭AI回复', toUserName='filehelper')
    if re.match(r'^开启定时消息.*$',msg['Text']) != None:
        #如果命令设置了时间，则设置时间
        t_hour = re.search(r'^开启定时消息,*([0-9]*),*([0-9]*).*$',msg['Text'])[1]
        t_min = re.search(r'^开启定时消息,*([0-9]*),*([0-9]*).*$',msg['Text'])[2]
        if t_hour!="":
            HOUR = t_hour
        if t_min!="":
            MIN = t_min
        SWITCH_GREET = True
        itchat.send('已经开启定时消息,时间为'+HOUR+"点"+MIN+"分", toUserName='filehelper')
    if re.match(r'^关闭定时消息.*$',msg['Text']) != None:
        SWITCH_GREET = False
        itchat.send('已经关闭定时消息', toUserName='filehelper')
    if re.match(r'^开启群消息.*$',msg['Text']) != None:
        SWITCH_CHATROOM = True
        itchat.send('已经开启定时群消息', toUserName='filehelper')
    if re.match(r'^关闭群消息.*$',msg['Text']) != None:
        SWITCH_CHATROOM = False
        itchat.send('已经关闭定时群消息', toUserName='filehelper')
    if re.match(r'^开启群新人问候.*$',msg['Text']) != None:
        SWITCH_GROUP = True
        itchat.send('已经开启群新人问候', toUserName='filehelper')
    if re.match(r'^关闭群新人问候.*$',msg['Text']) != None:
        SWITCH_GROUP = False
        itchat.send('已经关闭群新人问候', toUserName='filehelper')
    if re.match(r'^状态.*$',msg['Text']) != None:
        get_status()
    
#获取当前机器人状态
def get_status():
    result = "当前时间为:"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    result += "机器人当前状态：\n"
    if SWITCH_AI:
        result += "AI回复功能: "+ "开启\n"
    else:
        result += "AI回复功能: "+ "关闭\n"
    if SWITCH_GREET:
        result += "定时问候功能: 开启,"+HOUR+"点"+MIN+"分\n"
    else:
        result += "定时问候功能: "+ "关闭\n"
    if SWITCH_CHATROOM:
        result += "定时群消息: "+ "开启\n"
    else:
        result += "定时群消息: "+ "关闭\n"
    if SWITCH_GROUP:
        result += "群新人问候: "+ "开启\n"
    else:
        result += "群新人问候: "+ "关闭\n"
    itchat.send(result, toUserName='filehelper')

#END-----------------------------------手机远程控制模块----------------------------------------------

#BEGIN------------------------------------定时给好友发送问候信息（当地天气情况）模块----------------------

#定时问候 子线程
def batch_message(a):
    global SWITCH_GREET
    global LIST_FRIENDS
    friends = LIST_FRIENDS.copy()
    #读取好友地址，调用接口定时发送天气预报
    while True:
        #如果当前是凌晨1点，则重新初始化天气数据
        if time.localtime(time.time())[3]==1 and time.localtime(time.time())[4]==0:
            weather.init()

        if (SWITCH_GREET):
            if time.localtime(time.time())[3]==int(HOUR) and time.localtime(time.time())[4]==int(MIN):
                index = 0
                for friend in LIST_FRIENDS:
                    if index>MAX_COUNT:
                        break
                    weather_brief = _get_location_weather(friend, weather.CITYS_WEATHER)
                    itchat.send('@msg@'+"早上好 "+weather_brief,friend.UserName)
                    index += 1
                    time.sleep(1)
        time.sleep(60)

def _get_location_weather(friend, weathers):
    if friend['City'] in weathers:
        return  '\n'+weathers[friend['City']]
    if friend['Province'] in weathers:
        return  '\n'+weathers[friend['Province']]
    if '北京' in weathers:
        return  '\n'+weathers['北京']
    return ""

#BEGIN------------------------------------定时给好友发送问候信息（当地天气情况）模块----------------------

#BEGIN------------------------------------定时给在特定的群里发送消息模块---------------------------------

#定时群消息 子线程
def batch_chatroom(name):
    global LIST_CHATROOM
    while True:
        if SWITCH_CHATROOM:
            msg = _get_joke()
            print(msg)
            print("\n")
            if msg=="":
                time.sleep(CHATROOM_SPAN)
                continue
            for chatroom in LIST_CHATROOM:
                if re.search(r'^.*'+name+'.*$',chatroom['NickName'])!=None:
                    itchat.send(msg, chatroom['UserName'])
        time.sleep(CHATROOM_SPAN)

def _get_joke():
    #读取文本
    with open("storage/joke", 'r',encoding="utf8") as load_f:
        arr = load_f.read().split('|')
        msg = arr.pop()
    #回写文本
    with open("storage/joke", 'w',encoding="utf8") as load_f:
        load_f.write('|'.join(arr))
    return msg.strip()

#END------------------------------------定时给在特定的群里发送消息模块---------------------------------


#主函数
def run(hot = False):
    global LIST_FRIENDS
    global LIST_CHATROOM
    itchat.auto_login(hotReload=hot)
    #获取天气
    weather.init()
    #获取好友和群列表
    LIST_FRIENDS = itchat.get_friends(update=True)
    LIST_CHATROOM = itchat.get_chatrooms(True)
    random.shuffle(LIST_FRIENDS)
    #开启定时问候任务
    timing_greet = threading.Thread(target=batch_message,args=(1,))
    timing_greet.start()
    #开启定时群消息任务
    timing_joke = threading.Thread(target=batch_chatroom,args=(CHATROOM_NAME,))
    timing_joke.start()
    #获取当前机器人状态
    get_status()
    #运行
    itchat.run()
    