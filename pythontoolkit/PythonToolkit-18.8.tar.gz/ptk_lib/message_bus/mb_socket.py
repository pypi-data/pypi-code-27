"""
MessageBus socket communications base components:

MsgChannel      -   Asyncore channel base object for sending message objects 
                    over a socket
ServerChannel   -   Asyncore channel base object for listening for connections 
                    or servers.
MBThread        -   Comms thread class.

SocketResult    -   Object used to ensure asyncrhonous return of results.
"""
#---logging---------------------------------------------------------------------
import logging
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

#-------------------------------------------------------------------------------
import asynchat
import asyncore
import socket
import threading
import time
from collections import deque
import StringIO
import cPickle as pickle

import mb_protocol

from mb_misc import TimeoutError, SubjectError, HandlerError, WeakRefHandler, AsyncResult

#---Globals---------------------------------------------------------------------
HANDSHAKE   = '<<MB_PROTOCOL_V2>>'   #protocol handshake string

#-------------------------------------------------------------------------------
# A channel object that can send/recieve messagebus message objects
#-------------------------------------------------------------------------------
class MsgChannel(asyncore.dispatcher):
    def __init__(self, name, map, sock=None, timeout=10):
        asyncore.dispatcher.__init__(self, sock, map)

        #client/node name to use when sending/connecting
        self.name = name

        #timeout for handshake/message results
        self.timeout = timeout

        #Use to make things thread safe
        self._lock = threading.Lock()   

        #message counter - used to generate unique message ids
        self._count = 0

        #replies dictionary {msgid:reply_obj}
        self._replies={}
        
        #store incoming data until complete
        self._chunkSize = 1024 * 128
        self._buffer = StringIO.StringIO()

        #flag used to indicate socket is closing.
        self._closing = False
        
        #outgoing buffer/queue
        self._sendq = deque()

        #message counter - used to generate unique message ids
        self._count = 0

    #---------------------------------------------------------------------------
    def connect(self, host, port):
        """
        Connect to a listening MessageBus at the address=(host,port).
        """
        if self.connected:
            raise Exception('Already connected')

        if self.accepting is True:
            raise Exception('Already listening for a connection')

        if self.socket is None:
            #create the socket
            self.create_socket (socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)

        #try to connect
        address= (host, int(port))
        log.info('connecting on: '+str(address)+'...')
        nmax=10
        for n in range(0,nmax+1):
            log.info('try'+str(n))
            try:
                self.socket.connect(address)
                break
            except:
                if n==nmax:
                    log.exception('Exception when trying to connect')
                    raise Exception('Could not connect!')
                #sleep for a bit before trying again
                time.sleep(1)
        self.handle_connect()

    def listen(self, port,  allow_ext=False):
        """Allow the master MessageBus to connect to us"""
        if self.connected is True:
            raise Exception('Already connected')

        if  self.accepting is True:
            raise Exception('Already listening')

        #create the socket and listen for connections
        self.create_socket (socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()

        if allow_ext is True:
            host = socket.gethostname()
        else:
            host = 'localhost'
        address = (host,port)
        self.bind(address)

        #start listening for connections
        self.listen(1)
    
    def _client_handshake(self, conn):
        """
        Do the client handshake on a connected socket
        """
        #send the handshake message
        log.info('Sending client handshake message...')
        conn.setblocking(True)
        conn.sendall(HANDSHAKE)

        #read the reply should be the same
        log.info('Waiting for server handshake message...')
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

        #send node name request
        log.info('Requesting node name '+str(self.name))
        conn.sendall(self.name+'\n')
        
        #read assgined name
        name=''    
        tic= time.time()
        while name.endswith('\n') is False:
            name = name + conn.recv(1)
            if (time.time()-tic) > 10:
                log.exception('Timeout waiting for node name')
                conn.close()
                raise Exception('Timeout waiting for node name')
        assigned_name = name.rstrip('\n')
        log.info('Assigned name: '+str(assigned_name) )
        return assigned_name

    #---asyncore methods--------------------------------------------------------
    def readable (self):
        return True

    def writable (self):
        return (self._sendq and self.connected)

    def handle_read (self):
        try:
            data = self.recv(self._chunkSize)
        except socket.error, why:
            self.handle_error()
            return
            log.debug('read '+str(len(data)))
        self._buffer.seek(0,2) # seek to end
        self._buffer.write(data)

        #check for messages
        while True:
            self._buffer.seek(0,0) # seek to beginning

            #read pickle object
            try:
                #try to unpickle data tuple
                data = pickle.load(self._buffer)
                
                #convert to message object
                try:
                    msg = mb_protocol.Message(msgid=data[0], msgtype=data[1], 
                                        from_node=data[2], to_node=data[3], 
                                        subject=data[4], data=data[5:])
                    #A system message
                    if (msg.msgtype == mb_protocol.MSG_SYSTEM):
                        self.process_sys_msg(msg)

                    #Addressed messsage to this node requiring a result returned.
                    elif (msg.msgtype == mb_protocol.MSG_ADD_RESULT):
                        #return the result via SocketResult
                        res_obj = SocketResult( self, msg.msgid) 
                        msg.set_result = res_obj.set_result
                        msg.get_result = res_obj.get_result
                        self.process_msg(msg)

                    #address message no reply needed
                    elif msg.msgtype == mb_protocol.MSG_ADD_NO_RESULT:
                        self.process_msg(msg)

                    #a published message
                    elif (msg.msgtype == mb_protocol.MSG_PUBLISHED):
                        self.process_published(msg)
                        
                    #log.debug('Message recieved: '+str(msg.msgtype)+' : '+str(msg.subject))
                except:
                    log.error('Invalid data recieved from unpickle: '+str(data))
                
                #remove unpickled data from buffer
                pos = self._buffer.tell()
                self._buffer.buf = self._buffer.buf[pos:]

            except EOFError:
                break
            except:
                raise
                #other unpickle error
                #try dropping characters until the stream is recovered
                char = self._buffer.buf[0]
                self._buffer.buf = self._buffer.buf[1:]
                log.warning('Unpickling error: dropping chars until recovered/EOF'+str(char))
            
    def handle_write (self):
        self.initiate_send()

    def handle_close(self):
        asyncore.dispatcher.close(self)

        #clear any messages waiting for replies
        for sent_msg in  self._replies.values():
            #call the set_result method object to return a TimeoutError
            sent_msg.set_result(TimeoutError(sent_msg.to_node))

        #call the on_close/on_err_close subclass methods
        if (self._closing is False):
            log.warning('channel closed unexpectedly [handle_close]!')
            self.handle_err_disconnect()
        else:
            log.debug('channel closed [handle_close]')
            self.handle_disconnect()

    def handle_connect(self):
        #do handshake
        try:
            self.name = self._client_handshake(self.socket)
            self.connected = True
        except:
            #failed to handshake/register, close the connection
            log.error('Handshake failed, closing connection')
            self.close()

    def handle_accept(self):
        try:
            conn, addr - self.accept()
            #do connection handshake 
            self.name = self._client_handshake(conn)

            #close the old listening socket
            if self.socket is not None:
                self.socket.close()

            #set this connection as the socket
            self.connected = True
            self.listening = False
            self.set_socket(conn)

        except:
            #failed to handshake/register, close the connection
            log.error('Handshake failed, closing connection')
            conn.close()
            return

    def handle_expt(self):
        #
        #Avoid connecting errors on windows when nothing is listening on the port
        #that we are trying to connect to.
        pass

    def handle_error(self):
        asyncore.dispatcher.handle_error(self)

    def handle_write(self):
        self.initiate_send()

    #---new handlers------------------------------------------------------------
    def handle_disconnect(self):
        """
        Called when the socket closes normally
        """
        pass

    def handle_err_disconnect(self):
        """
        Called when the socket closes unexpectedly
        """
        pass

    #---------------------------------------------------------------------------
    def initiate_send(self):
        """Send all data currently in the send queue"""
        #log.debug('init send')
        with self._lock:
            while self._sendq and self.connected:
                data = self._sendq[0]
                
                # send the data
                try:
                    num_sent = self.send(data)
                except socket.error:
                    self.handle_error()
                    return
                
                #check how much was sent and store anything remaining back in
                if (num_sent < len(data)):
                    self._sendq[0] = data[num_sent:]
                else:
                    del self._sendq[0]
                return

    def close(self):
        """ Close the channel after sending a SYS_SOCKET_CLOSING message"""
        #already closing/closed
        if (self._closing is False):
            #set flags
            self._closing = True
            #send a system close message
            msg = mb_protocol.Message( 'SYS', msgtype=mb_protocol.MSG_SYSTEM,
                        from_node=None, to_node=None,
                        subject=mb_protocol.SYS_SOCKET_CLOSING, data=())
            self.forward_msg(msg)
            time.sleep(0.1) #sleep to allow message to be sent
            
        #close socket
        asyncore.dispatcher.close(self)
        
        #clear any messages waiting for replies
        for sent_msg in  self._replies.values():
            #call the set_result method object to return a TimeoutError
            sent_msg.set_result(TimeoutError(sent_msg.to_node))

        self.handle_disconnect()

    def set_socket(self, sock, map=None):
        #set socket options to keep things zippy...
        sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY,1)
        asyncore.dispatcher.set_socket(self, sock, map)

    #---------------------------------------------------------------------------
    def send_msg(self, to, subject, data=(), get_result=False):
        """
        Send a new message over the socket

        to      -   Node to send message to.
        subject -   The message subject.
        data    -   A list or tuple data object.
        get_result  -   True/False wait for and return the result.

        Returns - the result value if get_result is True, or None
        """
        if self.connected is False:
            raise Exception('Not connected!')

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
            res_obj = AsyncResult(msgid, self.timeout)
            msg.set_result = res_obj.set_result
            msg.get_result = res_obj.get_result

        #send the message to the parent MessageBus
        #log.debug('sending message: '+msg.to_node + ' , '+msg.subject)
        self.forward_msg(msg)

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

    def publish_msg(self, subject, data=()):
        """
        Publish a message via the MessageBus.

        subject -   message subject
        data    -   tuple containing message data.
        """
        if self.connected is False:
            raise Exception('Not connected!')

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
        self.forward_msg(msg)
        
    def forward_msg(self, msg):
        """
        Forward a message over the socket connection
        """
        #convert message object to data tuple for pickling
        data = msg.to_tuple()
        try:
            s = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        except:
            raise Exception('Message data contains unpicklible data! '+msg.msgtype+' '+str(data))
        
        #need to wait for the result?
        if msg.msgtype == mb_protocol.MSG_ADD_RESULT:
            #store msg internally until reply is recieved
            self._replies[msg.msgid] = msg

        #Split into chunks and append to send queue
        if len(s) > self._chunkSize:
            #split the data into chunks
            for i in xrange(0, len(s), self._chunkSize):
                self._sendq.append(s[i:i+self._chunkSize])
        else:
            #less than 4095 just add
            self._sendq.append(s)

        #do the sending here and straight away to keep everything snappy
        self.initiate_send()

    def send_result( self, msgid, result):
        """
        Send a result to an addressed message - this is called by the 
        SocketResult object when it is called via the msg.set_result method.
        """
        #construct the message object
        msg = mb_protocol.Message( 'REPLY TO:'+str(msgid),
                        msgtype=mb_protocol.MSG_SYSTEM,
                        from_node=None, to_node=None,
                        subject=mb_protocol.SYS_SOCKET_RESULT, data=(msgid,result,))
        #forward
        self.forward_msg(msg)

    def get_timeout(self):
        """
        Get the message result timeout
        """
        return self.timeout

    def set_timeout(self, timeout):
        """
        Set the message result timeout
        """
        self.timeout = timeout

    #---------------------------------------------------------------------------
    def process_sys_msg(self, msg):
        """
        Process an incoming sys message 
        """
        #a result to a previous message
        if msg.subject == mb_protocol.SYS_SOCKET_RESULT:
            log.debug('reply message data: '+str(msg.data))
            msgid,res = msg.data
            sent_msg = self._replies.pop(msgid, None)
            if sent_msg is not None:
                #call the set_result method object to return the result
                sent_msg.set_result(res)
            else:
                log.error('Result recieved for unknown msgid: '+msgid)
            return

        #a close request
        if msg.subject  == mb_protocol.SYS_NODE_CLOSE:
            log.debug('Node close request')
            self.close()
            return

        #a close notification
        if msg.subject  == mb_protocol.SYS_SOCKET_CLOSING:
            log.debug('Node closing notification')
            self._closing = True
            return

    def process_msg(self, msg):
        """
        Process an incomming addressed message
        """
        pass

    def process_published(self, msg):
        """
        Process an incomming published message
        """
        pass

    

