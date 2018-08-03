"""
MessageBus misc classes.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)
#-------------------------------------------------------------------------------

import weakref                  #weak references to handlers
from inspect import ismethod    #for weak references to methods
import threading

#---Message handler weak reference class----------------------------------------
class WeakRefHandler():
    """ Stores a weakref to a handler objects (including methods) """
    def __init__(self,obj):
        if callable(obj) is False:
            raise Exception('Message handlers should be callable')
        if ismethod(obj) is True:
            if obj.im_self is None:
                raise Exception('Unbound method passed as message handler')
            self._ismthd = True
            self._obj = weakref.ref(obj.im_self)#store a ref to the 'self' part
            self._fnc = obj.im_func #store a ref to the func part
        else:
            self._ismthd = False
            self._obj = weakref.ref(obj)

    def __call__(self,msg):
        """call the handler passing the msg as the argument"""
        if self.isdead():
            return None
        #if a method, need to do more complex
        if self._ismthd:
            s = self._obj()
            h = self._fnc
            return h(s,msg)
        #otherwise just call it
        h = self._obj()
        return h(msg)

    def isdead(self):
        return (self._obj is not None) and (self._obj() is None)
        
    def __eq__(self,obj):
        if ismethod(obj) is True:
           if (self._obj()==obj.im_self) and (self._fnc== obj.im_func):
              return True
           else :
              return False
        else:
           if self._obj() == obj:
              return True
           else:
              return False
        return False
    
    def __repr__(self):
        if self._ismthd:
            return 'Method: '+str(self._fnc)+ ' of object: '+str(self._obj)
        return str(self._obj)

#---Async result-------------------------------------------------------------
class AsyncResult():
    """
    An object representing a delayed result. 
    This allows a message to be processed in the main thread, and allow the 
    reply to be returned to the sending thread.
    """
    def __init__(self, msgid, timeout=30):
        """
        Create an AsyncResult object.
        """
        self._event = threading.Event()
        self._result = None
        self._msgid = msgid
        self._timeout = timeout

    def get_result(self):
        """Replacement for the msg object get_result callable"""
        try:
            self._event.wait(self._timeout)
        except:
            return TimeoutError()
        return self._result

    def set_result(self,result):
        """Replacement for the msg object set_result callable"""
        self._result = result
        self._event.set()


#-------------------------------------------------------------------------------

#---Error objects---------------------------------------------------------------
class AddressError(Exception):
    """
    A representation of an error idicating that the address was unknown, 
    used so that the exception is raised in the sending thread/process.
    """
    def __init__(self,to_node):
        self.to_node = to_node
        Exception.__init__(self,'Unknown node address: '+self.to_node)

class SubjectError(Exception):
    """
    An error object indicating that the message subject was not handled by the 
    recieving Node.
    """
    def __init__(self, to_node, subject):
        self.to_node = to_node
        self.subject = subject
        Exception.__init__(self, 'Unhandled subject:'+self.subject+
                            ' at node: '+self.to_node+' '+self.subject)

class HandlerError(Exception):
    """
    An error object indicating that the message handler at the recieving Node 
    failed.
    """
    def __init__(self, to_node, subject):
        self.to_node = to_node
        self.subject = subject
        Exception.__init__(self, 'Subject handler failed:'+self.subject+
                            ' at node: '+self.to_node+' '+self.subject)

class TimeoutError(Exception):
    """
    A representation of an error idicating that recieving the result timed out, 
    used so that the exception is raised in the sending thread/process.
    """
    def __init__(self, to_node):
        self.to_node = to_node
        Exception.__init__(self,'Unknown address: '+self.to_node)

