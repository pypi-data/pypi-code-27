"""
wxPython messagebus client

"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)
#-------------------------------------------------------------------------------

#wx imports
import wx                       
import wx.lib.newevent

from mb_client import MBClient
import mb_protocol
from wx_message_bus import EvtMsg_Publish, EVT_MSG_PUBLISH , EvtMsg_Send , EVT_MSG_SEND

#-------------------------------------------------------------------------------
class wxMBClient(MBClient):
    def __init__(self, name='Client.#', timeout=10):
        MBClient.__init__(self,name,timeout)

        #create a wx event handler to catch messenger events
        self.evt_hndlr = wx.EvtHandler()
        self.evt_hndlr.Bind(EVT_MSG_PUBLISH, self.on_evt_publish)
        self.evt_hndlr.Bind(EVT_MSG_SEND,  self.on_evt_send)

    def process_msg(self, msg):
        evt = EvtMsg_Send(msg=msg)
        #post the event
        wx.PostEvent(self.evt_hndlr, evt)

    def process_published(self, msg):
        #create the event
        evt = EvtMsg_Publish(msg=msg)
        #post the event
        wx.PostEvent(self.evt_hndlr, evt)

    #---wxevent handlers--------------------------------------------------------
    def on_evt_publish(self,event):
        """
        wxEvent handler to publish a message
        """
        MBClient.process_published(self, event.msg)

    def on_evt_send(self,event):
        """
        wxEvent handler to send a message
        """
        MBClient.process_msg(self, event.msg)