#-------------------------------------------------------------------------------
# Base server channel
#-------------------------------------------------------------------------------
class ServerChannel(asyncore.dispatcher):
    def __init__(self, map, port=6667, allow_ext=False):    
        """
        A channel object that listens for an incoming connections.
        """
        asyncore.dispatcher.__init__ (self, map=map)

        #store some internal attributes
        self.port = port
        self.allow_ext = allow_ext

        #create the socket and listen for connections
        self.create_socket (socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()

        if allow_ext is True:
            host = socket.gethostname()
        else:
            host = 'localhost'
        address = (host,port)
        self.bind(address)

        #start listening for connections
        self.listen(5)

    def get_port(self):
        """
        Get the port the server is listening on
        """
        return self.port
        
    def get_external_allowed(self):
        """
        Get whether the server allows external (non-localhost) connections
        """
        return self.allow_ext

    def writable(self):
        return False
        
    #---------------------------------------------------------------------------
    def handle_accept(self):
        pass


#-------------------------------------------------------------------------------
# Communications thread using select to control connection objects implementing 
# the handle_*  methods.
#-------------------------------------------------------------------------------
class MBThread(threading.Thread):
    """
    Thread running the main socket communications loop.
    This monitors objects added via add_channel/remove_channel or given in
    the mapping dictionary consisting of {socket:object}.
    
    The channel objects should implement handle_* methods.
    
    See:
        MBServer        -   a socket listening for incomming connections
        MBRemoteNode    -   a MessageBus Node represent a remote connection.  
    """
    def __init__(self, map={}):
        """
        Create a MBThread to manage communications on the sockets given in the 
        dictionary.
        """
        threading.Thread.__init__(self,name='Communications async loop')
         
        #channel objects {socket:mbsocket}
        self.map = map

        #make thread a daemon (stops when main thread stops)
        self.setDaemon(True)
        
    def run(self):
        """
        Start the communications loop.
        """
        while self.map:
            try:
                asyncore.poll( timeout=0.05, map=self.map)
            except:
                pass

    #---------------------------------------------------------------------------
    # Add/remove sockets to those being monitored.
    #---------------------------------------------------------------------------      
    def get_channel_map(self):
        """
        Get the channel map dictionary this thread is managing
        """
        return self.map

    #---------------------------------------------------------------------------
    # Start/Stop the thread
    #---------------------------------------------------------------------------         
    def start(self):
        """
        Start monitoring added connections 
        """
        #start the thread
        threading.Thread.start(self)
        
    def stop(self, join=True):
        """
        Stop the communcications thread by closing all channels
        
        join - wait for comms thread to close before proceeding 
                (prevents occasional errors on exit)
        """        
        #close all the channels
        for obj in self.map.values():
            obj.close()

        #join with thread
        if join is False:
            return
        
        #called from the thread!
        if self is threading.currentThread():
            return
            
        #wait for the comms thread to end
        if self.is_alive():
            self.join()


#-------------------------------------------------------------------------------
class SocketResult():
    """
    An object representing a delayed result for socket channels.
    This uses the socket channels send_result method to return the result.
    """
    def __init__(self, node, msgid):
        """
        Create an SocketResult object.
        node is a remote node whose send_result method will be used to send the 
        res to the client.
        msgid is the message id this result relates to.
        """
        self._result = None
        self._node = node
        self._msgid = msgid

    def set_result(self, result):
        """Replacement for the msg object set_result callable"""
        #call the socket channel's send_result method with the result and msgid
        self._node.send_result( self._msgid, result)

    def get_result(self, result):
        """Replacement for the msg object get_result callable"""
        return self._result


