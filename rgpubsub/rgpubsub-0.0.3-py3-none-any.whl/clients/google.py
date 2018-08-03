from rgpubsub import Publisher
from google.cloud import pubsub


class GoogleClientPublisher(Publisher):

    def __init__(self):
        self._publisher = pubsub.PublisherClient()

    def _send(self, topic_name, payload, arguments):
        future = self._publisher.publish(topic_name, payload, **arguments)
        future.result()
