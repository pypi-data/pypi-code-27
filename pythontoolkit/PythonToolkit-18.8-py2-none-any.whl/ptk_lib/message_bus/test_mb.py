#!/usr/bin/env python
"""
MessageBus Test:

Create a master Message and a frame with:
    a sendto message button,
    a publish message
    a sendto message from thread button
    a publish message from thread button

    a launch external client
    a sendto external client
    a text control to print the message data to

The external client registers for the published messages and it's own
address
"""
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

#add the parent directory to the sys path in order to find other components
import sys
import os
startdir = os.path.dirname(__file__)
compdir = os.path.split(startdir)[0]
sys.path.append(compdir)
del os,startdir,compdir

import wx
from wx_message_bus import wxMessageBus
from mb_node import MBLocalNode

#for testing threads
import threading
import time

#for launching client
import subprocess
import sys

#-------------------------------------------------------------------------------
class TestThread(threading.Thread):
    def __init__(self,mb,n):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.node=MBLocalNode('Thread.'+str(n))
        self.node.connect(mb)

        self._stop = False
        self.n = n

    def run(self):
        while self._stop is False:
            res = self.node.send_msg('Node.1','Addressed Test',
                                ('This is an addressed message from a thread ' +
                                str(self.n),), get_result=True) 
            self.node.publish_msg('PublishTest.2',('this is the result from the thread '+
                                str(self.n)+' : '+str(res),))
            time.sleep(5)

    def stop(self):
        self._stop=True
        self.node.disconnect()

