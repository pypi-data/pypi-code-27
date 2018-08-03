"""
MessageBus Node

These objects register with the MessageBus to send and recieve messages.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)

#---Imports---------------------------------------------------------------------
import threading

#Other messenger components
import mb_protocol
from mb_misc import AsyncResult, WeakRefHandler, AddressError, SubjectError, HandlerError

#-------------------------------------------------------------------------------
# Base message bus node object 
#   - just handles connection/disconnection and SYS_NODE_CLOSE message 
#   - use subclasses.
#-------------------------------------------------------------------------------
class MBNode(object):
    def __init__(self, name):
    
        self.connected = False
        self.name = name
        self.msgbus = None

    #---connection/disconnection------------------------------------------------
    def connect(self, msgbus):
        """
        Connect to a message bus
        """
        if self.connected is True:
            raise Exception('All ready connected to a message bus')

        self.msgbus = msgbus
        self.name = self.msgbus.register_node( self, self.name )
        self.connected = True

    def disconnect(self):
        """
        Disconnect from a message bus - if connected to one.
        """
        if self.connected is False:
            return False

        self.connected = False
        self.msgbus._remove_node(self.name, err=False)

    #---incomming messages------------------------------------------------------    
    def process_msg(self, msg):
        """
        Process a message addressed to this node.
        """
        #system message requesting the node closes
        if msg.subject == mb_protocol.SYS_NODE_CLOSE:
            self.disconnect()
            return

    def process_published(self, msg):
        """
        Process a published message - called after a message has been published
        for the node to perform extra tasks such as forwarding to a client or
        logging the message. Default is to do nothing.
        """
        pass        

#-------------------------------------------------------------------------------
# Local Node object - A node in the same process as the MessageBus with messaging
#   capablilities (send/recieve message to/from other node and publish messages)
#-------------------------------------------------------------------------------
class MBLocalNode(MBNode):
    def __init__(self, name):
        """
        A local MessageBus node which can be used to send, recieve and publish
        messages.
        """
        MBNode.__init__(self, name)

        #Lock used to make things thread safe
        self._lock = threading.Lock()   
     
        #message counter - used to generate unique message ids
        self._count = 0

        #message handlers for addressed messages
        self._msg_hndlrs = {}  #dictionary of {subject:handler}
        
    #---addressed messages------------------------------------------------------
    def send_msg(self, to, subject, data=(), get_result=False):
        """
        Send a message via the MessageBus.

        to      -   Node to send message to.
        subject -   The message subject.
        data    -   A list or tuple data object.
        get_result  -   True/False wait for and return the result.

        Returns - the result value if get_result is True, or None
        """
        if self.connected is False:
            raise Exception('Node not connected to a MessageBus!')

        #get unique message id.
        with self._lock:
            msgid = str(self.name)+':'+str(self._count)
            self._count+=1
        
        #set message type
        if get_result is True:
            msgtype = mb_protocol.MSG_ADD_RESULT
        else:
            msgtype = mb_protocol.MSG_ADD_NO_RESULT

        #construct the message object
        msg = mb_protocol.Message(  msgid,
                                    msgtype, 
                                    from_node=self.name,
                                    to_node=to, 
                                    subject=subject,
                                    data=data   )

        #result object allows the reply/result to be returned to the sending 
        #thread
        if get_result is True:
            res_obj = AsyncResult(msgid, self.msgbus.timeout)
            msg.set_result = res_obj.set_result
            msg.get_result = res_obj.get_result

        #send the message to the parent MessageBus
        self.msgbus.process_msg(msg)

        #Get a reply?
        if get_result is False:
            return None

        #get the reply/result - this will block the sending thread until a reply
        #is set using reply(res)
        res = msg.get_result()

        #check if an error
        if isinstance(res, Exception):
            raise res

        return res

    def set_handler(self, subject, handler):
        """
        Register a message handler for the addressed message subject given.
        """
        #get the lock
        with self._lock:
            #store handler into dictionary
            self._msg_hndlrs[subject]=WeakRefHandler(handler) 

    def remove_handler(self, subject):
        """
        Remove the message handler for the message subject.
        """
        #get the lock
        with self._lock:
            #store handler into dictionary
            self._msg_hndlrs.pop(subject,None) 

    def process_msg(self, msg):
        """
        Process a message addressed to this node.
        """
        #system message requesting the node closes
        if msg.subject == mb_protocol.SYS_NODE_CLOSE:
            self.disconnect()
            return

        #get handler
        with self._lock:
            handler = self._msg_hndlrs.get(msg.subject,None)

        if handler is not None:
            #check if the handler is dead
            if handler.isdead():
                log.info('dead handler'+str(handler))

                #remove it
                with self._lock:
                    self._msg_hndlrs.pop(msg.subject)

                #return an SubjectError
                res = SubjectError(msg.to_node, msg.subject)

            else:   
                #call it        
                try:
                    res = handler(msg)
                except:
                    log.exception('Handler failed: '+str(handler))
                    res=HandlerError(msg.to_node, msg.subject)
        else:
            log.info('No handler found for subject: '+str(msg.subject))
            #return an SubjectError
            res = SubjectError(msg.to_node, msg.subject)

        #return the result via the reply object/callable at msg.set_result
        msg.set_result(res)

    #---published messages------------------------------------------------------
    def publish_msg(self, subject, data=()):
        """
        Publish a message via the MessageBus.

        subject -   message subject
        data    -   tuple containing message data.
        """
        if self.connected is False:
            raise Exception('Node not connected to a MessageBus!')

        #get unique message id
        with self._lock:
            msgid = str(self.name)+':'+str(self._count)
            self._count+=1

        #construct the message object
        msg = mb_protocol.Message(  msgid, 
                                    msgtype=mb_protocol.MSG_PUBLISHED, 
                                    from_node=self.name,
                                    to_node='', 
                                    subject=subject,
                                    data=data )

        #publish the message via the parent MessageBus
        self.msgbus.process_published(msg)

    def subscribe(self, subject, handler):
        """
        Subscribe a message handler for the published message subject given.
        """
        if self.connected is False:
            raise Exception('Not connected to a message bus')

        return self.msgbus.subscribe(subject, handler)

    def unsubscribe(self, subject, handler):
        """
        Remove the message handler subscribed for the message type.
        """
        if self.connected is False:
            raise Exception('Not connected to a message bus')

        return self.msgbus.unsubscribe(subject, handler)

    
    
