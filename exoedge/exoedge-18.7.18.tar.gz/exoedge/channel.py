# pylint: disable=C0103,R0902
"""
Module to generate data from arbitrary source modules as defined in config_io.
"""
import os
import sys
import time
import logging
import json
import threading
import six
if six.PY2:
    import Queue as queue
elif six.PY3:
    import queue
path = os.path.dirname(
    os.path.realpath(__file__)
).rsplit('/', 1)[0] + '/sources'
sys.path.append(path)

LOG = logging.getLogger('EXOEDGE.' + __name__)


class Channel(threading.Thread, object):
    """
    A Channel is connected to a Source, which provides the Channel
    with data to send in data_in.

    This class provides methods to get new data from a source specified in
    config_io.
    """
    def __init__(self, **kwargs):
        """
        Channel initialized by config_io.ConfigIO._add_channel()

        Parameters:
        name:               The key used for the channel object in config_io
        display_name:       The human-readable display name of the Channel
        description:        The description of the Channel
        properties:         <<<General metadata store>>>
                            <<<TODO>>>
        protocol_config:    The configuration for the source protocol
        offset:             The `b` parameter in `y = mx + b` to be applied to
                            a value before being put in the Channel's queue
        multiplier:         The `m` parameter in `y = mx + b` to be applied to
                            a value before being put in the Channel's queue
        sample_rate:        The period in milliseconds between source samples
        report_rate:        The period in milliseconds between reports to
                            Murano
        report_on_change:   Boolean to only send value if the value has changed
                            since last sample
        mode:               The mode with which the Source is run.
                            poll | async | async2
        down_sample:        Method by which to down sample values in Channel
                            queue
                            MAX | MIN | SUM | AVG | ACT
        async_timeout:      The timeout in seconds for waiting on the event
                            set by an `async`-mode source.
        app_specific_config The reference object to the source from which data
                            will be received
        """
        threading.Thread.__init__(self, name=kwargs.get('name'))
        # TOP LEVEL KEYS
        self.name = kwargs.get('name')
        self.display_name = kwargs.get('display_name')
        self.description = kwargs.get('description')
        self.properties = kwargs.get('properties')
        self.protocol_config = kwargs.get('protocol_config', {})

        # PROTOCOL_CONFIG KEYS
        self.application = self.protocol_config.get('application')
        self.interface = self.protocol_config.get('interface')
        self.offset = self.protocol_config.get('offset', 0)
        self.multiplier = self.protocol_config.get('multiplier', 1)   # "gain"
        self.sample_rate = self.protocol_config.get('sample_rate')
        self.report_rate = self.protocol_config.get('report_rate')
        self.report_on_change = self.protocol_config.get('report_on_change')
        self.mode = self.protocol_config.get('mode', 'poll')
        self.down_sample = self.protocol_config.get('down_sample', 'ACT')

        self.app_specific_config = self.protocol_config.get('app_specific_config', {})
        self.positionals = self.app_specific_config.get('positionals', tuple())
        self.parameters = self.app_specific_config.get('parameters', {})
        self.__script = self.app_specific_config.get('__script', '')

        # DERIVED
        self.downsampler = DownSampler(self.down_sample)
        self.async_timeout = kwargs.get('async_timeout', 1.0)
        self.last_value = None
        self.last_report = 0
        self.q_out = queue.Queue() if self.down_sample else queue.LifoQueue()

        self.e_emission = threading.Event()
        if self.mode == 'async':
            self.e_async = threading.Event()
            self.parameters.update({
                '_fn': self.put_data,
                'event': self.e_async
            })
        self._kill = False

    def kill(self):
        """ Kill the Channel. """
        self._kill = True

    def is_killed(self):
        """ Return Channel's kill state. """
        return self._kill

    def get_data(self):
        """ Get value from Source.

        Import Source module and run specified function, passing in
        Channel.source.parameters as keyword arguments.
        """
        if not self.__script:
            val = getattr(__import__(self.app_specific_config['module']),
                          self.app_specific_config['function'])(*self.positionals, **self.parameters)
            return val
        else:
            try:
                exec(self.__script)
                return val
            except (SyntaxError, NameError):
                raise Exception('__script must define `val`')
        return val

    def handle_getting_of_data(self):
        """ Call get_data() while handling different Source modes.

        TODO: rename this method
        """
        if self.mode == 'poll':
            # Typical behavior. Poll a function at sample_rate
            # and send if report_on_change is false or the value
            # has changed.
            _new_val = self.get_data()
            if self.report_on_change and _new_val == self.last_value:
                # only report_on_change, even if report_rate passes
                self._sleep()
            else:
                self.try_emit()
                self.put_data(_new_val)
                self.last_value = _new_val
                self._sleep()

        elif self.mode == 'async':
            # Used if the function defined has the ability to
            # set events and add to the Channel's queue. The
            # function serves as a thread, so only start it once
            # and wait for the event to be set.
            if self.last_report == 0:
                self.get_data()
            else:
                LOG.debug('not fetching channel %s data',
                          self.name)
            self.e_async.wait(self.async_timeout)
            self.emit(time.time())
            self.e_async.clear()

        elif self.mode == 'async2':
            # Used if the function defined doesn't return unless
            # a condition has been met. Simpler async case than
            # mode `async`.
            self.put_data(self.get_data())
            self.emit(time.time())

    def try_emit(self):
        """ Determine whether or not to run emit()

        If the report_rate duration has passed, or report_on_change is
        set to True, call emit()
        """
        t = time.time()
        _t = self.last_report + self.report_rate / 1000
        if self.report_on_change or t >= _t:
            self.emit(t)
        else:
            LOG.debug('not reporting channel %s',
                      self.name)

    def emit(self, timestamp):
        """ Set event to request data_in be sent.

        Sets Channel.e_emission event, which is watched by
        config_io.ChannelWatcher.run(). Sets last_report to the current
        timestamp.
        """
        self.e_emission.set()
        self.last_report = timestamp

    def _sleep(self):
        """ Sleep for the sample rate

        TODO: only sleep remaining time after data is processed.
        """
        time.sleep(self.sample_rate / 1000)

    def put_data(self, data):
        """ Place data in queue.

        In the future, this method will be switchable and optionally send
        data to gmq or SQL database, e.g. send_data_to_gmq(data)

        Parameters:
        data:           Datapoint to be placed in queue.
        """
        self.q_out.put(Data(data, gain=self.multiplier, offset=self.offset))

    def run(self):
        """ Get data from source until Channel is killed. """
        LOG.debug('starting')
        while not self._kill:
            self.handle_getting_of_data()
        self.e_emission.set()
        LOG.debug('exiting')


