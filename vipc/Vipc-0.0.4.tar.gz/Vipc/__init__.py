name="Vipc"
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
# import pandas   写csv文件
import json
import requests
from pyaudio import PyAudio,paInt16
import wave
import numpy as np
import pygame
import time
from aip import AipSpeech
import soundfile as sf
import matplotlib.pyplot as plt
import urllib
role = '女孩' #角色

APP_ID = '10698474'
API_KEY = 'hxGbVfeU15rnpw8s9SBWkixq'
SECRET_KEY = '48O289dZ81bALiWBGNySH6P91dtQ5zn5'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)




ipStr = 'http://jiaoxue.vipcode.cn/'

global filename
filename = ""
class PyQt5_QDialog (QDialog ):#line:3
    def __init__ (OO00OOOOOO00OO00O ):#line:4
        super ().__init__ ()#line:5
        OO00OOOOOO00OO00O .setObjectName ("dialog")#line:6
    def setBackground (O000O000O00O00OO0 ,OOO000O0O0OO00O00 ):#line:8
        O000O000O00O00OO0 .setStyleSheet ("#dialog{border-image:url(RESOURCE/drawable/"+OOO000O0O0OO00O00 +")}")#line:9
    def setResize (OOO00O000000O000O ,O00OOOOOOO00OOO0O ,O000O00OO00000000 ):#line:11
        OOO00O000000O000O .resize (O00OOOOOOO00OOO0O ,O000O00OO00000000 )#line:12
class PyQt5_QPushButton (QPushButton ):#line:15
    def __init__ (OOOOOO0000O000000 ,O0O0OO0O0OO0O00O0 ,x =0 ,y =0 ,width =113 ,height =32 ):#line:16
        super ().__init__ (O0O0OO0O0OO0O00O0 )#line:17
        OOOOOO0000O000000 .setGeometry (x ,y ,width ,height )#line:18
    def setBackground (O00O0OO0O0OOO00O0 ,OOOOOO0OO00000OO0 ):#line:20
        O00O0OO0O0OOO00O0 .setStyleSheet (O00O0OO0O0OOO00O0 .styleSheet ()+"QPushButton{border-image:url(RESOURCE/drawable/"+OOOOOO0OO00000OO0 +")}")#line:22
    def setPressedBackground (OO00OO0O000OOO0O0 ,O0O00OO00O0O0O00O ):#line:24
        OO00OO0O000OOO0O0 .setStyleSheet (OO00OO0O000OOO0O0 .styleSheet ()+"QPushButton:pressed{border-image:url(RESOURCE/drawable/"+O0O00OO00O0O0O00O +")}")#line:26
    def setBackgroundColor (O0000O0O0OOO00O00 ,O0O0OOOO00000O0O0 ):#line:28
        O0000O0O0OOO00O00 .setStyleSheet (O0000O0O0OOO00O00 .styleSheet ()+"QPushButton{background-color:"+O0O0OOOO00000O0O0 +"}")#line:29
    def setTextColor (O0000O0O0OOO0O0O0 ,O00O0OO00O0OOO00O ):#line:31
        O0000O0O0OOO0O0O0 .setStyleSheet (O0000O0O0OOO0O0O0 .styleSheet ()+"QPushButton{color:"+O00O0OO00O0OOO00O +"}")#line:32
    def setPressedTextColor (O0O000OOOOOO0000O ,OOOO0OOOO0000OOO0 ):#line:34
        O0O000OOOOOO0000O .setStyleSheet (O0O000OOOOOO0000O .styleSheet ()+"QPushButton:pressed{color:"+OOOO0OOOO0000OOO0 +"}")#line:35
    def setFontSize (O0O0O000O00O0000O ,O000OO000OOOO00O0 ):#line:37
        O000OO000000OOO0O =QFont ()#line:38
        O000OO000000OOO0O .setPixelSize (O000OO000OOOO00O0 )#line:39
        O0O0O000O00O0000O .setFont (O000OO000000OOO0O )#line:40
