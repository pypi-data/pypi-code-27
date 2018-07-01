#!/usr/bin/env python
import os
import logging
import signal
import traceback
import zulip
import sys
import argparse
import re
import configparser

from collections import OrderedDict

from types import FrameType
from typing import Any, Callable, Dict, Optional

from matrix_client.errors import MatrixRequestError
from matrix_client.client import MatrixClient
from requests.exceptions import MissingSchema

GENERAL_NETWORK_USERNAME_REGEX = '@_?[a-zA-Z0-9]+_([a-zA-Z0-9-_]+):[a-zA-Z0-9.]+'
MATRIX_USERNAME_REGEX = '@([a-zA-Z0-9-_]+):matrix.org'

# change these templates to change the format of displayed message
ZULIP_MESSAGE_TEMPLATE = "**{username}**: {message}"
MATRIX_MESSAGE_TEMPLATE = "<{username}> {message}"

class Bridge_ConfigException(Exception):
    pass

class Bridge_FatalMatrixException(Exception):
    pass

class Bridge_ZulipFatalException(Exception):
    pass

def matrix_login(matrix_client, matrix_config):
    # type: (Any, Dict[str, Any]) -> None
    try:
        matrix_client.login_with_password(matrix_config["username"],
                                          matrix_config["password"])
    except MatrixRequestError as exception:
        if exception.code == 403:
            raise Bridge_FatalMatrixException("Bad username or password.")
        else:
            raise Bridge_FatalMatrixException("Check if your server details are correct.")
    except MissingSchema as exception:
        raise Bridge_FatalMatrixException("Bad URL format.")

def matrix_join_room(matrix_client, matrix_config):
    # type: (Any, Dict[str, Any]) -> Any
    try:
        room = matrix_client.join_room(matrix_config["room_id"])
        return room
    except MatrixRequestError as exception:
        if exception.code == 403:
            raise Bridge_FatalMatrixException("Room ID/Alias in the wrong format")
        else:
            raise Bridge_FatalMatrixException("Couldn't find room.")

def die(signal, frame):
    # type: (int, FrameType) -> None
    # We actually want to exit, so run os._exit (so as not to be caught and restarted)
    os._exit(1)

def matrix_to_zulip(zulip_client, zulip_config, matrix_config, no_noise):
    # type: (zulip.Client, Dict[str, Any], Dict[str, Any], bool) -> Callable[[Any, Dict[str, Any]], None]
    def _matrix_to_zulip(room, event):
        # type: (Any, Dict[str, Any]) -> None
        """
        Matrix -> Zulip
        """
        content = get_message_content_from_event(event, no_noise)

        zulip_bot_user = ('@%s:matrix.org' % matrix_config['username'])
        # We do this to identify the messages generated from Zulip -> Matrix
        # and we make sure we don't forward it again to the Zulip stream.
        not_from_zulip_bot = ('body' not in event['content'] or
                              event['sender'] != zulip_bot_user)

        if not_from_zulip_bot and content:
            try:
                result = zulip_client.send_message({
                    "sender": zulip_client.email,
                    "type": "stream",
                    "to": zulip_config["stream"],
                    "subject": zulip_config["topic"],
                    "content": content,
                })
            except Exception as exception:  # XXX This should be more specific
                # Generally raised when user is forbidden
                raise Bridge_ZulipFatalException(exception)
            if result['result'] != 'success':
                # Generally raised when API key is invalid
                raise Bridge_ZulipFatalException(result['msg'])

    return _matrix_to_zulip

def get_message_content_from_event(event, no_noise):
    # type: (Dict[str, Any], bool) -> Optional[str]
    irc_nick = shorten_irc_nick(event['sender'])
    if event['type'] == "m.room.member":
        if no_noise:
            return None
        # Join and leave events can be noisy. They are ignored by default.
        # To enable these events pass `no_noise` as `False` as the script argument
        if event['membership'] == "join":
            content = ZULIP_MESSAGE_TEMPLATE.format(username=irc_nick,
                                                    message="joined")
        elif event['membership'] == "leave":
            content = ZULIP_MESSAGE_TEMPLATE.format(username=irc_nick,
                                                    message="quit")
    elif event['type'] == "m.room.message":
        if event['content']['msgtype'] == "m.text" or event['content']['msgtype'] == "m.emote":
            content = ZULIP_MESSAGE_TEMPLATE.format(username=irc_nick,
                                                    message=event['content']['body'])
    else:
        content = event['type']
    return content

def shorten_irc_nick(nick):
    # type: (str) -> str
    """
    Add nick shortner functions for specific IRC networks
    Eg: For freenode change '@freenode_user:matrix.org' to 'user'
    Check the list of IRC networks here:
    https://github.com/matrix-org/matrix-appservice-irc/wiki/Bridged-IRC-networks
    """
    match = re.match(GENERAL_NETWORK_USERNAME_REGEX, nick)
    if match:
        return match.group(1)
    # For matrix users
    match = re.match(MATRIX_USERNAME_REGEX, nick)
    if match:
        return match.group(1)
    return nick

