"""module used to parallelize tweet collection with a function"""
from .queue_stream import QueueStreamer

QUEUESTREAM = QueueStreamer()

def stream_to_queue(api_keys, queue, collection_time, *args, **kwargs):
    """Use this function in conjunction with multiprocessing.Process to parallelize
    consumption from queue with pushing to queue

    Keyword Arguments:
    api_keys - dict of api keys for twitter api access, e.g. {'consumer_key', 
    'consumer_secret', 'access_token', 'access_token_secret'}

    queue - multiprocessing.Queue() where tweets will be pushed into

    collection_time - total amount of time to collect tweets for in seconds

    *args, **kwargs - passed directly into tweepy's filter method
    """
    QUEUESTREAM.set_consumer_keys(consumer_key=api_keys['consumer_key'],
                                consumer_secret=api_keys['consumer_secret'])

    QUEUESTREAM.set_access_tokens(access_token=api_keys['access_token'], 
                                access_token_secret=api_keys['access_token_secret'])

    QUEUESTREAM.queue = queue
    QUEUESTREAM.collection_time = collection_time
    QUEUESTREAM.stream_to_queue(*args, **kwargs)
