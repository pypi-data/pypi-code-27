#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:秦洛
# 这是一个微信的群控系统，利用文件传输助手进行远程控制

import itchat
from itchat.content import *
import json
import time
import threading
import os
import re
import random


'''
全局变量
'''
LIST_CHATROOM = [] #群列表
SWITCH_MESSAGE = False #是否开启定时群消息
SWITCH_GREETING = False #是否开启新人入群自动打招呼
SWITCH_FRIEND = False #是否开启自动通过好友申请
SWITCH_AUTOFUNNY = False #是否开启群内指定消息的段子自动回复
CHATROOM_NAME_MESSAGE = ["咖喱的好笑群"] #定时发送群消息的群昵称
CHATROOM_SPAN = 3600 #发送群消息的间隔时间(S)
CHATROOM_NAME_GREETING = ['咖喱的好笑群'] #自动对新人打招呼的群昵称
CHATROOM_GREETING = 'Hi' #群内对新人的打招呼信息
CHATROOM_NAME_AUTOFUNNY = ["咖喱的好笑群"] #群内指定消息的段子自动回复的群昵称
CHATRROM_AUTOFUNNY = '群主最棒'
AUTOFUNNY_LASTTIME = int(time.time())-3600
AUTOFUNNY_SPAN = 3600
NEW_FRIEND_GREETING=('Hi[愉快]','很高兴认识你~以后我们就是朋友啦！','不过我可能不会经常在线，所以如果回复的不及时请见谅哦[偷笑]')#加好友后的打招呼信息
ALLCOMMAND = "开启(关闭)群消息\n开启(关闭)新人入群打招呼\n开启(关闭)好友申请\n开启(关闭)回复段子\n状态\n"






#BEGIN-----------------------------------手机远程控制模块----------------------------------------------
#说明：_command函数在msg_friend_text函数中调用，如果手机发送信息给‘文件传输助手’则调用这个控制模块

#好友发送的文本消息
@itchat.msg_register(TEXT)
def msg_friend_text(msg):
    #通过文件助手控制各个模块开关
    if msg['ToUserName'] == 'filehelper':
        _command(msg)

def _command(msg):
    global SWITCH_MESSAGE
    global SWITCH_GREETING
    global SWITCH_FRIEND
    global SWITCH_AUTOFUNNY
    if re.match(r'^help.*$',msg['Text']) != None:
        itchat.send(ALLCOMMAND, toUserName='filehelper')

    if re.match(r'^开启群消息.*$',msg['Text']) != None:
        SWITCH_MESSAGE = True
        itchat.send('已经开启群消息', toUserName='filehelper')
    if re.match(r'^关闭群消息.*$',msg['Text']) != None:
        SWITCH_MESSAGE = False
        itchat.send('已经关闭群消息', toUserName='filehelper')
    if re.match(r'^开启回复段子.*$',msg['Text']) != None:
        SWITCH_AUTOFUNNY = True
        itchat.send('已经开启回复段子', toUserName='filehelper')
    if re.match(r'^关闭回复段子.*$',msg['Text']) != None:
        SWITCH_AUTOFUNNY = False
        itchat.send('已经关闭回复段子', toUserName='filehelper')
    if re.match(r'^开启新人入群打招呼.*$',msg['Text']) != None:
        SWITCH_GREETING = True
        itchat.send('已经开启新人入群打招呼', toUserName='filehelper')
    if re.match(r'^关闭新人入群打招呼.*$',msg['Text']) != None:
        SWITCH_GREETING = False
        itchat.send('已经关闭新人入群打招呼', toUserName='filehelper')
    if re.match(r'^开启好友申请.*$',msg['Text']) != None:
        SWITCH_FRIEND = True
        itchat.send('已经开启好友申请', toUserName='filehelper')
    if re.match(r'^关闭好友申请.*$',msg['Text']) != None:
        SWITCH_FRIEND = False
        itchat.send('已经关闭好友申请', toUserName='filehelper')

    if re.match(r'^状态.*$',msg['Text']) != None:
        get_status()
    
#获取当前机器人状态
def get_status():
    result = "当前时间为:"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    result += "机器人当前状态：\n"
    if SWITCH_MESSAGE:
        result += "群消息功能: "+ "开启\n"
    else:
        result += "群消息功能: "+ "关闭\n"
    if SWITCH_AUTOFUNNY:
        result += "自动回复段子功能: "+ "开启\n"
    else:
        result += "自动回复段子功能: "+ "关闭\n"
    if SWITCH_GREETING:
        result += "新人问候功能: "+ "开启\n"
    else:
        result += "新人问候功能: "+ "关闭\n"
    if SWITCH_FRIEND:
        result += "自动通过好友申请: "+ "开启\n"
    else:
        result += "自动通过好友申请: "+ "关闭\n"
    itchat.send(result, toUserName='filehelper')