def zulip_to_matrix(config, room):
    # type: (Dict[str, Any], Any) -> Callable[[Dict[str, Any]], None]

    def _zulip_to_matrix(msg):
        # type: (Dict[str, Any]) -> None
        """
        Zulip -> Matrix
        """
        message_valid = check_zulip_message_validity(msg, config)
        if message_valid:
            matrix_username = msg["sender_full_name"].replace(' ', '')
            matrix_text = MATRIX_MESSAGE_TEMPLATE.format(username=matrix_username,
                                                         message=msg["content"])
            # Forward Zulip message to Matrix
            room.send_text(matrix_text)
    return _zulip_to_matrix

def check_zulip_message_validity(msg, config):
    # type: (Dict[str, Any], Dict[str, Any]) -> bool
    is_a_stream = msg["type"] == "stream"
    in_the_specified_stream = msg["display_recipient"] == config["stream"]
    at_the_specified_subject = msg["subject"] == config["topic"]

    # We do this to identify the messages generated from Matrix -> Zulip
    # and we make sure we don't forward it again to the Matrix.
    not_from_zulip_bot = msg["sender_email"] != config["email"]
    if is_a_stream and not_from_zulip_bot and in_the_specified_stream and at_the_specified_subject:
        return True
    return False

def generate_parser():
    # type: () -> argparse.ArgumentParser
    description = """
    Script to bridge between a topic in a Zulip stream, and a Matrix channel.

    Tested connections:
        * Zulip <-> Matrix channel
        * Zulip <-> IRC channel (bridged via Matrix)

    Example matrix 'room_id' options might be, if via matrix.org:
        * #zulip:matrix.org (zulip channel on Matrix)
        * #freenode_#zulip:matrix.org (zulip channel on irc.freenode.net)"""

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', required=False,
                        help="Path to the config file for the bridge.")
    parser.add_argument('--write-sample-config', metavar='PATH', dest='sample_config',
                        help="Generate a configuration template at the specified location.")
    parser.add_argument('--show-join-leave', dest='no_noise',
                        default=True, action='store_false',
                        help="Enable IRC join/leave events.")
    return parser

def read_configuration(config_file):
    # type: (str) -> Dict[str, Dict[str, str]]
    config = configparser.ConfigParser()

    try:
        config.read(config_file)
    except configparser.Error as exception:
        raise Bridge_ConfigException(str(exception))

    if set(config.sections()) != {'matrix', 'zulip'}:
        raise Bridge_ConfigException("Please ensure the configuration has zulip & matrix sections.")

    # TODO Could add more checks for configuration content here

    return {section: dict(config[section]) for section in config.sections()}

def write_sample_config(target_path):
    # type: (str) -> None
    if os.path.exists(target_path):
        raise Bridge_ConfigException("Path '{}' exists; not overwriting existing file.".format(target_path))

    sample_dict = OrderedDict((
        ('matrix', OrderedDict((
            ('host', 'https://matrix.org'),
            ('username', 'username'),
            ('password', 'password'),
            ('room_id', '#zulip:matrix.org'),
        ))),
        ('zulip', OrderedDict((
            ('email', 'glitch-bot@chat.zulip.org'),
            ('api_key', 'aPiKeY'),
            ('site', 'https://chat.zulip.org'),
            ('stream', 'test here'),
            ('topic', 'matrix'),
        ))),
    ))

    sample = configparser.ConfigParser()
    sample.read_dict(sample_dict)
    with open(target_path, 'w') as target:
        sample.write(target)

def main():
    # type: () -> None
    signal.signal(signal.SIGINT, die)
    logging.basicConfig(level=logging.WARNING)

    parser = generate_parser()
    options = parser.parse_args()

    if options.sample_config:
        try:
            write_sample_config(options.sample_config)
        except Bridge_ConfigException as exception:
            sys.exit(exception)
        print("Wrote sample configuration to '{}'".format(options.sample_config))
        sys.exit(0)
    elif not options.config:
        print("Options required: -c or --config to run, OR --write-sample-config.")
        parser.print_usage()
        sys.exit(1)

    try:
        config = read_configuration(options.config)
    except Bridge_ConfigException as exception:
        sys.exit("Could not parse config file: {}".format(exception))

    # Get config for each client
    zulip_config = config["zulip"]
    matrix_config = config["matrix"]

    # Initiate clients
    backoff = zulip.RandomExponentialBackoff(timeout_success_equivalent=300)
    while backoff.keep_going():
        print("Starting matrix mirroring bot")
        try:
            zulip_client = zulip.Client(email=zulip_config["email"],
                                        api_key=zulip_config["api_key"],
                                        site=zulip_config["site"])
            matrix_client = MatrixClient(matrix_config["host"])

            # Login to Matrix
            matrix_login(matrix_client, matrix_config)
            # Join a room in Matrix
            room = matrix_join_room(matrix_client, matrix_config)

            room.add_listener(matrix_to_zulip(zulip_client, zulip_config, matrix_config,
                                              options.no_noise))

            print("Starting listener thread on Matrix client")
            matrix_client.start_listener_thread()

            print("Starting message handler on Zulip client")
            zulip_client.call_on_each_message(zulip_to_matrix(zulip_config, room))

        except Bridge_FatalMatrixException as exception:
            sys.exit("Matrix bridge error: {}".format(exception))
        except Bridge_ZulipFatalException as exception:
            sys.exit("Zulip bridge error: {}".format(exception))
        except zulip.ZulipError as exception:
            sys.exit("Zulip error: {}".format(exception))
        except Exception as e:
            traceback.print_exc()
        backoff.fail()

if __name__ == '__main__':
    main()
