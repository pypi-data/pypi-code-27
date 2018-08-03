"""
MessageBus socket communications: Client side
---------------------------------------------

MBClient: MessageBus client object that can connect to a message bus via a 
socket and send/recieve addrssed and published messages.

See mb_server for server implementation.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

import socket
import time
import threading

from mb_socket import MBThread, MsgChannel
from mb_misc import SubjectError, HandlerError, WeakRefHandler
import mb_protocol

#-------------------------------------------------------------------------------
# Channel object to manage the MBClient communications socket
#-------------------------------------------------------------------------------
class ClientMsgChannel(MsgChannel):
    def __init__(self, client, name='Client.#', map={}, timeout=10):
        """
        A simple message bus client asyncore channel object.
        
        client - the client parent object to call with messages and close events
        name - a unique node name or autoname.
        map  - map dictionary of {socket: objects} to be monitored by the thread.
        """
        self.client = client
        MsgChannel.__init__(self, name, map, None, timeout)

    #---------------------------------------------------------------------------
    def process_msg(self, msg):
        """
        Process an incomming addressed message
        """
        log.debug('addressed message recieved: '+msg.subject)
        self.client.process_msg(msg)

    def process_published(self,msg):
        """
        Process an incomming published message
        """
        log.debug('published message recieved: '+msg.subject)
        self.client.process_published(msg)

    def handle_disconnect(self):
        """
        Called when the socket closes normally
        """
        log.info('client disconnected normally')
        self.client.on_disconnect()

    def handle_err_disconnect(self):
        """
        Called when the socket closes unexpectedly
        """
        log.info('client disconnected unexpectedly')
        self.client.on_err_disconnect()

#-------------------------------------------------------------------------------
# Socket client for MessageBus
#-------------------------------------------------------------------------------
class MBClient(object):
    """
    Socket client for MessageBus.
    """
    def __init__(self, name='Client.#', timeout=10):

        self._name = name
        
        #channel map dictionary will only ever have a listener or msg channel
        self._map   =   {}
        
        #timeout in seconds
        self.timeout = timeout

        #MBchannel object will be here
        self._channel = None
    
        #Comms thread running select call - set on connection
        self._thread = None

        #Lock used to make things thread safe
        self._lock = threading.Lock()   

        #message handlers for addressed messages
        self._msg_hndlrs = {}  #dictionary of {subject:handler}
        
        #handlers for published messagess
        self._sub_hndlrs = {} #dictionary of {subject:[handlers]}

    def __del__(self):
        self.shutdown()
        
    #---------------------------------------------------------------------------
    def connect(self, host, port):
        """
        Connect to a listening MessageBus at the address=(host,port).
        """
        if self.connected:
            raise Exception('Already connected')

        if self.listening is True:
            raise Exception('Already listening for a connection')

        self._channel = ClientMsgChannel(self, self._name, self._map, self.timeout)
        self._channel.connect(host,port)

        #create a comms thread if needed
        if (self._thread is None) or (self._thread.is_alive() is False):
            self._thread = MBThread(self._map)
        self._thread.start()

    def listen(self, port,  allow_ext=False):
        """Allow the master MessageBus to connect to us"""
        if self.connected is True:
            raise Exception('Already connected')

        if  self.listening is True:
            raise Exception('Already listening')

        #create a comms thread if needed
        if (self._thread is None) or (self._thread.is_alive() is False):
            self._thread = MBThread(self._map)
        
        #start listening
        self._channel = ClientMsgChannel(self, self.name, self._map, self.timeout)
        self._channel.listen(port, allow_ext)
        
        #start the thread
        self._thread.start()

    def disconnect(self):
        """
        Disconnect from the message bus or stop listening for connections
        """
        log.debug('in client disconnect')
        if self.listening or self.connected:
            self._channel.close()
        #on_disconnect called by msgchannel

    def on_disconnect(self):
        """
        Called when the socket channel disconnects from the message bus normally
        i.e. when requested to or when notified that the channel is closing.
        """
        #reset internals    
        self._channel = None
    
    def on_err_disconnect(self):
        """
        Called when the socket channel disconnects from the message bus 
        unexpectedly
        """
        #reset internals    
        self._channel = None

    def shutdown(self):
        """
        Ensure all channels are closed properly and the the thread is stopped
        """
        if (self._thread is not None) and (self._thread.is_alive):
            self._thread.stop()
    
    #get name from the msg channel or return the default
    @property
    def name(self):
        if self._channel is None:
            return self._name
        else:
            return self._channel.name

    @property
    def connected(self):
        if self._channel is None:
            return False
        else:
            return self._channel.connected

    @property
    def listening(self):
        if self._channel is None:
            return False
        else:
            return self._channel.accepting

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
            raise Exception('Not connected to a MessageBus!')
        return self._channel.send_msg( to, subject, data, get_result)

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
        Process a message addressed to this client.
        """
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
            raise Exception('Not connected to a MessageBus!')

        self._channel.publish_msg(subject, data)

    def subscribe(self, subject, handler):
        """
        Subscribe a message handler for the published message subject given.
        """
        #get the lock
        with self._lock:
            #get current list of handlers
            hlist = self._sub_hndlrs.get(subject,[])

            #add a weakref to the handler
            hlist.append(WeakRefHandler(handler)) 

            #store back into dictionary
            self._sub_hndlrs[subject]=hlist 

    def unsubscribe(self, subject, handler):
        """
        Remove the message handler subscribed for the message type.
        """
        with self._lock:
            hlist = self._sub_hndlrs.get(subject,[])

            #remove the handler
            for n in range(0,len(hlist)):
                h = hlist[n]
                if h == handler:
                    n = hlist.index(h)
                    hlist.pop(n)

            #store back into dict
            self._sub_hndlrs[subject] = hlist

    def process_published(self, msg):
        """
        Handles incoming published messages.
        """
        subject = msg.subject
        log.debug('publishing incomming message: '+msg.subject)
        while True:
            
            #get subscribers
            with self._lock:
                hlist = self._sub_hndlrs.get(subject,[])
        
            #call all handlers and check for dead ones
            new_hlist=[]
            for handler in hlist:
                #check if the handler is dead
                if handler.isdead():
                    pass
                else: 
                    new_hlist.append(handler)
                    try:
                        handler(msg)
                    except:
                        log.exception('Handler failed: '+str(handler))

            #store checked handler list back
            with self._lock:
                self._sub_hndlrs[subject]=new_hlist

            #remove last part of subject and recheck for subscribers
            try:
                subject, dropped = subject.rsplit('.',1)
            except ValueError:
                break


#-------------------------------------------------------------------------------
