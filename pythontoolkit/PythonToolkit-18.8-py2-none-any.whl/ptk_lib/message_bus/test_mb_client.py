#!/usr/bin/env python
"""
Messenger Test external client

Started by the msgr_test program to test client connections
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
from wx_client import wxMBClient

class TestFrame(wx.Frame):
    def __init__(self,client):
        wx.Frame.__init__(self,None,-1,'MessageBus Client Test')
        
        #create client object
        self.client = client
        self.client.set_handler('Addressed Test',self.HandleMessages)
        self.client.subscribe('PublishTest.2', self.HandlePublished)

        size = wx.BoxSizer(wx.VERTICAL)

        #SendTo Button
        self.sendto = wx.Button(self,-1,'Send to Node.2')
        self.sendto.Bind(wx.EVT_BUTTON, self.OnSendTo)
        size.Add(self.sendto, 0, wx.EXPAND)

        #bad address
        self.sendto2 = wx.Button(self,-1,'Send to bad addrss')
        self.sendto2.Bind(wx.EVT_BUTTON, self.OnSendTo2)
        size.Add(self.sendto2, 0, wx.EXPAND)

        #Publish Button
        self.publish = wx.Button(self,-1,'Publish')
        self.publish.Bind(wx.EVT_BUTTON, self.OnPublish)
        size.Add(self.publish, 0, wx.EXPAND)

        #the text control to print message data to
        self.out = wx.TextCtrl(self,-1,'The messages data will appear here\n',
                                style=wx.TE_MULTILINE)
        size.Add(self.out, 1, wx.EXPAND)

        #set the sizer
        self.SetSizer(size)

    #---event handlers----------------------------------------------------------
    def OnSendTo(self,event):
        res = self.client.send_msg('Node.2', 'Addressed Test', data=('from client',), get_result=True)
        self.out.AppendText('result of sent message: '+str(res)+'\n')

    def OnSendTo2(self,event):
        res = self.client.send_msg('BadNodeName', 'Addressed Test', data=('from client',), get_result=True)
        self.out.AppendText('result of sent message: '+str(res)+'\n')

    def OnPublish(self,event):
        self.client.publish_msg( 'PublishTest.1', data=())
    
    #---message handlers--------------------------------------------------------
    def HandleMessages(self,msg):
        """Add the message data to the static text"""
        out = ('Client recieved: '+str(msg.subject)+' from: '+ 
                str(msg.from_node) + ' id:'+str(msg.msgid)+ 'data: '+str(msg.data))
        self.out.AppendText(out+'\n')
        return 'handled'

    def HandlePublished(self,msg):
        """Add the message data to the static text"""
        out = ('Published message: '+str(msg.subject)+' from: '+ 
                str(msg.from_node) + ' id:'+str(msg.msgid)+ 'data: '+str(msg.data))
        self.out.AppendText(out+'\n')
        return 'handled published'


if __name__=='__main__':
    #create the application instance
    _app = wx.PySimpleApp()  

    #create the client object
    client = wxMBClient( 'Client.#', timeout=10)
    client.connect('localhost',6669)

    #frame to control everything
    f = TestFrame(client)
    f.Show()

    #start main loop
    _app.MainLoop()

    #close the client
    client.disconnect()
