"""Main module used to stream tweets to a multiprocessing queue."""
from tweepy import OAuthHandler
from tweepy import Stream

from .exception_handlers import consumer_keys_set, is_queue

from .stream_queue_listener import StreamQueueListener

class QueueStreamer(object):
    """Facade on top of Tweepy's Stream, OAuthHandler, and the
    StreamQueueListener (declared within this module). Tweets are streamed
    into the provided queue which must be an instance of an AbstractQueue."""

    def __init__(self, queue=None, collection_time=None):
        self._auth = None
        self._stream_queue_listener = StreamQueueListener()
        self._queue = queue
        self._collection_time = collection_time
        self._stream = None

    @property
    def queue(self):
        """the multiprocessing queue that tweets will be transferred into via
        StreamQueueListener
        """

        return self._queue

    @queue.setter
    def queue(self, queue):
        self._stream_queue_listener.queue = queue
        self._queue = queue

    @property
    def collection_time(self):
        """total time in seconds that tweets will be collected for"""

        return self._collection_time

    @collection_time.setter
    def collection_time(self, collection_time):
        """set how long you want to collect tweets for in seconds"""

        self._stream_queue_listener.end_time = collection_time
        self._collection_time = collection_time

        self._load_stream()

    def set_consumer_keys(self, consumer_key, consumer_secret):
        """set the consumer keys needed for the Twitter API"""

        self._auth = OAuthHandler(consumer_key, consumer_secret)

    @consumer_keys_set
    def set_access_tokens(self, access_token, access_token_secret):
        """set the access tokens needed for the Twitter API"""

        self._auth.set_access_token(access_token, access_token_secret)

        self._load_stream()

    def stream_to_queue(self, *args, **kwargs):
        """stream tweets to the queue

        Keyword arguments:
        queue -- instance of a multiprocessing Queue
        collection_time -- total amount of time in seconds to collect tweets for
        **kwargs -- exposed arguments for tweepy's Stream.filter method
        """

        self._stream.filter(*args, **kwargs)

    def _load_stream(self):
        """load Tweepy's Stream object if the listener and auth has been set"""

        if self._auth and self._stream_queue_listener:
            self._stream = Stream(self._auth, self._stream_queue_listener)
