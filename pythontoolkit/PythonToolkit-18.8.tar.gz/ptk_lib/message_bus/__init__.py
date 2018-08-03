"""
Package name: MessageBus
------------

Description:
------------

An intra-process and inter-process communications system.

Nodes (MBNode objects) connect to the message bus to send and recieve messages. 
These can either be published (sent to all nodes - no result/reply returned) or
addressed (sent to another node by name - with (optionally) the result returned).

The message sending/publishing system is thread safe with all messages being 
processed in the mainthread. The result/reply of addressed messages are returned
to sending thread (which blocks until this is recieved).

External processes can connect to the message bus using sockets by creating a 
MBClient object. This connects to the message bus via a RemoteNode object 
which forwards messages over the socket connection.
"""
