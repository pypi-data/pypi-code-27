import unittest
import unittest.mock

import tweepy

from ..queue_stream import QueueStreamer
from ..exception_handlers import ConsumerKeysNotSetError
from ..abstract import AbstractQueue

class TestQueueStreamMethods(unittest.TestCase):
    def setUp(self):
        self.queuestreamer = QueueStreamer()
    
    def test_setting_queue_sets_queue_and_streamqueuelistener(self):
        """declaring the queue sets it for both QueueStreamer and
        component queue_stream_listener"""

        queue = unittest.mock.MagicMock(AbstractQueue)
        self.queuestreamer.queue = queue
        self.assertIsInstance(self.queuestreamer.queue, unittest.mock.MagicMock)

    
    def test_set_consumer_keys_creates_an_instance_of_oauthhanlder(self):
        """using set_consumer_keys() creates an instance of OAuthHandler"""
        
        self.queuestreamer.set_consumer_keys(consumer_key='mock_key', consumer_secret='mock_secret')

        self.assertIsInstance(self.queuestreamer._auth, tweepy.OAuthHandler)
    
    def test_access_tokens_cannot_be_called_before_set_consumer_keys(self):
        """set_consumer_keys() creates the auth object"""

        with self.assertRaises(ConsumerKeysNotSetError):
            self.queuestreamer.set_access_tokens('fake', 'fake')

    def test_stream_to_queue_calls_stream_filter(self):
        """make sure stream_to_queue() calls filter()"""

        self.queuestreamer.set_consumer_keys(consumer_key='fake', consumer_secret='fake2')
        self.queuestreamer.set_access_tokens(access_token='fake', access_token_secret='fake2')

        # load the mock streamer
        mock_stream = unittest.mock.MagicMock()
        self.queuestreamer._stream = mock_stream

        self.queuestreamer.stream_to_queue()
        
        mock_stream.filter.assert_called_once()
