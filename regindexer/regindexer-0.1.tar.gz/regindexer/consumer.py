import logging

from fedmsg.consumers import FedmsgConsumer
import moksha.hub.reactor
import six.moves.queue as queue

from regindexer.indexer import Indexer

log = logging.getLogger('regindexer.consumer')


class Consumer(FedmsgConsumer):
    config_key = 'regindexer.consumer.enabled'

    def __init__(self, hub):
        super(Consumer, self).__init__(hub)

        prefix = hub.config.get('topic_prefix')
        env = hub.config.get('environment')
        self.topic = [
            prefix + '.' + env + '.bodhi.mashtask.complete',
        ]

        # Need to do this explicitly to avoid triggering the Initialization task
        if not hub.config.get(self.config_key, False):
            return

        self.index_queue = queue.Queue()

        config_file = hub.config.get('regindexer.config_file',
                                     '/etc/regindexer/config.yaml')
        self.indexer = Indexer(config_file)

        moksha.hub.reactor.reactor.callInThread(self._do_index_work)
        self.index_queue.put('Initialization')

    def consume(self, raw_msg):
        topic = raw_msg['topic']
        msg = raw_msg['body']['msg']

        if msg.get('ctype') in ('container', 'flatpak'):
            log.info("Got %s message for ctype=%s", topic, msg['ctype'])
            # trigger rebuilding the index
            self.index_queue.put('Bodhi mash, ctype="%s"' % msg['ctype'])

    def _do_index_work(self):
        while True:
            reason = self.index_queue.get()
            log.info("Rebuilding index for: %s", reason)
            self.indexer.index()