class PyQt5_QLineEdit (QLineEdit ):#line:43
    Password =QLineEdit .Password #line:44
    Normal =QLineEdit .Normal #line:45
    NoEcho =QLineEdit .NoEcho #line:46
    PasswordEchoOnEdit =QLineEdit .PasswordEchoOnEdit #line:47
    def __init__ (O000O000OO00O00OO ,OO0O00000O000O00O ,x =0 ,y =0 ,width =113 ,height =21 ):#line:49
        super ().__init__ (OO0O00000O000O00O )#line:50
        O000O000OO00O00OO .setGeometry (x ,y ,width ,height )#line:51
        O000O000OO00O00OO .setFontSize (14 )#line:52
        O000O000OO00O00OO .setAlignment (Qt .AlignVCenter )#line:53
    def setFontSize (OO0OOOOO0000O0OO0 ,OOO00OOOO000OO000 ):#line:55
        O000O00OOOOO00O00 =QFont ()#line:56
        O000O00OOOOO00O00 .setPixelSize (OOO00OOOO000OO000 )#line:57
        OO0OOOOO0000O0OO0 .setFont (O000O00OOOOO00O00 )#line:58
    def setBackground (O00O0OOO0OO0O00OO ,OOO000O0OO00OO00O ):#line:60
        O00O0OOO0OO0O00OO .setStyleSheet (O00O0OOO0OO0O00OO .styleSheet ()+"border-image:url(RESOURCE/drawable/"+OOO000O0OO00OO00O +");")#line:61
    def setBackgroundColor (OO0OO0O0OOO0000OO ,OOOOO000000OO0OOO ):#line:63
        OO0OO0O0OOO0000OO .setStyleSheet (OO0OO0O0OOO0000OO .styleSheet ()+"background-color:"+OOOOO000000OO0OOO +";")#line:64
    def setTextColor (OOO00OOOO0000OOOO ,O0OO0000000OOO0O0 ):#line:66
        OOO00OOOO0000OOOO .setStyleSheet (OOO00OOOO0000OOOO .styleSheet ()+"color:"+O0OO0000000OOO0O0 +";")#line:67
    def setDisplayMode (OOOO0OO0000OO0000 ,O0000OO0000O0000O ):#line:69
        if O0000OO0000O0000O ==PyQt5_QLineEdit .Password :#line:70
            OOOO0OO0000OO0000 .setEchoMode (O0000OO0000O0000O )#line:71
        elif O0000OO0000O0000O ==PyQt5_QLineEdit .Normal :#line:72
            OOOO0OO0000OO0000 .setEchoMode (O0000OO0000O0000O )#line:73
        elif O0000OO0000O0000O ==PyQt5_QLineEdit .NoEcho :#line:74
            OOOO0OO0000OO0000 .setEchoMode (O0000OO0000O0000O )#line:75
        elif O0000OO0000O0000O ==PyQt5_QLineEdit .PasswordEchoOnEdit :#line:76
            OOOO0OO0000OO0000 .setEchoMode (O0000OO0000O0000O )#line:77
class PyQt5_Qlabel (QLabel ):#line:81
    def __init__ (O0000OO0OO00OO0O0 ,OOOOO0OOOOO0000OO ,x =0 ,y =0 ,width =60 ,height =16 ):#line:82
        super ().__init__ (OOOOO0OOOOO0000OO )#line:83
        O0000OO0OO00OO0O0 .setGeometry (x ,y ,width ,height )#line:84
    def setFontSize (O000O00OO00000O0O ,OOOO0000OO00O0O00 ):#line:86
        O0O0OOO000O0OOO00 =QFont ()#line:87
        O0O0OOO000O0OOO00 .setPixelSize (OOOO0000OO00O0O00 )#line:88
        O000O00OO00000O0O .setFont (O0O0OOO000O0OOO00 )#line:89
    def setBackground (O00O0O00OO00O0OOO ,O00000OO00OO0000O ):#line:91
        O00O0O00OO00O0OOO .setStyleSheet (O00O0O00OO00O0OOO .styleSheet ()+"border-image:url(RESOURCE/drawable/"+O00000OO00OO0000O +");")#line:92
    def setBackgroundColor (O0OO00OO0OO0O00O0 ,O00OO0O00OO0OO0O0 ):#line:94
        O0OO00OO0OO0O00O0 .setStyleSheet (O0OO00OO0OO0O00O0 .styleSheet ()+"background-color:"+O00OO0O00OO0OO0O0 +";")#line:95
    def setTextColor (O0O000O0O0000O0O0 ,OO000O00OO0OO0O00 ):#line:97
        O0O000O0O0000O0O0 .setStyleSheet (O0O000O0O0000O0O0 .styleSheet ()+"color:"+OO000O00OO0OO0O00 +";")#line:98
