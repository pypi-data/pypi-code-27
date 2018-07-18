# pylint: disable=W0141,W0110,C0103
"""
ExoEdge ConfigIO module to handle Channel creation from a config_io object.
"""
from __future__ import print_function
import threading
import logging
import json
from exoedge.channel import Channel

LOG = logging.getLogger('EXOEDGE.' + __name__)

class ConfigIO(threading.Thread, object):
    """
    This class provides methods to create channels from a
    config_io and to format the data_in object to be sent
    to Murano. ConfigIO must be supplied a config_io as a
    dictionary.
    """
    __lock = threading.Lock()
    e_send_data_in = threading.Event()
    e_new_config = threading.Event()

    def __init__(self,
                 config_io,
                 wait_timeout=1.0):
        threading.Thread.__init__(self)
        self.config_io = {}
        self.wait_timeout = wait_timeout
        self._new_config_io = config_io
        self.last_report = 0
        self.channels = {}
        self._kill = False

    def kill(self):
        """ Stop all activity.

        Stops activity of all Channel threads, Channel-
        Watcher threads, and the ConfigIO thread.
        """
        self.kill_all_channels()
        self._kill = True

    def _has_channels(self):
        """ Return whether or not ConfigIO has channels.

        Used to determine if there are channels to kill.
        """
        return bool(self.channels)

    def _add_channel(self, name, ch_cfg):
        """ Create Channel and ChannelWatcher threads.

        Create a Channel and ChannelWatcher from a channel
        configuration object. Store them in the ConfigIO.channels
        dictionary.

        Parameters:
        ch_cfg:     the object representation of the channel
                    taken from config_io.
        name:       the key of the ch_cfg object in config_io

        """
        LOG.info('adding channel %s', name)
        ch_cfg['name'] = name
        channel = Channel(**ch_cfg)
        watcher = ChannelWatcher(channel,
                                 self.__lock,
                                 self.e_send_data_in)
        self.channels[name] = {'channel': channel,
                               'watcher': watcher}
        return

    def kill_all_channels(self):
        """ Stop Channel threads.

        Set Channel._kill = True for all Channels in ConfigIO.channels.
        Called by ConfigIO.run() when a new config_io is received.
        """
        LOG.info('killing all channels')
        for name, d in self.channels.items():
            logging.debug('killing channel %s', name)
            d['channel'].kill()
        self.channels = {}

    def set_config_io(self, cfg):
        """ Handle a new config_io.

        Handler for storing a newly received config_io and
        notifying the thread accordingly. Called by
        exo_edge.ConfigIOWatcher.run()

        Parameters:
        cfg:        the object representation of the config_io
        """
        LOG.critical('Received new config_io:\n%s',
                     json.dumps(cfg, indent=2))
        self._new_config_io = cfg
        self.e_new_config.set()

    def get_channel_data(self):
        """ Get data from Channel queues.

        Current implementation clears the queue after getting one value by
        either calling q.clear() or setting q to an empty list, per the
        implementation of LIFO queues.

        TODO: implement down_sampling
        """
        data_in = {}
        for name, d in self.channels.items():
            q = d['channel'].q_out
            if not q.empty():
                data_in[name] = d['channel'].downsampler.down_sample(
                    list(q.queue))
                # data_in[name] = q.get(timeout=0.0)
                try:
                    q.queue.clear()
                except AttributeError:  # LifoQueue.queue is a list
                    q.queue = []
            else:
                continue
        return data_in

    def run(self):
        """ Update ConfigIO and Channels upon new config_io.

        Waits for a new config_io event set by ConfigIO.set_config_io() and
        subsequently kills existing channels before creating new channels from
        the newly received config_io object. Starts Channels and ChannelWatchers.
        """
        LOG.debug('starting')
        self.e_new_config.set()     # set upon start()
        while not self._kill:
            if self.e_new_config.wait(self.wait_timeout):
                LOG.debug('Received config_io')

                if self._has_channels():
                    self.kill_all_channels()

                for name, cfg in self._new_config_io['channels'].items():
                    self._add_channel(name, cfg)

                # start all Channels and ChannelWatchers
                map(
                    lambda x: map(
                        lambda y: y.start(),
                        x.values()
                    ),
                    self.channels.values())

                self.e_new_config.clear()
                self.config_io = self._new_config_io
            else:
                LOG.debug('no new config')
        LOG.debug('exiting')


class ChannelWatcher(threading.Thread, object):
    """ Watch for new data from Channel.

    One ChannelWatcher is created per Channel. It waits for new data from a
    Channel and notifies ConfigIO of this activity.
    """
    def __init__(self,
                 C,
                 lock,
                 request_event,
                 wait_timeout=1.0):
        """
        ChannelWatcher initialized by ConfigIO._add_channel()

        Parameters:
        C:              Channel instance
        lock:           threading.lock instance used to set ConfigIO's
                        request_event
        request_event:  event used to notify ConfigIO of activity. Currently
                        implemented as e_new_data_in
        """
        threading.Thread.__init__(self, name=C.name)
        self.C = C
        self.lock = lock
        self.e_send_data_in = request_event
        self.wait_timeout = wait_timeout
        self.name = 'watcher-{}'.format(C.name)

    def run(self):
        """ Wait for Channel emission and requests data_in be packaged.

        ChannelWatcher watches its associated Channel's e_emission event
        called by channel.Channel.emit().
        """
        LOG.debug('starting')

        while not self.C.is_killed():
            if self.C.e_emission.wait(self.wait_timeout):
                LOG.debug('Received emission from Channel')
                with self.lock:
                    self.e_send_data_in.set()
                self.C.e_emission.clear()

        self.e_send_data_in.set()
        LOG.debug('exiting')