#-------------------------------------------------------------------------------
class TestFrame(wx.Frame):
    def __init__(self,mb):
        wx.Frame.__init__(self,None,-1,'MessageBus Test')
        self.mb = mb

        if self.mb.has_server() is False:
            self.mb.start_server(port=6669, allow_ext=False)

        size = wx.BoxSizer(wx.VERTICAL)

        #create node0
        self.node0 = MBLocalNode('Node.#')
        self.node0.connect(mb)
        self.node0.set_handler('Addressed Test',self.HandleMessages0)
        self.node0.subscribe('PublishTest', self.HandleMessages0)

        #create node1
        self.node1 = MBLocalNode('Node.#')
        self.node1.connect(mb)
        self.node1.set_handler('Addressed Test',self.HandleMessages1)
        self.node1.subscribe('PublishTest.1', self.HandleMessages1)


        #create node2 - used to ensure message arenot going astray
        self.node2 = MBLocalNode('Node.#')
        self.node2.connect(mb)
        self.node2.set_handler('Addressed Test',self.HandleMessages2)

        #Send Buttons
        self.send01 = wx.Button(self,-1,'Send Node.0 -> Node.1')
        self.send01.Bind(wx.EVT_BUTTON, self.OnSend01)
        size.Add(self.send01, 0, wx.EXPAND)

        self.send10 = wx.Button(self,-1,'Send Node.1 -> Node.0')
        self.send10.Bind(wx.EVT_BUTTON, self.OnSend10)
        size.Add(self.send10, 0, wx.EXPAND)

        self.send2c = wx.Button(self,-1,'Send Node.2 -> Client.0')
        self.send2c.Bind(wx.EVT_BUTTON, self.OnSend2c)
        size.Add(self.send2c, 0, wx.EXPAND)

        self.pub1 = wx.Button(self,-1,'Publish Test1')
        self.pub1.Bind(wx.EVT_BUTTON, self.OnPub1)
        size.Add(self.pub1, 0, wx.EXPAND)

        self.pub2 = wx.Button(self,-1,'Publish Test2 (client subscribes)')
        self.pub2.Bind(wx.EVT_BUTTON, self.OnPub2)
        size.Add(self.pub2, 0, wx.EXPAND)

        #Start a thread
        self.startt = wx.Button(self,-1,'Start Thread')
        self.startt.Bind(wx.EVT_BUTTON, self.OnStartThread)
        size.Add(self.startt, 0, wx.EXPAND)

        #stop all threads
        self.stopt = wx.Button(self,-1,'Stop Threads')
        self.stopt.Bind(wx.EVT_BUTTON, self.OnStopThreads)
        size.Add(self.stopt, 0, wx.EXPAND)
        self.threads=[]

        #External client Button
        self.lclient = wx.Button(self,-1,'Launch client')
        self.lclient.Bind(wx.EVT_BUTTON, self.OnLaunchClient)
        size.Add(self.lclient, 0, wx.EXPAND)

        #the text control to print message data to
        self.out = wx.TextCtrl(self,-1,'The messages data will appear here\n',
                                style=wx.TE_MULTILINE)
        size.Add(self.out, 1, wx.EXPAND)

        #set the sizer
        self.SetSizer(size)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    #---event handlers----------------------------------------------------------
    def OnClose(self,event):
        for t in self.threads:
            t.stop()
        self.threads=[]
        #shutdown message bus
        self.mb.shutdown()
        event.Skip()

    #---------------------------------------------------------------------------
    def OnSend01(self,event):
        res = self.node0.send_msg( 'Node.1', 'Addressed Test', data=(1,2,3),get_result=True)
        self.out.AppendText('Send01 reply: '+str(res)+'\n')

    def OnSend10(self,event):
        res = self.node1.send_msg( 'Node.0', 'Addressed Test', data=(1,2,3), get_result=True)
        self.out.AppendText('Send10 reply: '+str(res)+'\n')

    def OnSend2c(self,event):
        res = self.node2.send_msg( 'Client.0', 'Addressed Test', data=(1,2,3), get_result=True)
        self.out.AppendText('Send2c reply: '+str(res)+'\n')

    #---------------------------------------------------------------------------
    
    def OnPub1(self,event):
        self.node1.publish_msg( 'PublishTest.1', data=('test',))

    def OnPub2(self,event):
        self.node2.publish_msg( 'PublishTest.2', data=(1.23,))

    def OnStartThread(self,event):
        t = TestThread(self.mb,len(self.threads)+1)
        self.threads.append(t)
        t.start()

    def OnStopThreads(self,event):
        for t in self.threads:
            t.stop()
        self.threads=[]

    def OnLaunchClient(self,event):
        if self.mb.has_server() is False:
            self.mb.start_server(port=6669,allow_ext=False)

        #arguments for external process
        shell = True
        if sys.platform=='win32':
            args = ['test_mb_client.py']
        else:
            args = ['"./test_mb_client.py"']
        #create process
        self.process = subprocess.Popen(args,shell=shell)

    #---message handlers--------------------------------------------------------
    def HandleMessages0(self,msg):
        """Add the message data to the static text"""
        out = ('Node.0 recieved message: '+str(msg.subject)+' from: '+ 
                str(msg.from_node) + ' id:'+str(msg.msgid)+ 'data: '+str(msg.data))
        self.out.AppendText(out+'\n')
        return 'handled0'

    def HandleMessages1(self,msg):
        """Add the message data to the static text"""
        out = ('Node.1 recieved message: '+str(msg.subject)+' from: '+ 
                str(msg.from_node) + ' id:'+str(msg.msgid)+ 'data: '+str(msg.data))
        self.out.AppendText(out+'\n')
        return 'handled1'

    def HandleMessages2(self,msg):
        """Add the message data to the static text"""
        out = ('Node.2 recieved message: '+str(msg.subject)+' from: '+ 
                str(msg.from_node) + ' id:'+str(msg.msgid)+ 'data: '+str(msg.data))
        self.out.AppendText(out+'\n')
        return 'handled2'

#-------------------------------------------------------------------------------
node_count = 0

def get_node_number():
    global node_count
    name = 'Node:'+str(node_count)
    node_count= node_count+1
    print 'in group callback: asigning node name:',name
    return name

#-------------------------------------------------------------------------------
if __name__=='__main__':


    #create the application instance
    _app = wx.PySimpleApp()  
    mb = wxMessageBus()
    mb.register_node_group('Node', get_node_number)
    f = TestFrame(mb)
    f.Show()
    #start main loop
    _app.MainLoop()


