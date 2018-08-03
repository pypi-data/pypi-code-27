"""
Tools plugin system.

The ToolManager object handles the loading of plugins.
Plugins are defined by subclassing Tool instances.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.WARNING)

#---Imports---------------------------------------------------------------------
import os
import sys   
import pickle #used to store loaded plugins

import wx
from tool import Tool

#---ToolManager class-----------------------------------------------------------
class ToolManager():
    def __init__(self,tool_path):
        """
        Create a ToolManager, where tools are stored in tool_path
        """
        #dictionary of loaded tools {toolname: tool instance}
        self._loaded_tools  = {}
        #dictionary of unloaded tools 
        self._unloaded_tools = {}
        #directory containng tools
        self.tool_path = tool_path
        self.import_tools()
        log.info('Toolmanager started')

    #---Interface methods-------------------------------------------------------
    def import_tools(self):
        """
        Imports python packages containing the tools from the tooldir specified
        - this needs to be done before a tool can be loaded using LoadTools
        """
        log.debug('Importing tools from '+ str(self.tool_path))
        #get a list of the files in the toolpath
        if os.path.exists(self.tool_path) is False:
           return
        files = os.listdir(self.tool_path)

        #add path to the sys.path
        sys.path.insert(0, self.tool_path)
        #try to import each module in names
        for name in files:
            module,ext = os.path.splitext(name)
            if (ext in ['.py','.pyc','.pyd','']) and (module.startswith('.') is False):
                try:
                    __import__(module, None, None, [])
                except:
                    log.exception('Tool import failed: '+module)

        #remove from sys.path
        sys.path.pop(0)

    def start_tools(self,names):
        """
        Start the tools specified by the list of names given. Tool classes need
        to have been imported (using import_tools) before they can be started
        """
        log.debug('Starting tools: '+str(names))
        if type(names)!=list:
            log.error('names should be a list!')
            return

        #try to load each tools
        for name in names:
            self.start_tool(name)     

    def start_tool(self,name):
        """
        Start the tool specified by name
        """
        #check if tool is already loaded
        if self.is_loaded(name) is True:
            return

        #check it was not previously loaded
        if self._unloaded_tools.has_key(name):
            tool = self._unloaded_tools.pop(name)
            self._loaded_tools[name] = tool
            return
        
        #check tool is available
        tools = self.find_available_tools()
        if tools.has_key(name):
            tool = tools[name]
        else:
            log.error('start failed - no tool with name: '+str(name))
            return

        #check tool requirements
        for x in tool.requires:
            if self.is_loaded(x) is False:
                log.error('start tool failed - tool '+name+' requires: '+x)
                wx.MessageBox('start tool failed - tool '+name+' requires: '+x,'tool start')
                return

        #create an instance of the tool
        try:
            self._loaded_tools[name]=tool()
        except:
            log.exception('start failed when creating tool instance: '+str(name))
            wx.MessageBox('start failed when creating tool instance: '+str(name),'tool start')

    
    def stop_tools(self,names):
        """
        Stop the tools given by names - this moves the tool instance to an 
        interim storage dictionary in case it is re-started. The tool will be 
        fully disabled after restarting the program.
        """
        log.debug('Stop tools '+str(names))
        if type(names)!=list:
            log.error('Stop tools, names should be a list!')
            return
        for name in names:
            self.stop_tool(name)

    def stop_tool(self,name):
        if self.is_loaded(name) is True:
            log.info('Stopping '+str(name))
            tool= self._loaded_tools.pop(name)
            self._unloaded_tools[name]=tool        

    def save_settings(self):
        """
        Call to save ToolManager preferences (tools to load at startup)
        """
        log.debug('In SaveToolSettings')

        #save the loaded plugins
        cfg = wx.GetApp().GetConfig()
        cfg.SetPath("app//")

        #only save non-core tools
        usertools = []
        for k in self._loaded_tools:
            tool = self._loaded_tools[k]
            if tool.core is False:
                usertools.append(k)
        log.debug('In save_settings'+str(usertools))

        cfg.Write('Tools',pickle.dumps(usertools))
        cfg.Flush()
        log.info('Saved activated user tools')

    def load_settings(self):
        """
        Call to load ToolManager preferences (and load previously enabled tools)
        """
        log.debug('In LoadToolManagerSettings')

        #loaded the previously loaded plugins
        cfg = wx.GetApp().GetConfig()
        cfg.SetPath("app//")

        dump = cfg.Read('Tools',"")
        if dump =='':
            names = []
        else:
            names = pickle.loads(str(dump))
        self.start_tools(names)


    #---Utility methods---------------------------------------------------------
    def is_loaded(self,name):
        """
        Checks if a tool is loaded, returns True/False
        """
        ans = self._loaded_tools.has_key(name)
        return ans

    def is_available(self,name):
        """
        Checks if a tool is imported, returns True/False
        """
        tools = self.find_available_tools()
        if tools.has_key(name) is True:
            return True
        else:   
            return False

    def find_available_tools(self):
        """
        Returns a dictionary of available tools 
        {name string:tool classes}
        """
        dict ={}
        tools = Tool.__subclasses__()
        for x in tools:
            dict[x.name]=x
        return  dict

    def get_tool(self,name):
        """
        Returns the singleton instance of a loaded tool, or none if not loaded
        """
        if self._loaded_tools.has_key(name):
            tool = self._loaded_tools[name]
        else:
            raise Exception('No tool with name: '+name)
        return tool

    def get_loaded_tools(self):
        """
        Returns a list of the loaded tools
        """
        names = self._loaded_tools.keys()
        return names

    def shutdown(self):
        """
        Shutdown the toolmanager service
        """
        log.info('Shutting down ToolManager')
        self.save_settings()
