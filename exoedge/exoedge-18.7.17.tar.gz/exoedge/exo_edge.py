"""
ExoEdge module. Provides high-level functionality to play nicely
with Exosite's Remote Condition Monitoring solution for Industrial IoT.
"""
from __future__ import print_function
import json
import logging
import threading
import time

from exoedge.config_io import ConfigIO

LOG = logging.getLogger('EXOEDGE.' + __name__)


class ExoEdge(object):
    """
    ExoEdge is the root class for integration with ExoSense. An instance
    is created from a Device and is set up using one of several strategies:
        -   local:      Set up ExoEdge from a local file. Upon completion
                        write this value to Murano.
        -   remote:     Set up ExoEdge from config_io in Murano.
    TODO: GMQ support
    TODO: refactor to use q.put() and q.get()
    """

    def __init__(self,
                 D,
                 **kwargs):
        """ Onus of initialization is on the application.

        Parameters:
        D:                  Device/connection object from murano_client.
        strategy:           The strategy with which to instantiate an ExoSense
                            object.
                            local | read | subscribe
        config_io_file:     Local file used to cache copy of config_io.
                            Typically `./<UUID>.json`.
        cache_config_io:    Whether or not to save a local copy of
                            config_io in config_io_file.
        config_io_sync:     Whether or not to keep local copy of config_io
                            synced with Murano.
        """
        self.strategy = 'local' if kwargs.get('local_strategy') else 'remote'

        global config_io, device
        # config_io = ConfigIO(config_io)
        config_io = ConfigIO(None)
        device = D

        self.cache_config_io = not kwargs.get('no_config_cache')  # cache_config_io
        self.config_io_file = kwargs.get('config_io_file') or '{}.json'.format(kwargs.get('murano_id'))
        self.config_io_sync = not kwargs.get('no_config_sync')    # config_io_sync

        if self.config_io_sync:
            self.config_io_watcher = ConfigIOWatcher(self.config_io_file,
                                                     self.cache_config_io)

        self.data_in_writer = DataInWriter()
        self._kill = False

    def kill(self):
        """ Stop reporting

        Calls config_io.ConfigIO.kill(), which eventually causes the Channels
        and their respective ChannelWatchers to die gracefully.
        """
        LOG.info('killing...')

        global config_io
        config_io.kill()

        if self.config_io_sync:
            self.config_io_watcher.kill()

        self.data_in_writer.kill()
        config_io.e_send_data_in.set()
        self._kill = True

    def setup(self):
        global config_io

        if self.strategy == 'local':
            config_io.set_config_io(self.read_local_config_io())
            self.tell_mur_config_io()

        elif self.strategy == 'remote':
            self.retrieve_remote_config_io()
            self.write_local_config_io()

        _ = self.config_io_watcher.start() if self.config_io_sync else None
        config_io.start()

        self.data_in_writer.start()

    def tell_mur_config_io(self):
        """ Write to Murano config_io resource. """
        device.tell(resource='config_io',
                    timestamp=time.time(),
                    payload=json.dumps(config_io._new_config_io))

    def write_local_config_io(self):
        """ Write config_io to local file.

        TODO: Rename method.
        """
        if self.cache_config_io:
            LOG.info('writing the following to local config io file %s:',
                     self.config_io_file)
            LOG.info(json.dumps(config_io._new_config_io, indent=2))
            with open(self.config_io_file, 'w') as f:
                json.dump(config_io._new_config_io, f)

    def read_local_config_io(self):
        """ Read config_io from local file. """
        infostr = 'READING LOCAL CONFIG_IO'
        LOG.critical('\n{:-^80}\n'.format(infostr))

        if self.config_io_file:
            try:
                return json.load(open(self.config_io_file, 'r'))

            except IOError:
                raise NoLocalConfigIO('config_io file {} does not exist.'
                                      .format(self.config_io_file))

        else:
            raise NoLocalConfigIO('A local config_io file has not been set.')

    def retrieve_remote_config_io(self):
        """ Get config_io from Murano """
        infostr = 'RETRIEVING CONFIG_IO FROM EXOSENSE'
        LOG.critical('\n{:-^80}\n'.format(infostr))

        inbound = device.watch(timeout=5.0)
        if inbound and inbound.resource == 'config_io':
            global config_io
            config_io.set_config_io(json.loads(inbound.payload))
            self.tell_mur_config_io()
        else:
            self.retrieve_remote_config_io()