class Data(tuple):
    """ Class to attach a timestamp to new data that is generated """
    def __new__(self, d, **kwargs):
        """ Subclasses tuple. (timestamp, data) """
        self.ts = time.time()
        self.offset = kwargs.get('offset')
        self.gain = kwargs.get('gain')
        try:
            self.d = d * self.gain + self.offset
        except TypeError:
            self.d = d
        # Attempt to JSON serialize the data point. If not
        # serializable, force into string.
        try:
            json.dumps(d)
        except TypeError:
            self.d = str(self.d)

        return tuple.__new__(Data, (self.ts, self.d))

    def age(self):
        """ Return age of data point in seconds """
        return time.time() - self.ts


class DownSampler(object):
    """ Class to deal with down sampling Channel data

    Methods:
    max:            Maximum value in list
    min:            Minimum value in list
    sum:            Sum of values in list
    avg:            Average of values in list
    act:            Last value in list ("actual value")
                    TODO: determine if this should return entire list
                          and if omitting down_sample in channel config
                          should result in the last value instead
    """
    method_mapper = {
        'max': max,
        'min': min,
        'sum': sum,
        'avg': lambda ls: float(sum(ls))/len(ls),
        'act': lambda ls: ls[-1]    # ls.pop()
    }

    def __init__(self, method):
        """
        Initialized by Channel.__init__()
        """
        self.method = method.lower()
        self._fn = self.method_mapper.get(self.method)

    def down_sample(self, data):
        """ Down sample data

        Assume data is list of tuples, e.g.
        [(ts, val), (ts, val), ...]
        """
        LOG.debug('Performing downsample %s on %s', self.method, data)
        try:
            return self._fn([d[1] for d in data])
        except:
            # kludge for non-tuple data
            return self._fn(data)
