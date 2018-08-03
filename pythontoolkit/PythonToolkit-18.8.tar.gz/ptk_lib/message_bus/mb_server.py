"""
MessageBus socket communications: Server side
---------------------------------------------

MBServer: Server object/thread to do asynchronous socket communications for the 
message bus


RemoteNode: MessageBus node object representing a remote client (created 
automatically for connecting clients)

See mb_client for client implementation.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

import socket
import threading
import time

from mb_node import MBNode
import mb_protocol
from mb_socket import ServerChannel, MsgChannel, HANDSHAKE

#-------------------------------------------------------------------------------
# Channel object to listening for an incomming connection
#-------------------------------------------------------------------------------
class MBServer(ServerChannel):
    def __init__(self, msgbus, port, allow_ext):
        """
        A connection object that listens for an incoming connections and spawns 
        MBRemoteNodes to manage them.
        """
        self.msgbus = msgbus
        ServerChannel.__init__(self, msgbus._map, port, allow_ext)
    
    def handle_accept(self):
    
        #accept the connection
        try:
            conn, client_address = self.socket.accept()
        except:
            log.exception('accept failed')
            return
           
        #make non blocking
        conn.setblocking(False)
        
        #create a new RemoteNode on the message bus.
        #this does the handshake and registers/returns the node name
        try:
            node = MBRemoteNode(self.msgbus, conn)
        except:
            #failed to handshake/register, close the socket
            log.exception('MBServer: handshake failed, closing connection')
            conn.close()

    def handle_close(self):
        """called when the socket is closed"""
        ServerChannel.handle_close(self)
    
        #remove from the message bus
        self.msgbus.server = None

#-------------------------------------------------------------------------------
# Channel object to manage the MBRemoteNode communications socket
#-------------------------------------------------------------------------------
class MBMsgChannel(MsgChannel):
    def __init__(self, node, socket):
        self.node = node
        self.msgbus = node.msgbus
        MsgChannel.__init__(self, node.name, self.msgbus._map, socket)

    def process_msg(self, msg):
        """
        Process an incomming addressed message
        """
        log.debug('addressed message recieved: '+msg.subject)
        self.msgbus.process_msg(msg)

    def process_published(self,msg):
        """
        Process an incomming published message
        """
        log.debug('published message recieved: '+msg.subject)
        self.msgbus.process_published(msg)

    def handle_disconnect(self):
        """
        Called when the socket closes normally
        """
        self.node.disconnect(error=False)

    def handle_err_disconnect(self):
        """
        Called when the socket closes unexpectedly
        """
        self.node.disconnect(error=True)

#-------------------------------------------------------------------------------
# RemoteNode - An MBNode that represents a remote connection (via a socket 
# connection).
#-------------------------------------------------------------------------------
class MBRemoteNode(MBNode):
    def __init__(self, msgbus, socket):
        """
        A Node which represents a remote connection. It sends/published message
        on the message bus on behalf of its client and forwards message to the
        client.

        thread   - the MBThread to monitor this socket 
        conn     - a connected Socket object
        """
        MBNode.__init__(self, None)

        #MBConnection object will be here once the socket has been handshaken
        self.channel = None

        #Lock used to make things thread safe
        self.lock = threading.Lock()   

        #do handshake and node name assingment.
        self.connect(msgbus, socket)

    #---------------------------------------------------------------------------
    def connect(self, msgbus, conn):
        """
        Handshake the socket connection, conn, and connect to a msgbus using the
        requested node name.
        """
        if self.connected is True:
            raise Exception('All ready connected to a message bus')

        ## Do the handshake on the connected socket
        #send the handshake message
        log.info('Sending handshake message...')
        conn.sendall(HANDSHAKE)
        conn.setblocking(True)

        #read the reply should be the same
        log.info('Waiting for handshake message...')
        buffer = ''
        while len(buffer)<len(HANDSHAKE):
            try:
                buffer = buffer + conn.recv(1)
            except:
                log.exception('Timeout waiting for handshake message')
                conn.close()
                raise Exception('Timeout waiting for handshake message')

        #check protocol
        log.info('Checking protocol...'+buffer)
        if buffer !=HANDSHAKE:
            conn.close()
            log.exception('Handshake message was not received')
            raise Exception('Handshake message was not received')

        log.info('Handshake OK.')

        ##Do second stage handshake, setting node name
        #read requested node name
        name = ''
        try:
            while name.endswith('\n') is False:
                name = name + conn.recv(1)
        except:
            conn.close()
            raise Exception('Timeout waiting for node name')

        try:
            name = name.rstrip('\n')
        except:
            log.exception('Error when processing node name')
            name = 'Client.*'
        log.info('Client requested node name: '+str(name))

        ## 3rd stage is to register the name and send the assigned name in case 
        ## it is different than that requested, i.e. using autoname/number
        try:
            msgbus.register_node( self, name )
            self.connected = True
        except:
            conn.close()
            raise Exception('Connection requested a node name already in use: '+
                            str(name))

        #send the assigned name
        log.info('Client registered as: '+str(self.name))
        conn.sendall(self.name+'\n')

        #make non blocking
        conn.setblocking(False)

        #set internal attributes
        self.msgbus = msgbus

        #create the MBMsgChannel object
        self.channel = MBMsgChannel(self, conn)
        log.info('Client connected')

    def disconnect(self, error=False):
        """
        Disconnect this node from the message bus.
        """
        #not connected to a msgbus
        if self.connected is False:
            return False
            
        #set internals flag
        self.connected = False
        
        #remove the node from the message bus
        self.msgbus._remove_node(self.name, error)

        #close the connection if open
        if self.channel.connected:
            self.channel.close()

        #remove the dead channel object
        self.channel = None

    #---------------------------------------------------------------------------
    # Node methods    
    #---------------------------------------------------------------------------
    def process_msg(self, msg):
        """
        Process a message addressed to this node - forwards it to the client.
        """
        if (self.channel is None) or (self.channel.connected is False):
            pass
        else:
            self.channel.forward_msg(msg)

    def process_published(self, msg):
        """
        rocess a published message - called after a message has been published
        for the node to perform extra tasks - forward it to the client - but 
        only if it did not come from the client.
        """
        if (self.channel is None) or (self.channel.connected is False):
              pass
        else:
            #only forward back to client if it didn't come from the client!
            fromnode = msg.get_from()
            if fromnode!=self.name:
                self.channel.forward_msg(msg)
