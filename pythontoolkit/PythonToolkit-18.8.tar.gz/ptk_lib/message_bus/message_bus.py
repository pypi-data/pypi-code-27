"""
MessageBus system:

                                                    ______    
                                                   | Coms |   
                    ____________                   |thread|   
    MBLocalNode1 ___|            |___ MBRemoteNode.|......|...MBClient1
    MBLocalNode2 ___| MessageBus |___ MBRemoteNode.|......|...MBClient2
    MBLocalNode3 ___|____________|___ MBRemoteNode.|......|...MBClient3
                                                   |______|   


Nodes (either local nodes or remote nodes/clients) connect to the messages bus
and have a unique node name. This node name can be used to send messages 
directly between nodes (addressed messages) and the result of the message 
handler can be optionally returned to the sender. 

Alternatively nodes can publish messages via the message bus. Here the message 
is sent to the messagebus and and it will call the subscribers for the subject 
and any parent subjects, e.g. for 'subject.sub1.sub2' subscribers for 
'subject.sub1.sub2', 'subject.sub1' and 'subject' will be called it that order.

Client objects are forwarded the published message by the controlling 
MBRemoteNode and handle them locally.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

import threading

#Other messenger components
from mb_misc import AsyncResult, AddressError, WeakRefHandler
from mb_socket import MBThread
from mb_server import MBServer
import mb_protocol

#-------------------------------------------------------------------------------
# The message bus base class: use a subclass of this with the _do_delayed_send
# and _do_delayed_publish methods integrated into a mainloop.
#-------------------------------------------------------------------------------
class MessageBus():
    def __init__(self, name='MessageBus', timeout=5):
        """
        The message bus base class: use a subclass of this with the 
        _do_delayed_send and _do_delayed_publish methods integrated into a 
        mainloop.
        """
        self.name = name
        self.timeout = timeout

        #message counter 
        #   - used to generate unique message ids for retrieving replies
        self._count = 0
    
        #nodes
        self._lock = threading.Lock()
        self._nodes = {}      #{name:node} dictionary
        self._node_names = [] 
        #node name list used to preserve node order - nodes added first will 
        #process messages first!

        #Automatic node name assignment:
        #
        # node names ending with '.#' are assumed to be automatically incremented
        # numbering, ie. 'Node:#' gives, Node:0, Node:1 etc
        #
        # node names ending with '.*' are assumed to be requests for a node name
        # in a group. E.g. 'Node:*' is a request for a name in the 'Node' group
        # For these a registered python callable is used to provide a node name.
        # In this example, the following function could be registed for the
        # 'Node' group and would be called:
        #
        #   self.register_node_group('Node',get_node_number)
        #
        #   def get_node_number():
        #        name = 'Node.number'+str(node_count)
        #        node_count= node_count+1
        #        return name
        #
        # The connecting node will be assigned Node.number0, then None.number1 
        # and so on for following connections. 

        # These allow simplified code when multiple similar connections are 
        # required with the connecting ndoes not having to worry about their 
        # name being unique.
        #
        #dictionary of {name: callback} used to automatically assign node names
        self._auto_name_callbacks = {} 
        #dictionary of {name: count} use to automatically asign node numbers
        self._auto_name_n = {}

        #---socket communications-----------------------------------------------
        self.server = None     #server channel
        self._thread = None    #comms thread
        self._map = {}         #map dictionary for channels 
        self._shutdown = False  #shutdown flag used to shutdown quietly

        #---for publishing------------------------------------------------------
        
        #local handlers for published messagess
        self._sub_hndlrs = {} #dictionary of {subject:[handlers]}

    #---nodes-------------------------------------------------------------------
    def has_node(self, node_name):
        """
        Check if a node exists on the message bus.
        """
        return self._nodes.has_key(node_name)

    def register_node_group(self, node_group, callable):
        """
        Set a callable that generates a new node name it the node_group given
        when a node connects with a name 'node_group:*'.
        This should return a new, unique, name in the group. e.g. Node:A, Node:B
        etc.
        """
        self._auto_name_callbacks[node_group] = callable

    def register_node(self, node, node_name):
        """
        Add a node to the Messenger system - this is given a unique name which 
        can be used to send messages from point to point. The node itself should
        have a recieve(msg) method to handle messages sent to the node which may
        have different subjects.
        """
        with self._lock:

            #auto-name node - using group callback
            if node_name.endswith('.*'):
                log.debug('Registering node using autoname, group: '+node_name[:-2])
                group = node_name[:-2]
                callable = self._auto_name_callbacks.get(group, None)
                if callable is None:
                    #use autonumber
                    node_name = node_name[:-2]+'.#'
                else:
                    node_name = callable()

            #auto-name node - using name counter
            if node_name.endswith('.#'):
                start = node_name[:-2]
                log.debug('Registering node using autoname, counter: '+start)
                n = self._auto_name_n.get( start, 0)
                node_name = start+'.'+str(n)
                self._auto_name_n[ start ] = n+1

            #check if name is unique - if not raise an error
            if self._nodes.has_key(node_name):
                log.exception('Node name '+node_name+' already registered')
                raise ValueError('Node name '+node_name+' already registered')

            #store the node name
            node.name = node_name

            #store reference to the node
            self._nodes[node_name] = node
            self._node_names.append(node_name)

        log.info('Registered node : '+str(node_name))
        self.publish_msg( mb_protocol.SYS_NODE_CONNECT+'.'+node_name, (node_name,))
        return node_name

    def _remove_node(self, node_name, err=False):
        """
        This is called internally by closing nodes - use close_node
        Remove the node with the name given from the Messenger system and publish
        a SYS_NODE_CLOSED or SYS_NODE_ERR_CLOSED message.
        """
        with self._lock:
            node = self._nodes.pop(node_name,None)
            try:
                self._node_names.pop( self._node_names.index(node_name))
            except:
                pass

        if node is None:
            return

        if self._shutdown is True:
            return

        self.publish_msg( mb_protocol.SYS_NODE_DISCONNECT+'.'+node_name,
                                (node_name,err))
        log.info('Node removed: '+str(node_name)+' error= '+str(err))

    def close_node(self, node_name):
        """
        Send a message to a node requesting it closes.
        """
        log.info('Closing node ' + node_name)
        #send a system close message
        with self._lock:
            msgid = str(self.name)+':'+str(self._count)
            self._count+=1

        msgtype = mb_protocol.MSG_SYSTEM
        subject = mb_protocol.SYS_NODE_CLOSE
        msg = mb_protocol.Message( msgid, msgtype,from_node=self.name,
                       to_node=node_name, subject=subject, data=())
        #send via message bus
        self.process_msg(msg)

    def shutdown(self):
        """Close all nodes and shutdown the communications thread"""
        log.info('Shutting down message bus')
        self._shutdown = True

        #close all nodes - they remove themselves from the MessageBus and close 
        #sockets etc.
        for node in self._nodes.values():
            log.info('Closing node: '+node.name)
            try:
                node.disconnect()
            except:
                log.exception('Exception closing node: '+str(node))
                
        #stop server
        self.stop_server()

    #---socket server-----------------------------------------------------------
    def start_server(self,port=6668,allow_ext=False):
        """
        Start a thread to monitor for external clients.
            port        - port to listen on.
            allow_ext   - allow clients external to this computer. 
        """
        if self.server is not None:
            log.exception('Server already started')
            raise Exception('Server already started')

        #create a MBServer thread
        log.debug(  'Starting server '+str(port)+
                    ' allow external ='+str(allow_ext))
        

        #create a server socket listening for connections and start listening
        try:
            self.server = MBServer(self, port, allow_ext)
        except:
            self.server = None
            raise

        #make sure a comms thread is started
        if (self._thread is None) or (self._thread.is_alive is False):
            self._thread = MBThread(self._map)
            self._thread.start()
            
    def stop_server(self):
        """
        Stop the server monitoring for external clients
        """
        log.info('Stopping server')
        if self.server is None:
            raise Exception('No server thread running')

        self._thread.stop(join=True)
        log.info('Server stopped')
        self.server = None
        self._thread = None

    def has_server(self):
        """
        Returns True if server is active, False otherwise
        """
        if self.server is None:
            return False
        else:
            return True

    #---send addressed messages-------------------------------------------------
    def send_msg(self, to, subject, data=(), get_result=False):
        """
        Send a message directly on the MessageBus.
        to      -   Node to send message to.
        subject -   The message subject.
        data    -   A list or tuple data object.        
        get_result  -   True/False wait for and return the result.

        Returns - the result value if get_result is True, or None
        """
        #construct the message object
        with self._lock:
            msgid = str(self.name)+':'+str(self._count)
            self._count+=1

        if get_result is True:
            msgtype = mb_protocol.MSG_ADD_RESULT
        else:
            msgtype = mb_protocol.MSG_ADD_NO_RESULT

        msg = mb_protocol.Message( msgid, msgtype,from_node=self.name,
                       to_node=to, subject=subject, data=data)

        #result object allows the reply/result to be returned to the sending 
        #thread
        if get_result is True:
            res_obj = AsyncResult(msgid, self._timeout)
            msg.set_result = res_obj.set_result
            msg.get_result = res_obj.get_result

        #send the message via the MessageBus
        self.process_msg(msg)

        if get_result is False:
            return None

        #get the reply/result - this will block the sending thread until a result
        #is set using msg.set.result(res)
        try:
            res = msg.get_result()
        except:
            log.exception('Get result failed:')

        #check if an error
        if isinstance(res, Exception):
            raise res

        return res

    def process_msg(self, msg):
        """
        Send a message on the MessageBus.
        msg         -   the message object to send
        """
        #addressed message?
        if (msg.msgtype not in [mb_protocol.MSG_ADD_RESULT, 
                        mb_protocol.MSG_ADD_NO_RESULT, mb_protocol.MSG_SYSTEM]):
            raise Exception('Not an addressed message type')

        #check if this is the main thread or not.
        mainthread = isinstance(threading.current_thread(), threading._MainThread)
        if (mainthread is True):
            self._do_send(msg)
        else:
            self._do_delayed_send(msg)

    def _do_send(self, msg):
        """
        Send the message in the current thread - this is only used in the 
        main thread.
        """
        log.debug('Sending message to: '+msg.to_node+' subject: '+msg.subject)

        #get the node
        with self._lock:
            node = self._nodes.get(msg.to_node,None)

        if node is None:
            res = AddressError(msg.to_node)
            msg.set_result(res)
            return

        #pass the message object to the node
        try:
            node.process_msg(msg) 
        except:
            log.exception('Node recieve failed: '+str(msg.subject)+' to '+str(msg.to_node))
            raise

    def _do_delayed_send(self,msg):
        """
        Send the message in the main thread via an event.
        """
        pass

    #---Published messages------------------------------------------------------
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


    def publish_msg(self, subject, data):
        """
        Publish a message directly on the MessageBus
        """
        #construct the message object
        with self._lock:
            msgid = str(self.name)+':'+str(self._count)
            self._count+=1

        msg = mb_protocol.Message( msgid, msgtype=mb_protocol.MSG_PUBLISHED, 
                        from_node=self.name, to_node=None, 
                        subject=subject, data=data )
        self.process_published(msg)

    def process_published(self, msg):
        """
        Publish a message on the MessageBus
        msg         -   the mesage object to publish
        """
        #published message
        if (msg.msgtype!=mb_protocol.MSG_PUBLISHED):
            raise Exception('Not a published message type')
        #always publish via an event  
        self._do_delayed_publish(msg)      

    def _do_publish(self,msg):
        """
        Publish the message in the main thread - this is only used in the 
        main thread.
        """
        #get the subject
        log.debug('Publishing message; subject= '+msg.subject)

        #-----------------------------------------------------------------------
        # Handle local subscribers
        #-----------------------------------------------------------------------
        #get the subscribers for this message subjects
        subject = msg.subject
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

        #Finally pass message to each node (including the sending node) in turn 
        #for it to do extra tasks, e.g. forward to a client or log the message.
        #Most local nodes do nothing.

        #get the nodes into a new list in case new nodes area created when iterating.
        with self._lock:
            nodes = list(self._nodes.values()) 

        for node in nodes:
            try:
                node.process_published(msg)
            except:
                log.exception('Node process_published failed: '+node.name)

    def _do_delayed_publish(self, msg):
        """
        Publish the message in the main thread via an event.
        """
        pass


#-------------------------------------------------------------------------------
# PyMessageBus - simple MessageBus that stores sent messages sent from thread 
# and published messages internally. These are processed when a call is made to 
# process_waiting_messages() form the mainloop.
#-------------------------------------------------------------------------------
class PyMessageBus(MessageBus):
    def __init__(self, name='MessageBus', timeout=5):
        """
        Create a MessageBus instance - this should be done only once and the 
        instance stored where it can be used.
        """
        MessageBus.__init__(self, name, timeout)

        #store sent/published messages internally until process_waiting_messages
        #is called from a mainloop
        self._to_send = []
        self._to_publish = []

    #---overloaded methods to trigger an event----------------------------------
    def _do_delayed_send(self,msg):
        """
        Send the message in the main thread via an event.
        """
        with self._lock:
            self._to_send.append(msg)

    def _do_delayed_publish(self, msg):
        """
        Publish the message in the main thread via an event.
        """
        with self._lock:
            self._to_publish.append(msg)

    def process_waiting_messages(self):
        """
        Process message waiting to be sent or published - this should be called 
        in the application mainloop at regular intervals.
        """
        #clear addressed messages
        while len(self._to_send)!=0:
            try:
                with self._lock:
                    msg = self._to_send.pop(0)
                self._do_send(msg)
            except IndexError:
                pass

        #clear published messages
        while len(self._to_publish)!=0:
            try:
                with self._lock:
                    msg = self._to_publish.pop(0)
                self._do_send(msg)
            except IndexError:
                pass