class PyQt5_QMovie (QMovie ):#line:100
    def __init__ (OOOOO0OOOO0OOOOOO ,OO0000OO0OOO0O0OO ):#line:101
        super ().__init__ ("RESOURCE/gif/"+OO0000OO0OOO0O0OO )#line:102
class PyQt5_QMediaPlayer ():#line:104
    def __init__ (O0O000OOOOO00O0OO ,O0000O0O0O0O0O0O0 ):#line:105
        pygame .mixer .init ()#line:106
        O0O000OOOOO00O0OO .music =pygame .mixer .music #line:107
    def prepare_audio (OOO0OOO000O0OO0O0 ,O00O0O0OO0000O00O ):#line:108
        OOO0OOO000O0OO0O0 .music .load ("RESOURCE/audio/"+O00O0O0OO0000O00O )#line:109
    def prepare_voice (O0O0O0O00OOOOO00O ,OOOO0OOO0O0OOO000 ):#line:110
        O0O0O0O00OOOOO00O .music .load ("RESOURCE/voice/"+OOOO0OOO0O0OOO000 )#line:111
    def play (O00O000OO000000O0 ,loops =0 ,start =0.0 ):#line:112
        O00O000OO000000O0 .music .play (loops ,start )#line:113
    def stop (O000000OO0000O000 ):#line:114
        O000000OO0000O000 .music .stop ()#line:115
    def pause (OO00000OOO00O0OO0 ):#line:116
        OO00000OOO00O0OO0 .music .pause ()#line:117
    def setVolume (OOO0O00OOOOO000OO ,OO0O0O00OOO0OO000 ):#line:118
        OOO0O00OOOOO000OO .music .set_volume (OO0O0O00OOO0OO000 )#line:119
    def isPlaying (O00000O00OOO000O0 ):#line:120
        if O00000O00OOO000O0 .music .get_busy ()==1 :#line:121
            return True #line:122
        else :#line:123
            return False #line:124
