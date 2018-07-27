"""
Stream tweets to a queue
"""
from .parallel_stream import stream_to_queue
from .queue_stream import QueueStreamer

name = "stream_tweets"
__version__ = "1.0.0"