class DataInWriter(threading.Thread, object):
    """ Class to deal with writing data_in.

    TODO: Rename class.
    TODO: refactor to use q.put() for murano_client
    """
    def __init__(self,
                 wait_timeout=1.0):
        """
        DataInWriter initialized by ExoEdge.go()

        Parameters:
        wait_timeout:       Timeout to wait for e_send_data_in event before
                            reevaluating own _kill status
        """
        threading.Thread.__init__(self)
        self.wait_timeout = wait_timeout
        self._kill = False

    def kill(self):
        """ Stop all activity. """
        self._kill = True

    def package_data_in(self, timeout=1.0):
        """ Assemble data_in JSON blob.

        Takes signal data and assembles into a packet that
        ExoEdge understands.

        TODO: Implement or remove timeout parameter.
        """
        data = config_io.get_channel_data()
        if data:
            return json.dumps(data)
        else:
            return None

    def write_data_in(self):
        """ Write to Murano resource data_in

        Called by run()
        """
        data = self.package_data_in()
        if data:
            LOG.critical('WRITING DATA: %s', data)
            device.tell(resource='data_in',
                        timestamp=time.time(),
                        payload=data)
        else:
            LOG.debug('NO DATA TO SEND')

    def run(self):
        """ Wait for e_send_data_in event to be set

        Event set by config_io.ChannelWatcher.run(). Upon set,
        write_data_in()
        """
        LOG.debug('starting')
        while not self._kill:
            global config_io
            delivery = config_io.e_send_data_in.wait(self.wait_timeout)
            if delivery:
                self.write_data_in()

            config_io.e_send_data_in.clear()
        LOG.debug('exiting')


class ConfigIOWatcher(threading.Thread, object):
    """
    Class to deal with keeping local and cloud config_io
    in sync. Created if config_io_sync is set to True
    upon initiation of ExoEdge.

    TODO: refactor to q.get() from murano client
    """
    def __init__(self,
                 config_io_file=None,
                 cache_config_io=False,
                 timeout=300000):
        """
        Initialized by ExoEdge.go()

        Parameters:
        config_io_file:     File to save local copy of config_io
        cache_config_io:    Whether or not to save a local copy of config_io
        timeout:            Timeout to longpoll config_io resource in Murano
        """
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.cache_config_io = cache_config_io
        self.config_io_file = config_io_file
        self.timeout = timeout
        self._kill = False

    def kill(self):
        """ Stop activity. """
        self._kill = True

    def write_local_config_io(self):
        """ Write config_io to local file.

        TODO: Rename method.
        """
        LOG.debug('writing to local config io file %s',
                  self.config_io_file)
        with open(self.config_io_file, 'w') as f:
            json.dump(config_io._new_config_io, f)

    def run(self):
        """ Longpoll config_io.

        Informs config_io.ConfigIO that new config_io has been found.
        """
        while not self._kill:
            global config_io, device
            inbound = device.watch(timeout=5)
            if inbound and inbound.resource == 'config_io':
                config_io.set_config_io(json.loads(inbound.payload))

                device.tell(resource='config_io',
                            payload=inbound.payload,
                            timestamp=time.time())
                _ = self.write_local_config_io() if self.cache_config_io else None

            else:
                LOG.debug('No config_io payload')


class ExoEdgeException(Exception):
    """
    Base exception class
    """
    pass


class ConfigIONotFound(ExoEdgeException):
    pass


class ConfigIONotSet(ConfigIONotFound):
    pass

class NoLocalConfigIO(ConfigIONotFound):
    pass

class MaxLongpollAttempts(ExoEdgeException):
    pass
