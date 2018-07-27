import unittest
import unittest.mock

import queue
from time import time, sleep
import json

from ..exception_handlers import EndTimeNotSetError
from ..stream_queue_listener import StreamQueueListener
from ..abstract import AbstractQueue

class TestStreamQueueListenerErrorHandling(unittest.TestCase):
    def setUp(self):
        self.streamqueuelistener = StreamQueueListener()

    def test_setting_queue_fails_if_supplied_queue_is_not_mp_queue(self):
        
        with self.assertRaises(TypeError):

            # supply queue attribute with a dictionary
            self.streamqueuelistener.queue = {}

    def test_end_time_not_set_error_raises(self):
        """on_data() raised when calling method"""

        with self.assertRaises(EndTimeNotSetError):
            self.streamqueuelistener.on_data('mockdata')

    def test_collection_time_is_int(self):
        """if the supplied collection_time argument is not of type int"""
        
        with self.assertRaises(TypeError):
            self.streamqueuelistener.end_time ='fake'

    def test_collection_time_is_not_neg(self):
        """end_time is not negative"""

        with self.assertRaises(ValueError):
            self.streamqueuelistener.end_time = -1


class TestStreamQueueListenerMethods(unittest.TestCase):
    def setUp(self):
        self.mockqueue = unittest.mock.MagicMock(AbstractQueue)

        self.streamqueuelistener = StreamQueueListener()
        self.streamqueuelistener.queue = self.mockqueue
        self.mock = {'mock': 1}

    def test_end_time_adds_collection_time_secs(self):
        """set_end_time(): is > lower bound possible for test"""

        self.streamqueuelistener.end_time = 2
        self.assertTrue(self.streamqueuelistener.end_time > time())

    def test_end_time_is_less_than_collection_time_secs(self):
        """end_time is < upper bound possible for test"""

        self.streamqueuelistener.end_time = 0
        self.assertTrue(self.streamqueuelistener.end_time < time() + 3)

    def test_on_data_loads_data_onto_queue(self):
        """test whether queue's put method gets called"""

        self.streamqueuelistener.end_time = 50

        # add the mock to the queue using on_data()
        self.streamqueuelistener.on_data(self.mock)

        # make sure on_data() calls put()
        self.mockqueue.put.assert_called_once()
    
    def test_on_data_pushes_a_zero_onto_queue_when_end_time_complete(self):
        """make sure that the zero signal gets pushed onto the queue so that
        the consumer knows that the tweet collection is complete"""

        # use a real instance of a queue to test
        self.streamqueuelistener.queue = queue.Queue()
        
        self.streamqueuelistener.end_time = 1
        
        # keep putting data onto the queue for 1 second
        on_data_value = self.streamqueuelistener.on_data(self.mock)
        
        while on_data_value is not False:
            on_data_value = self.streamqueuelistener.on_data(self.mock)

        # create an alias for the queue and get the size
        q = self.streamqueuelistener.queue
        qsize = q.qsize()

        while qsize is not 1:
            q.get()
            qsize = q.qsize()
        
        # this should be zero
        last_value_from_queue = q.get()

        self.assertEqual(last_value_from_queue, 0)