"""Handle all the logic for adding a tweet to the supplied queue"""
from time import time
from json import loads

from tweepy.streaming import StreamListener

from .exception_handlers import is_queue, is_int, is_not_neg, check_end_time

class StreamQueueListener(StreamListener):
    """Subclass of a StreamListener from the tweepy package. This class is extended to allow
    for adding tweets to a multiprocessing queue and stop at an end time. Will place
    0 onto the queue to indicate that the end time has been reached."""

    def __init__(self):
        StreamListener.__init__(self)
        self._queue = None
        self._end_time = None

    @check_end_time
    def on_data(self, data):
        """main method for consuming a tweet and placing onto a queue. Needed as per
        tweepy specification"""

        if time() < self._end_time:
            self._queue.put(data)
            return None

        self._queue.put(0)
        return False
    
    @property
    def end_time(self):
        """total time (in seconds) to collect tweets for"""

        return self._end_time

    @end_time.setter
    @is_int
    @is_not_neg
    def end_time(self, collection_time):
        """establish an end time by supplying how long you want to collect tweets for
        in seconds"""

        self._end_time = time() + collection_time

    @property
    def queue(self):
        """get the queue supplied"""

        return self._queue

    @queue.setter
    @is_queue
    def queue(self, queue):
        self._queue = queue
