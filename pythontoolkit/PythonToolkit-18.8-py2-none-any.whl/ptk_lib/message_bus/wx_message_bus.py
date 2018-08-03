#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

import threading

#wx imports
import wx                       
import wx.lib.newevent

from message_bus import MessageBus

#-------------------------------------------------------------------------------

#publish event
EvtMsg_Publish, EVT_MSG_PUBLISH = wx.lib.newevent.NewEvent()

#Send message, the reply is stored internally for the waiting thread to collect
EvtMsg_Send , EVT_MSG_SEND  = wx.lib.newevent.NewEvent() 

class wxMessageBus(MessageBus):
    def __init__(self, name='MessageBus', timeout=5):
        """
        Create a wxMessageBus instance - this should be done only once and the 
        instance stored where it can be used.
        """
        MessageBus.__init__(self, name, timeout)

        #create a wx event handler to catch messenger events
        self.evt_hndlr = wx.EvtHandler()
        self.evt_hndlr.Bind(EVT_MSG_PUBLISH, self.on_publish)
        self.evt_hndlr.Bind(EVT_MSG_SEND,  self.on_send)

    #---overload these methods to trigger an event------------------------------
    def _do_delayed_send(self,msg):
        """
        Send the message in the main thread via an event.
        """
        evt = EvtMsg_Send(msg=msg)
        #post the event
        wx.PostEvent(self.evt_hndlr, evt)

    def _do_delayed_publish(self, msg):
        """
        Publish the message in the main thread via an event.
        """
        #create the event
        evt = EvtMsg_Publish(msg=msg)
        #post the event
        wx.PostEvent(self.evt_hndlr, evt)

    #---wx event handlers-------------------------------------------------------
    def on_publish(self,event):
        """
        wxEvent handler to publish a message
        """
        self._do_publish(event.msg)

    def on_send(self,event):
        """
        wxEvent handler to send a message
        """
        self._do_send(event.msg)