#END-----------------------------------手机远程控制模块----------------------------------------------

#BEGIN----------------------------------新好友请求自动添加模块-----------------------------------------

#新好友请求
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    if SWITCH_FRIEND:
        itchat.add_friend(**msg['Text'])# 该操作将自动将好友的消息录入，不需要重载通讯录
        #新好友的打招呼信息,延迟后发送打招呼信息
        itchat.send_msg(GREETING[0],msg['RecommendInfo']['UserName'])
        itchat.send_msg(GREETING[1],msg['RecommendInfo']['UserName'])
        itchat.send_msg(GREETING[2],msg['RecommendInfo']['UserName'])

#END-------------------------------------新好友请求自动添加模块-----------------------------------------


#BEGIN------------------------------------新人入群自动打招呼模块-----------------------------------------

#群内发送的通知
@itchat.msg_register([NOTE],isGroupChat=True)
def msg_chatroom_note(msg):
    #如果有新人加入群聊而且在群列表中z则发送打招呼消息
    if re.search(r'加入群聊',msg.Text)!=None and SWITCH_GREETING and _check_chatroom_name(msg.FromUserName, CHATROOM_NAME_GREETING):
        name = re.match(r'^"(.*?)".*$',msg.Text)[1]
        itchat.send("@"+name.strip()+" "+CHATROOM_GREETING, msg.FromUserName) 

#END------------------------------------新人入群自动打招呼模块-----------------------------------------

#BEGIN------------------------------------群内消息处理模块-----------------------------------------

#群内发送指定消息后自动回复段子
@itchat.msg_register([TEXT],isGroupChat=True)
def msg_chatroom_note(msg):
    global AUTOFUNNY_LASTTIME
    #如果群内成员发送指定内容
    if re.search(CHATRROM_AUTOFUNNY,msg.Text)!=None and SWITCH_AUTOFUNNY and _check_chatroom_name(msg.FromUserName, CHATROOM_NAME_AUTOFUNNY):
        if int(time.time()-AUTOFUNNY_LASTTIME) > AUTOFUNNY_SPAN:
            AUTOFUNNY_LASTTIME = int(time.time())
            funny = _get_joke()
            print(funny)
            print("\n")
            if funny == "":
                funny = "抱歉，脑子空空的，等会再讲段子"
            itchat.send(funny, msg.FromUserName) 

#END------------------------------------群内消息处理模块-----------------------------------------

#BEGIN------------------------------------定时给在特定的群里发送消息模块---------------------------------

#定时群消息 子线程
def batch_chatroom(names):
    global LIST_CHATROOM
    while True:
        if SWITCH_MESSAGE:
            msg = _get_joke()
            print(msg)
            print("\n")
            if msg=="":
                time.sleep(CHATROOM_SPAN)
                continue
            for chatroom in LIST_CHATROOM:
                if _check_chatroom_name(chatroom['UserName'],names):
                    itchat.send(msg, chatroom['UserName'])
        time.sleep(CHATROOM_SPAN)

#END------------------------------------定时给在特定的群里发送消息模块---------------------------------

#BEGIN------------------------------公共函数模块-------------------------------------------------------

#从storage/joke中提取一个段子
def _get_joke():
    #读取文本
    with open("storage/joke", 'r',encoding="utf8") as load_f:
        arr = load_f.read().split('|')
        msg = arr.pop()
    #回写文本
    with open("storage/joke", 'w',encoding="utf8") as load_f:
        load_f.write('|'.join(arr))
    return msg.strip()

#检查当前群名称是否符合指定群名称列表
def _check_chatroom_name(username,chatroomlist):
    nickname = _get_chatroom_nickname(username)
    for condi in chatroomlist:
        result = re.search(condi,nickname)
        if result != None:
            return True
    #所有关键字都不符合则返回False不打招呼
    return False

#根据群名称获取群昵称
def _get_chatroom_nickname(username):
    for chatroom in LIST_CHATROOM:
        if chatroom.UserName == username:
            return chatroom.NickName
    return ""

#END------------------------------公共函数模块-------------------------------------------------------


#主函数
def run(hot = False):
    global LIST_CHATROOM
    itchat.auto_login(hotReload=hot)
    #获取群列表
    LIST_CHATROOM = itchat.get_chatrooms(True)
    #开启定时群消息任务
    timing_joke = threading.Thread(target=batch_chatroom,args=(CHATROOM_NAME_MESSAGE,))
    timing_joke.start()
    #获取当前机器人状态
    get_status()
    #运行
    itchat.run()
    