class PyQt5_QCheckBox (QCheckBox ):#line:128
    def __init__ (OO0OO0O0OO0O000OO ,OOO0O0O0000000O0O ,x =0 ,y =0 ,width =20 ,height =20 ):#line:129
        super ().__init__ (OOO0O0O0000000O0O )#line:130
        OO0OO0O0OO0O000OO .setGeometry (x ,y ,width ,height )#line:131
        OO0OO0O0OO0O000OO .isIndicator =True #line:132
        OO0OO0O0OO0O000OO .image_name_normal =""#line:133
        OO0OO0O0OO0O000OO .image_name_pressed =""#line:134
    def setIndicator (O0OO0OOO0O000OO0O ,OO0O0O0O0O0OOOOO0 ):#line:136
        O0OO0OOO0O000OO0O .isIndicator =OO0O0O0O0O0OOOOO0 #line:137
        O0OO0OOO0O000OO0O .setStyleSheet ("")#line:138
        if O0OO0OOO0O000OO0O .image_name_normal !="":#line:139
            O0OO0OOO0O000OO0O .setUncheckedBackground (O0OO0OOO0O000OO0O .image_name_normal )#line:140
        if O0OO0OOO0O000OO0O .image_name_pressed !="":#line:141
            O0OO0OOO0O000OO0O .setCheckedBackground (O0OO0OOO0O000OO0O .image_name_pressed )#line:142
    def setUncheckedBackground (OOOO0OOO000O0OOO0 ,O00O0OOOO0OO0OOOO ):#line:144
        if OOOO0OOO000O0OOO0 .isIndicator :#line:145
            OOOO0OOO000O0OOO0 .setStyleSheet (OOOO0OOO000O0OOO0 .styleSheet ()+"QCheckBox:unchecked{width:"+str (OOOO0OOO000O0OOO0 .width ())+"px;height:"+str (OOOO0OOO000O0OOO0 .height ())+"px;border-image:url(RESOURCE/drawable/"+O00O0OOOO0OO0OOOO +")}")#line:148
        else :#line:149
            OOOO0OOO000O0OOO0 .setStyleSheet (OOOO0OOO000O0OOO0 .styleSheet ()+"QCheckBox:indicator:unchecked{width:"+str (OOOO0OOO000O0OOO0 .width ())+"px;height:"+str (OOOO0OOO000O0OOO0 .height ())+"px;border-image:url(RESOURCE/drawable/"+O00O0OOOO0OO0OOOO +")}")#line:152
        OOOO0OOO000O0OOO0 .image_name_normal =O00O0OOOO0OO0OOOO #line:153
    def setCheckedBackground (O0OO0O0O0O0OOOO0O ,O0OOO000000O0O000 ):#line:155
        if O0OO0O0O0O0OOOO0O .isIndicator :#line:156
            O0OO0O0O0O0OOOO0O .setStyleSheet (O0OO0O0O0O0OOOO0O .styleSheet ()+"QCheckBox:checked{width:"+str (O0OO0O0O0O0OOOO0O .width ())+"px;height:"+str (O0OO0O0O0O0OOOO0O .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OOO000000O0O000 +")}")#line:159
        else :#line:160
            O0OO0O0O0O0OOOO0O .setStyleSheet (O0OO0O0O0O0OOOO0O .styleSheet ()+"QCheckBox:indicator:checked{width:"+str (O0OO0O0O0O0OOOO0O .width ())+"px;height:"+str (O0OO0O0O0O0OOOO0O .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OOO000000O0O000 +")}")#line:163
        O0OO0O0O0O0OOOO0O .image_name_pressed =O0OOO000000O0O000 #line:164
class PyQt5_QRadioButton (QRadioButton ):#line:167
    def __init__ (OOO00OOO0O00O00O0 ,O000O0O00O0OO00OO ,x =0 ,y =0 ,width =20 ,height =20 ):#line:168
        super ().__init__ (O000O0O00O0OO00OO )#line:169
        OOO00OOO0O00O00O0 .setGeometry (x ,y ,width ,height )#line:170
        OOO00OOO0O00O00O0 .isIndicator =True #line:171
        OOO00OOO0O00O00O0 .image_name_normal =""#line:172
        OOO00OOO0O00O00O0 .image_name_pressed =""#line:173
    def setFontSize (O00OOOO0OO0OOO000 ,OO0O0OOOOO0OOOOOO ):#line:175
        OO0O0O0OOOO0O000O =QFont ()#line:176
        OO0O0O0OOOO0O000O .setPixelSize (OO0O0OOOOO0OOOOOO )#line:177
        O00OOOO0OO0OOO000 .setFont (OO0O0O0OOOO0O000O )#line:178
    def setTextColor (OO00O00O0OOOOO0OO ,OO0OOOOOOOOO00OOO ):#line:180
        OO00O00O0OOOOO0OO .setStyleSheet (OO00O00O0OOOOO0OO .styleSheet ()+"color:"+OO0OOOOOOOOO00OOO +";")#line:181
    def setIndicator (O0OOOO000O00O0000 ,O0OOOOOOO0O0OO00O ):#line:183
        O0OOOO000O00O0000 .isIndicator =O0OOOOOOO0O0OO00O #line:184
        O0OOOO000O00O0000 .setStyleSheet ("")#line:185
        if O0OOOO000O00O0000 .image_name_normal !="":#line:186
            O0OOOO000O00O0000 .setUncheckedBackground (O0OOOO000O00O0000 .image_name_normal )#line:187
        if O0OOOO000O00O0000 .image_name_pressed !="":#line:188
            O0OOOO000O00O0000 .setCheckedBackground (O0OOOO000O00O0000 .image_name_pressed )#line:189
    def setUncheckedBackground (O0OOO0O0O0O00OOOO ,O0OO00OO0OOOOO00O ):#line:191
        if O0OOO0O0O0O00OOOO .isIndicator :#line:192
            O0OOO0O0O0O00OOOO .setStyleSheet (O0OOO0O0O0O00OOOO .styleSheet ()+"QRadioButton:unchecked{width:"+str (O0OOO0O0O0O00OOOO .width ())+"px;height:"+str (O0OOO0O0O0O00OOOO .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OO00OO0OOOOO00O +")}")#line:195
        else :#line:196
            O0OOO0O0O0O00OOOO .setStyleSheet (O0OOO0O0O0O00OOOO .styleSheet ()+"QRadioButton:indicator:unchecked{width:"+str (O0OOO0O0O0O00OOOO .width ())+"px;height:"+str (O0OOO0O0O0O00OOOO .height ())+"px;border-image:url(RESOURCE/drawable/"+O0OO00OO0OOOOO00O +")}")#line:199
        O0OOO0O0O0O00OOOO .image_name_normal =O0OO00OO0OOOOO00O #line:200
    def setCheckedBackground (OOO00O0O00OOOO0OO ,O00O0O0OOOOOOO00O ):#line:202
        if OOO00O0O00OOOO0OO .isIndicator :#line:203
            OOO00O0O00OOOO0OO .setStyleSheet (OOO00O0O00OOOO0OO .styleSheet ()+"QRadioButton:checked{width:"+str (OOO00O0O00OOOO0OO .width ())+"px;height:"+str (OOO00O0O00OOOO0OO .height ())+"px;border-image:url(RESOURCE/drawable/"+O00O0O0OOOOOOO00O +")}")#line:206
        else :#line:207
            OOO00O0O00OOOO0OO .setStyleSheet (OOO00O0O00OOOO0OO .styleSheet ()+"QRadioButton:indicator:checked{width:"+str (OOO00O0O00OOOO0OO .width ())+"px;height:"+str (OOO00O0O00OOOO0OO .height ())+"px;border-image:url(RESOURCE/drawable/"+O00O0O0OOOOOOO00O +")}")#line:210
        OOO00O0O00OOOO0OO .image_name_pressed =O00O0O0OOOOOOO00O #line:211
class PyQt5_QGroupBox (QGroupBox ):#line:214
    def __init__ (O000O00OOO00O0000 ,O0OOOOOOOOO00O0OO ,x =0 ,y =0 ,width =120 ,height =80 ):#line:215
        super ().__init__ (O0OOOOOOOOO00O0OO )#line:216
        O000O00OOO00O0000 .setGeometry (x ,y ,width ,height )#line:217
        O000O00OOO00O0000 .setObjectName ("groupbox")#line:218
    def setBackground (O0O0O00O0OOOO00O0 ,OOOO00O00O00OOOOO ):#line:220
        O0O0O00O0OOOO00O0 .setStyleSheet ("#groupbox{border-image:url(RESOURCE/drawable/"+OOOO00O00O00OOOOO +")}")#line:221
    def setBackgroundColor (OOO0OO00000O0OO0O ,O00O0O0O000OOOOO0 ):#line:223
        OOO0OO00000O0OO0O .setStyleSheet ("#groupbox{background-color:"+O00O0O0O000OOOOO0 +"}")#line:224
    def setBorderWidth (O0OOO00O0OOOOOOOO ,OOOO0000OOO0O0000 ):#line:226
        O0OOO00O0OOOOOOOO .setStyleSheet (O0OOO00O0OOOOOOOO .styleSheet ()+"border-width:"+str (OOOO0000OOO0O0000 )+"px;border-style:solid;")#line:227
def getQuestion (O0O0OOO00O0OOOOO0 ):#line:230
    try :#line:231
        OOO0OOO0000O00000 =ipStr +'TiKu/ti/findById.do?id=%d'%O0O0OOO00O0OOOOO0 #line:233
        OOO0OOO0000O00000 =urllib .request .Request (url =OOO0OOO0000O00000 )#line:234
        OOO0OOO0000O00000 .add_header ('Content-Type','application/json')#line:235
        OO000O000OO0OOO0O =urllib .request .urlopen (OOO0OOO0000O00000 )#line:236
    except urllib .error .URLError as OO00OO00OO0O0OO00 :#line:237
        OOOOOOO00OO0O00O0 ={"id":1 ,"wenti":"由于网络问题未找到所需内容，请检查您的网络","daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:238
        return OOOOOOO00OO0O00O0 #line:239
    OOOOOOO00OO0O00O0 =json .loads (OO000O000OO0OOO0O .read ().decode ('utf-8'))#line:241
    print (OOOOOOO00OO0O00O0 )#line:242
    if OOOOOOO00OO0O00O0 :#line:244
        if OOOOOOO00OO0O00O0 ["state"]!=0 :#line:245
            return {"id":1 ,"wenti":OOOOOOO00OO0O00O0 ["message"],"daan":"0","jiexi":"  ","a":" ","b":" ","c":" ","d":" "}#line:246
        else :#line:247
            return OOOOOOO00OO0O00O0 ["data"]#line:248
def checkedRight (O00000O0000OO000O ,O0O00O00OOO0O0O0O ):#line:249
    for OO000000O0000OOOO in range (len (O0O00O00OOO0O0O0O )):#line:250
        if OO000000O0000OOOO ==O00000O0000OO000O :#line:251
            O0O00O00OOO0O0O0O [O00000O0000OO000O ].setTextColor ("blue")#line:252
        else :#line:253
            O0O00O00OOO0O0O0O [OO000000O0000OOOO ].setTextColor ("gray")#line:254
def checkedFalse (O0O00OOO00O0OOOO0 ,O00000O0000O000OO ,OO00OOOOO00000O0O ):#line:255
    for OO0O000O0000O00O0 in range (len (OO00OOOOO00000O0O )):#line:256
        if OO0O000O0000O00O0 ==O00000O0000O000OO :#line:257
            OO00OOOOO00000O0O [O00000O0000O000OO ].setTextColor ("red")#line:258
        elif OO0O000O0000O00O0 ==O0O00OOO00O0OOOO0 :#line:259
            OO00OOOOO00000O0O [OO0O000O0000O00O0 ].setTextColor ("blue")#line:260
        else :#line:261
            OO00OOOOO00000O0O [OO0O000O0000O00O0 ].setTextColor ("gray")#line:262
def reductionRadioBtn (OO0000OOOOOO00OO0 ):#line:263
    for OOO00O0000000O0OO in range (len (OO0000OOOOOO00OO0 )):#line:264
        OO0000OOOOOO00OO0 [OOO00O0000000O0OO ].setCheckable (False )#line:266
        OO0000OOOOOO00OO0 [OOO00O0000000O0OO ].setCheckable (True )#line:267
def changeFoodNum (OO0OO0O000O0OOO00 ,O00O00OO0OOOOO000 ):#line:270
    OOOO0O00O00O0O000 =ipStr +'TiKu/person/findUser.do?users='+OO0OO0O000O0OOO00 #line:272
    O0O00OO000OOO0OOO =urllib .request .urlopen (OOOO0O00O00O0O000 )#line:274
    OOO00O0OO0O0OO000 =json .loads (O0O00OO000OOO0OOO .read ().decode ('utf-8'))#line:276
    if OOO00O0OO0O0OO000 ["state"]==0 :#line:278
        O0OO0OO0O0OO0OOO0 =OOO00O0OO0O0OO000 ["data"]#line:280
        O000OOO000O00OO0O =O0OO0OO0O0OO0OOO0 ["foodData"]+O00O00OO0OOOOO000 #line:281
        O00O000O00OO0OO0O ='users='+OO0OO0O000O0OOO00 +'&foodData='+str (O000OOO000O00OO0O )#line:282
        OOOO0O00O00O0O000 =ipStr +'TiKu/person/updateFoodData.do?'+O00O000O00OO0OO0O #line:283
        O00O0O00OO0OOOO00 =requests .post (OOOO0O00O00O0O000 )#line:284
        OOO00O0OO0O0OO000 =json .loads (O00O0O00OO0OOOO00 .text )#line:285
        if OOO00O0OO0O0OO000 ['state']==0 :#line:286
           return O000OOO000O00OO0O #line:287
        else :#line:288
            print (OOO00O0OO0O0OO000 ['message'])#line:289
    else :#line:290
        print (OOO00O0OO0O0OO000 ["message"])#line:291
