"""
The tool class:
"""
import wx
from ptk_lib import VERSION

#---Tool (plugin) class---------------------------------------------------------
class Tool(object):
    """
    Tool base class
    """
    name = 'Tool'           #tool name
    descrip = ''            #tool description
    version = VERSION       #tool version
    author = 'T.Charrett'   #tool author
    requires = []           #list of tool names this tool requires
    core = False            #is a core tool
    icon = None             #the icon to display in the toolmanger

    def __init__(self):
        #store references to the application, toolmanager and messenger for 
        #conveience
        self.app = wx.GetApp()
        self.toolmgr = self.app.toolmgr
        self.msg_bus = self.app.msg_bus



