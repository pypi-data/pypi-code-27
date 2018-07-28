import socket
import select
import threading
import logging

from .message import IRCOutputMsg, IRCInputMsg


class IRCClient:
    """
    Creates a light IRC Client that can be used to send messages to a server.

    :param network: The network hostname to connect to
        (e.g. `chat.freenode.net`).
    :param nickname: The nickname to connect with.
    :param port: (Optional) The port to use for connection. Default is `6667`.
    :param password: (Optional) The password to use if one is needed
    :param username: (Optional) The username to use. Default is the nickname.
        Has an effect only if `is_service` is set to `False`.
    :param realname: (Optional) The realname to use. Default is the nickname.
        Has an effect only if `is_service` is set to `False`.
    :param is_service: (Optional) Is the client a service (see RFC 2812 - 
        section 1.2.2) ? Default is `False`.
    :param info: (Optional) The information about the service. Default is the
        niclname. Has an effect only if `is_service` is set `True`.
    :param loglevel: Set the minimal log level to output logs. See `logging`'s
        levels.
    """

    def __init__(self, network, nickname, port=6667, password=None, 
                 username=None, realname=None, is_service=False, info=None,
                 loglevel=logging.ERROR):

        # Set up logger
        self.logger = logging.getLogger(__name__)
        if not self.logger.hasHandlers():
            # Avoid to get multiple handlers even if there are mutliple clients
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(loglevel)

        # Save options
        self.network = network
        self.port = port
        self.nickname = nickname
        self.username = username or nickname
        self.realname = realname or nickname
        self.is_service = is_service
        self.info = info or self.realname

        # Connect to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect_to_network(password)
    
        # Start the listening thread used to answer PING commands
        self.exec_lock = threading.Lock()
        self.exec_lock.acquire()
        self.listen_thread = threading.Thread(target=self._listen_loop)
        self.listen_thread.start()

    def _send(self, msg):
        """
        Send a string to the socket. Add the CRLF ending.

        :param s: The string to send
        """
        msg.validate()
        s = msg.render()
        self.logger.debug("=> " + s)
        b = (s + "\r\n").encode()
        self.sock.send(b)

    def _get_line(self, timeout=None):
        """
        Retrieve a single line from the socket. Remove the trailing CRLF.

        :param timeout: (Optional) Maximum time to wait for an answer in
            seconds. Default is None which means wait forever.
        :returns: The raw line as received without the trailing CRLF.
        """
        l = ""
        while True:
            i, o, e = select.select([self.sock], [], [], timeout)
            if not i and timeout is not None:
                return None
            # Replace decoding error instead of ignore else it is an empty
            # character which means the connection has been closed.
            r = self.sock.recv(1).decode(errors='replace')
            if not r:  # Empty character
                raise Exception("Connection closed")
            if r is "\n":  # End of line
                return l
            if r is not "\r":  # characters that are part of the line
                l += r

    def _read(self, timeout=None):
        """
        Read 1 line from the socket and answers PING commands automatically.
        
        :param timeout: (Optional) Maximum time to wait for an answer in
            seconds. Default is None which means wait forever.
        :returns: The line read from the socket or None if timeout was reached.
        """
        line = self._get_line(timeout)
        if not line:
            return None
        self.logger.debug("<= " + line)
        msg = IRCInputMsg(line)  # Cast to an IRCMsg
        try:
            msg.validate()
        except Exception as e:
            self.logger.error(e)
        if msg.command == "PING":
            self.pong(msg.parameters[0])
        return msg

    def _empty_buffer(self):
        """
        Empty the input buffer of the socket from every message.
        """
        while self._read(timeout=1) is not None:
            pass

    def _listen_loop(self):
        """
        A loop used to listen to the socket input in a separate thread
        in order to answer PING commands and keep the connection alive.
        """
        while not self.exec_lock.acquire(blocking=False):
            self._read(timeout=1)
        self.exec_lock.release()

    def join(self, *channels, keys=None):
        """
        IRC `JOIN` command.

        Examples:
            `client.join("#chan")`
                ask to join #chan
            `client.join("#chan1", "#chan2", "#chan3")`
                ask to join #chan1, #chan2 and #chan3
            `client.join("#chan1", "#chan2", keys=["key1", key2"])`
                ask to join #chan1 using key1 and #chan2 using key2
            `client.join("#chan1", "#chan2", keys=["key1"])`
                ask to join #chan1 using key1 and #chan2 with no key

        :param *channels: The expanded list of channels to join
        :param keys: The list of keys to use for each channel
        """
        if keys:
            msg = IRCOutputMsg("JOIN", ",".join(channels), ",".join(keys))
        else:
            msg = IRCOutputMsg("JOIN", ",".join(channels))
        self._send(msg)
        self._empty_buffer()

    def nick(self, nickname):
        """
        IRC `NICK` command.

        Example:
            `client.nick("MoaMoaK")`
                Set the nickname to MoaMoaK

        :param nickname: The nickname to use.
        """
        msg = IRCOutputMsg("NICK", nickname)
        self._send(msg)
        self._empty_buffer()

    def part(self, *channels, part_message=""):
        """
        IRC `PART` command.

        Examples:
            `client.part("#chan")`
                Leave #chan.
            `client.part("#chan1", "#chan2", "#chan3")`
                Leave #chan1, #chan2 and #chan3 at the same time.
            `client.part("#chan", part_message="See you soon!")`
                Leave #chan with the message 'See you soon!'
        
        :param *channels: The expanded list of channels to leave.
        :param part_message: (Optional) A message to inform other while 
            leaving. Default is to not send a part message.
        """
        chans = ",".join(channels)
        if part_message:
            msg = IRCOutputMsg("PART", ",".join(channels), part_message)
        else:
            msg = IRCOutputMsg("PART", ",".join(channels))
        self._send(msg)
        self._empty_buffer()

    def pass_(self, password):
        """
        IRC `PASS` command. This commands has a trailing '_' because the
        key-word 'pass' is reserved by python.

        Example:
            `client.pass_("password")`
                Authenticate using password 'password'.

        :param password: The password to use.
        """
        msg = IRCOutputMsg("PASS", password)
        self._send(msg)
        sefl._empty_buffer()

    def pong(self, server):
        """
        IRC `PONG` command.

        Example:
            `client.pong("serv1.net")`
                Respond to a ping from serv1.net

        :param server: The server to which respond.
        """
        msg = IRCOutputMsg("PONG", server)
        self._send(msg)
        self._empty_buffer()

    def privmsg(self, msgtarget, text_to_be_sent):
        """
        IRC `PRIVMSG` command.

        Examples:
            `client.privmsg("#chan", "Hello, world !")`
                Send 'Hello, world !' to the chan '#chan'
            `client.privmsg("nice_guy", "Good bye !")`
                Send 'Good bye !' to the user nicknamed 'nice_guy'

        :param msgtarget: The target of the message.
        :param text_to_be_sent: The message to send to the target.
        """
        msg = IRCOutputMsg("PRIVMSG", msgtarget, text_to_be_sent)
        self._send(msg)
        self._empty_buffer()

    def quit(self, quit_message=None):
        """
        IRC `QUIT` command.

        Examples:
            `client.quit()`
                Quit the network.
            `client.quit("Adios amigos")
                Send send the message 'Adios amigos' while quitting the network.

        :param quit_message: (Optional) A message to send to the network while
            quitting. Default is to not send any message.
        """
        if quit_message is None:
            msg = IRCOutputMsg("QUIT")
        else:
            msg = IRCOutputMsg("QUIT", quit_message)
        self._send(msg)

    def service(self, nickname, distribution, info):
        """
        IRC `SERVICE` command. This command is not supported by server
        implementation based on RFC 1459.

        Example:
            `client.service("dict", "*.fr", "French Dictionnary")`
                Service resgistring itself with a name of dict. This service
                will only be available on servers which name matches '*.fr'.

        :param nickname: The nickname of the service.
        :param distribution: The visibility of the service. See RFC 2812 -
            section 3.1.6 for more details.
        :param info: Some information about the service.
        """
        msg = IRCOutputMsg("SERVICE", nickname, '*', distribution, '0', '0',
                           info)
        self._send(msg)
        self._empty_buffer()
        
    def user(self, user, mode, realname):
        """
        IRC `USER` command. This command uses RFC 2812 specification as the
        `hostname` and `servername` fields defined in RFC 1459 should be
        ignored in a client-to-server message according to RFC 1459 - section
        4.1.3. That way both RFC are covered and supported.

        Examples:
            `client.user("username", 0, "My real name")`
                Specify the client has the username 'username' and a realname
                'My real name'.
            `client.user("A", 8, "B")`
                Specify the client has the username 'A' and the realname 'B'
                and is invisible.

        :param user: The username of the client.
        :param mode: The client mode to use. See RFC 2812 - section 3.1.3 for
            more details. In case of server implementation based on RFC 1459,
            this field is ignored.
        :param realname: The real name of the client.
        """
        msg = IRCOutputMsg("USER", user, mode, '*', realname)
        self._send(msg)
        self._empty_buffer()

    def _connect_to_network(self, password=None):
        """
        Initialize the connection to the network by sending the
        initial required IRC commands. See RFC 2812 - section 3.1 for more.

        :param password: (Optional) A password to use to authenticate. Default
            is to not use any password. Passing the password as an argument is
            to avoid to store it.
        """
        # Connect to the socket
        self.sock.connect((self.network, self.port))

        if password is not None:
            # Use the password if needed
            self.pass_(password)

        if self.is_service:
            # Connect as a service
            self.service(self.nickname, '*', self.info)
        else:
            # Connect as a user
            self.nick(self.nickname)
            self.user(self.username, '0', self.realname)

    def close(self):
        """
        Close the IRC client by quitting the network and closing the socket.
        """
        self.exec_lock.release()
        self.listen_thread.join()
        self.quit()
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
