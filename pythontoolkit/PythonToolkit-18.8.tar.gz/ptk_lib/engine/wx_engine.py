"""
wx external engine:

uses the wx mainloop and wxevents to run user commands.

wxEngine    -   Base class / simple embedded engine.
PTK_wxEngine -   The class used for a standalone PTK wxEngine

"""
#---Logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

#-------------------------------------------------------------------------------
import wx
from engine import Engine

#---External part---------------------------------------------------------------
# Main thread is a wx.app mainloop waiting for commands or exit flag
from wx.lib.newevent import NewEvent
EvtEngineCode , EVT_ENGINE_CODE = NewEvent() #wx event to run user code
EvtEngineDisconnect , EVT_ENGINE_DISCONNECT = NewEvent() #wx event for engine disconnects

class wxEngine(Engine):
    engtype='Embedded.wx'
    def __init__(self, parent, englabel=None, userdict={},  timeout=10):
        """
        The PTK engine class for embedding in wxpython applications. 
        To use create an instance of this or a subclass. 
        It uses the parent object to post/bind event. 
        engine.disconnect() should also be called before the application exits.

        Evts to use:
        EVT_ENGINE_DISCONNECT -  sent went the PTK interface disconnects or the 
        user raises a system exit (e.g. via typing exit()).

        Methods/attributes you might want to overload:
        _get_welcome()      - Returns a string welcome message.
        self.eng_prompts    - these are the prompts used by the controlling 
                                console.
        """
        Engine.__init__(self, englabel, userdict, timeout)
        self.parent = parent
        #bind wx_User_Code event
        self.parent.Bind(EVT_ENGINE_CODE, self.OnEngineCode)

    #---overload base methods---------------------------------------------------
    def run_code(self,code):
        """
        Run some compiled code as the user.
        """ 
        evt = EvtEngineCode(code=code)
        wx.PostEvent(self.parent, evt)

    def on_disconnect(self):
        """
        The engine node disconnected from the message bus.
        This will post an EVT_ENGINE_DISCONNECT event.
        """
        Engine.on_disconnect(self)
        evt = EvtEngineDisconnect(err=False)
        wx.PostEvent(self.parent, evt)

    def on_err_disconnect(self):
        """
        The engine node disconnected from the message bus.
        This will post an EVT_ENGINE_DISCONNECT event.
        """
        Engine.on_err_disconnect(self)
        evt = EvtEngineDisconnect(err=True)
        wx.PostEvent(self.parent, evt)

    def get_welcome(self):
        """Return the engines welcome message"""
        welcome = Engine.get_welcome(self) + "\n\nRunning as an external engine process with a wx mainloop\n"
        return welcome

    #---wx code event handler---------------------------------------------------
    def OnEngineCode(self,event):
        #run code
        self._run_code(event.code) 


#-------------------------------------------------------------------------------
class PTK_wxEngine(wxEngine):
    engtype='PTK.wx'
    def __init__(self, englabel=None, userdict={}, timeout=10):
        """
        The wxEngine object used for a standalone PTK engine. 
        It creates its own wx.App object.
        """
        #clear sigint allows us to raise a keyboard interrupt in running code.
        self.app = wx.App(redirect=False, clearSigInt=False)
        self.app.SetAppName('wxEngine')

        self.app.Bind(EVT_ENGINE_DISCONNECT, self.OnEngineDisconnect)

        #create a dummy frame to stop wx mainloop from exiting
        self._dummyf = wx.Frame(None,-1,'Dummy')

        #disable exit from mainloop when no frames exist 
        # - this doesn't seem to work?
        self.app.SetExitOnFrameDelete(False) 

        wxEngine.__init__(self, self.app, englabel, userdict, timeout)

    #---Main interface----------------------------------------------------------
    def start_main_loop(self):
        """Wait for user commands to execute"""
        if self.connected is False:
            raise Exception('Not connected to MessageBus!')

        self.app.MainLoop()
        log.info('Mainloop ended')

    #---wx close event handler---------------------------------------------------
    def OnEngineDisconnect(self,event):
        self.stop_code(quiet=True)
        self.app.ExitMainLoop()
