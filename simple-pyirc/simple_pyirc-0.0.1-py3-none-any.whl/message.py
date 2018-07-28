IRC_RESPONSES = ['001', '002', '003', '004', '005',
                 '200', '201', '202', '203', '204', '205', '206', '207',
                 '208', '209', '210', '211', '212', '219', '221', '234',
                 '235', '242', '243', '251', '252', '253', '254', '255',
                 '256', '257', '258', '259', '261', '262', '263',
                 '301', '302', '303', '305', '306', '311', '312', '313',
                 '314', '315', '317', '318', '319', '321', '322', '323',
                 '324', '325', '331', '332', '341', '342', '346', '347',
                 '348', '349', '351', '351', '353', '364', '365', '366',
                 '367', '368', '369', '371', '372', '374', '375', '376',
                 '381', '382', '383', '391', '392', '393', '394', '395']
IRC_ERRORS = ['401', '402', '403', '404', '405', '406', '407', '408', '409',
              '411', '412', '413', '414', '415', '421', '422', '423', '424',
              '431', '432', '433', '436', '437', '441', '442', '443', '444',
              '445', '446', '451', '461', '462', '463', '464', '465', '466',
              '467', '471', '472', '473', '474', '475', '476', '477', '478',
              '481', '482', '483', '484', '485', '491', '501', '502']
IRC_COMMANDS = ['ADMIN', 'AWAY', 'CONNECT', 'DIE', 'ERROR', 'INFO', 'INVITE',
                'ISON', 'JOIN', 'KICK', 'KILL', 'LINKS', 'LIST', 'LUSERS',
                'MODE', 'MOTD', 'NAMES', 'NICK', 'NOTICE', 'OPER', 'PART',
                'PASS', 'PING', 'PONG', 'PRIVMSG', 'QUIT', 'REHASH',
                'RESTART', 'SERVICE', 'SERVLIST', 'SQUERY', 'SQUIT', 'STATS',
                'SUMMON', 'TIME', 'TOPIC', 'TRACE', 'USER', 'USERHOST',
                'USERS', 'VERSION', 'WALLOPS', 'WHO', 'WHOIS', 'WHOWAS']


class IRCMsg:
    """
    An object representing an IRC message

    :attribute prefix: The optional prefix of the message (`None` when no
        prefix).
    :attribute command: The IRC command of the message.
    :attribute parameters: The list of parameters of the message.
    """
    prefix = None
    command = ""
    parameters = []

    def render(self):
        """Returns the full message as a string."""
        msg = []
        if self.prefix is not None:
            msg.append(":" + self.prefix)
        msg.append(self.command)
        if self.parameters :
            if any(c in self.parameters[-1] for c in (' ', ':')):
                # Case where the last parameter contains spaces or ':',
                # it must be marked as last parameter by prefixing with ':'
                msg.extend(self.parameters[:-1])
                msg.append(':' + self.parameters[-1])
            else:
                msg.extend(self.parameters)

        return " ".join(msg)

    def validate(self):
        """
        Validate that the message is valid according to RFC constraints.
        Raises exceptions if something is not valid.
        """
        self._validate_prefix()
        self._validate_command()
        self._validate_parameters()

        if len(self.render()) > 510:
            raise Exception("Message too long")

    def _validate_prefix(self):
        if self.prefix is None:
            return
        if " " in self.prefix:
            raise Exception("Prefix should not contains whitespaces")
    
    def _validate_command(self):
        if self.command not in IRC_COMMANDS:
            # May be a 3-digit numeric code instead
            try:
                int(self.command)
            except ValueError:
                raise Exception("Command '{}' not specified by RFC"
                                .format(self.command))
            else:
                if len(self.command) != 3:
                    raise Exception("3-digit numeric command should have "
                        "exactly 3 digits unlike '{}'".format(self.command))

    def _validate_parameters(self):
        if len(self.parameters) > 15:
            raise Exception("Too many parameters")

        for i, parameter in enumerate(self.parameters):
            if not parameter:
                raise Exception("Empty parameter is not allowed")

            # Only the last parameter can contain spaces
            exclude = (('\x00', '\r', '\n') if i == len(self.parameters) - 1
                       else ('\x00', '\r', '\n', ' '))
            if any(c in parameter for c in exclude):
                raise Exception("Invalid character in parameter")
            
            if i != len(self.parameters) and parameter[0] == ':':
                raise Exception("Only the last parameter can begin with a ':'")


class IRCInputMsg(IRCMsg):
    """An object representing an IRC message FROM the server.

    :param text: The text received that must be parsed.
    """
    def __init__(self, text):
        if not text:
            raise Exception("Missing argument, cannot parse message")
        
        # Remove potential whitespaces even if there should not be any
        text = text.strip()

        if text[0] == ":":  # There is a prefix
            components = text.split(' ', maxsplit=2)
            if not len(components) > 1:
                raise Exception("Missing argument, cannot parse message")
            self.prefix = components[0][1:]  # Remove the ':' from the prefix
            cmd_index = 1
        else:  # No prefix specified
            components = text.split(maxsplit=1)
            cmd_index = 0

        self.command = components[cmd_index]
        
        if len(components) > cmd_index + 1:  # There are parameters
            parameters = components[cmd_index + 1].split(maxsplit=14)

            # Look for the first parameter beggining with a ':'
            i = 0
            while i < len(parameters) and parameters[i][0] != ':':
                i += 1
            if i != len(parameters):
                # Parameter i is the first to begin with a ':'
                # All following parameters are considered the last parameter
                # which can contain spaces and ':'
                parameters[i] = parameters[i][1:]  # Remove the ':'
                parameters[i:] = [" ".join(parameters[i:])]  # Concatenate

            self.parameters = parameters


class IRCOutputMsg(IRCMsg):
    """An object representing an IRC message TO the server.

    :param command: The IRC command to send
    :param *parameters: The expanded list of parameters of the message.
    """
    def __init__(self, command, *parameters):
        self.command = command
        self.parameters = parameters
    
    def _validate_prefix(self):
        # The only valid prefix for a client-to-server message is the
        # nickname of the client or nothing. So in this implementation
        # the client cannot send prefixes at all.
        if self.prefix is not None:
            raise Exception("Client cannot send prefixes")

    def _validate_command(self):
        super(IRCOutputMsg, self)._validate_command()
        if self.command not in IRC_COMMANDS:
            raise Exception("Client should only send IRC commands not numerical responses")
