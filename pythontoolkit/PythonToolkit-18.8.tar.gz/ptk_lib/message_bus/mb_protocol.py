"""
This module defines the Messenger msgtypes for use with the protocol socket 
communications module.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)


#---Message types---------------------------------------------------------------
#a Message that was published:
MSG_PUBLISHED    = 'MSG_PUBLISHED'

#a Message that was sent to a registered address, result returned
MSG_ADD_RESULT  = 'MSG_ADD_RESULT'

#a Message that was sent to a registered address, no result returned
MSG_ADD_NO_RESULT  = 'MSG_ADD_NO_RESULT'  

#a Message object containing a system command/notification for external connections
MSG_SYSTEM      = 'MSG_SYSTEM'

#---special message subjects----------------------------------------------------
#request to close the connection to the message bus
SYS_NODE_CLOSE  = 'Sys.Node.Close'

#These are published by the message bus when nodes connects or disconnects with
#the node name appended to the subject. Allowing subscribers to keep track of
#connected nodes. data=(node_name, err=True/False)
SYS_NODE_CONNECT        = 'Sys.Node.Connect'
SYS_NODE_DISCONNECT     = 'Sys.Node.Disconnect'

#special addressed message subjects used for socket client managment
SYS_SOCKET_RESULT = 'Sys.Socket.Result'    #a result to a previous message.
SYS_SOCKET_CLOSING = 'Sys.Socket.Closing'  #socket connection is closing.

#---Message object--------------------------------------------------------------
class Message(object):
    def __init__(self,  msgid, msgtype=MSG_PUBLISHED,
                        from_node='', to_node='',
                        subject='', data=()):
        """
        Create a new message object:
            msgid       - a unique identifier.
            msgtype     - the message type - PUBLISHED/ADDRESSED
            from_node   - the sender node name
            to_node     - the destination node name (addressed message only)
            subject     - the message subject
            data        - the message data
        """
        self.msgid  = msgid                 # unique msg id
        self.msgtype= msgtype               # the message type
        self.from_node = from_node          # sender node name
        self.to_node = to_node              # destination node name
        self.subject = subject              # message subject
        # message data
        if type(data) not in [tuple,list]:
            raise Exception('msg data should be a tuple or list!')
        self.data = data             
        
    def get_msgid(self):
        """ Return the unique msgid """
        return self.msgid

    def get_msgtype(self):
        """ Return the message type """
        return self.msgtype

    def get_to(self):
        """ Return the destination node name (addressed messages) """
        return self.to_node

    def get_from(self):
        """ Return the sender node name (published messages) """
        return self.from_node

    def get_subject(self):
        """ Return the message subject"""
        return self.subject

    def get_data(self): 
        """ Return the message data tuple """
        return self.data

    def set_result(self, result):
        """ Callable to set the message result - this is replaced if a result is required"""
        pass

    def get_result(self):
        """ Callable to get the message result - this is replaced if a result is required"""
        return None
    
    def to_tuple(self):
        """
        Return msg as a tuple (for pickling etc)
        """
        t = (self.msgid, self.msgtype, 
                self.from_node, self.to_node, self.subject,) + self.data
        return t
